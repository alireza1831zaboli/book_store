from django.contrib import admin
from .models import Book, CustomUser, Purchase

admin.site.register(Book)
admin.site.register(CustomUser)
admin.site.register(Purchase)
