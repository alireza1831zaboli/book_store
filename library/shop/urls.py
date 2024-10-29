from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    BookListView,
    PurchaseBookView,
    ReturnBookView,
    UpdateCreditView,
    UserBooksView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("books/", BookListView.as_view(), name="book_list"),
    path("my-books/", UserBooksView.as_view(), name="user_books"),
    path("purchase/", PurchaseBookView.as_view(), name="purchase"),
    path("return/", ReturnBookView.as_view(), name="return_book"),
    path("update-credit/", UpdateCreditView.as_view(), name="update_credit"),
]
