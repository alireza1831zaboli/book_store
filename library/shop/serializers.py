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


class UserLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["location"]


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "price")


class PurchaseBookSerializer(serializers.Serializer):
    book_title = serializers.CharField()


class ReturnBookSerializer(serializers.Serializer):
    book_title = serializers.CharField()


class UpdateCreditSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    credit = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        model = CustomUser
        fields = ["username", "credit"]
