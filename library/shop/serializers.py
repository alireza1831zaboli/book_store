from rest_framework import serializers
from .models import CustomUser, Book
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("username", "password", "credit")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data["username"], credit=validated_data.get("credit", 0)
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "price")


class PurchaseBookSerializer(serializers.Serializer):
    book_title = serializers.CharField()

    


class ReturnBookSerializer(serializers.Serializer):
    book_title = serializers.CharField()  # فقط book_title




class UpdateCreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["credit"]
