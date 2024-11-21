from rest_framework import serializers
from .models import CustomUser, Book
from django.contrib.gis.geos import Point
from notifications.task import create_notification

class RegisterSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)

    class Meta:
        model = CustomUser
        fields = ("username", "password", "credit", "latitude", "longitude")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        latitude = validated_data.pop("latitude", None)
        longitude = validated_data.pop("longitude", None)

        user = CustomUser(
            username=validated_data["username"],
            credit=validated_data.get("credit", 0)
        )
        user.set_password(validated_data["password"])

        if latitude is not None and longitude is not None:
            user.location = Point(longitude, latitude)

        user.save()
        create_notification.delay(user.id, "You have successfully register.")
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
