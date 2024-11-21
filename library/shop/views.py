from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import CustomUser, Book, Purchase
from .serializers import (
    RegisterSerializer,
    BookSerializer,
    PurchaseBookSerializer,
    ReturnBookSerializer,
    UpdateCreditSerializer,
    UserLocationSerializer,
)
from django.shortcuts import render, redirect
from django.contrib.gis.geos import Polygon, Point
from rest_framework import status
from notifications.task import create_notification


tehran_polygon = Polygon(
    (
        (51.28, 35.40),  # شمال غرب
        (51.28, 35.50),  # شمال شرق
        (51.60, 35.50),  # شرق
        (51.60, 35.40),  # جنوب شرق
        (51.60, 35.30),  # جنوب شرقی
        (51.55, 35.30),  # جنوب
        (51.55, 35.25),  # جنوب غربی
        (51.28, 35.25),  # غرب
        (51.28, 35.40),  # شمال غرب
    )
)


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserBooksView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        user = self.request.user
        return user.owned_books.all()

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        books = self.get_queryset()
        return render(request, "my_books.html", {"books": books})


class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.filter(avalible=True)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        books = self.get_queryset()
        return render(request, "book_list.html", {"books": books})


class PurchaseBookView(generics.CreateAPIView):
    serializer_class = PurchaseBookSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user_location = user.location
            book_title = serializer.validated_data["book_title"]

            try:
                book = Book.objects.get(title=book_title)

            except Book.DoesNotExist:
                return Response(
                    {"error": "Book does not exist."}, status=status.HTTP_404_NOT_FOUND
                )

            if user.credit < book.price:
                return Response(
                    {"error": "Not enough credit to buy this book."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not user_location:
                return Response(
                    {"error": "Location not set for user."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not tehran_polygon.contains(user_location):
                return Response(
                    {"error": "Purchases are restricted to Tehran Province."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            if user.owned_books.filter(id=book.id).exists():
                return Response(
                    {"error": "You already own this book."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.credit -= book.price
            user.owned_books.add(book)
            book.avalible = False
            book.save()
            user.save()
            purchase = Purchase(
                user=user,
                book=book,
            )
            purchase.save()
            create_notification.delay(
                user.id, f"You have successfully purchased {book.title}."
            )

            return redirect("book_list")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReturnBookView(generics.CreateAPIView):
    serializer_class = ReturnBookSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            book_title = serializer.validated_data["book_title"]
            try:
                book = Book.objects.get(title=book_title)
                if not user.owned_books.filter(id=book.id).exists():
                    return Response(
                        {"error": "You do not own this book."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                purchase = Purchase.objects.filter(
                    user=user, book=book, is_returned=False
                ).first()
                if not purchase:
                    return Response(
                        {"error": "No valid purchase record found."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if not purchase.can_be_returned():
                    return Response(
                        {"error": "The return period has expired."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            except Book.DoesNotExist:
                return Response(
                    {"error": "Book does not exist."}, status=status.HTTP_404_NOT_FOUND
                )

            purchase.is_returned = True
            purchase.save()
            user.credit += book.price
            user.owned_books.remove(book)
            user.save()
            book.avalible = True
            book.save()
            create_notification.delay(
                user.id, f"You have successfully returned {book.title}."
            )
            return redirect("book_list")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateCreditView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UpdateCreditSerializer

    def put(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if not request.user.is_staff:
            return Response(
                {"error": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            credit = serializer.validated_data["credit"]

            try:
                choise_user = CustomUser.objects.get(username=username)
                choise_user.credit = credit
                choise_user.save()
                create_notification.delay(
                    choise_user.id, "wallet has been successfully updated."
                )

                return Response(
                    {"success": "User credit updated successfully."},
                    status=status.HTTP_200_OK,
                )

            except CustomUser.DoesNotExist:
                return Response(
                    {"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateLocationView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserLocationSerializer

    def put(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        user = request.user
        lat = request.data.get("latitude")
        lon = request.data.get("longitude")

        if not lat or not lon:
            return Response(
                {"error": "Latitude and longitude are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.location = Point(float(lon), float(lat))
        user.save()
        create_notification.delay(user.id, "location has been successfully updated.")

        return Response(
            {"success": "Location updated successfully."}, status=status.HTTP_200_OK
        )
