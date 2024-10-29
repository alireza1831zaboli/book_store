from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .models import CustomUser, Book
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    BookSerializer,
    PurchaseBookSerializer,
    ReturnBookSerializer,
    UpdateCreditSerializer,
)
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        if user is not None:
            refresh = RefreshToken.for_user(user)
            if user.is_active:
                login(request, user)
                response = Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                )

                # response.set_cookie(
                #     key="access_token",
                #     value=str(refresh.access_token),
                #     httponly=True,
                #     secure=False,
                #     samesite="Lax",
                # )
                return response
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


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

            except Book.DoesNotExist:
                return Response(
                    {"error": "Book does not exist."}, status=status.HTTP_404_NOT_FOUND
                )

            user.credit += book.price
            user.owned_books.remove(book)
            user.save()
            book.avalible = True
            book.save()

            return redirect("book_list")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateCreditView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UpdateCreditSerializer

    def put(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if not request.user.is_staff:  # یا request.user.is_superuser
            return Response({"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            credit = serializer.validated_data["credit"]

            try:
                choise_user = CustomUser.objects.get(username=username)
                choise_user.credit = credit 
                choise_user.save()

                return Response(
                    {"success": "User credit updated successfully."},
                    status=status.HTTP_200_OK,
                )

            except CustomUser.DoesNotExist:
                return Response(
                    {"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
