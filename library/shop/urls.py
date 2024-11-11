from django.urls import path
from .views import (
    RegisterView,
    BookListView,
    PurchaseBookView,
    ReturnBookView,
    UpdateCreditView,
    UserBooksView,
    UpdateLocationView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("books/", BookListView.as_view(), name="book_list"),
    path("my-books/", UserBooksView.as_view(), name="user_books"),
    path("purchase/", PurchaseBookView.as_view(), name="purchase"),
    path("return/", ReturnBookView.as_view(), name="return_book"),
    path("update-credit/", UpdateCreditView.as_view(), name="update_credit"),
    path("update-location/", UpdateLocationView.as_view(), name="update_location"),
]
