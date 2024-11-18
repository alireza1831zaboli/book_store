from django.urls import path
from .views import ImageUploadView, upload_image_page

urlpatterns = [
    path('upload-image/', ImageUploadView.as_view(), name='upload_image'),
    path('upload-page/', upload_image_page, name='upload_image_page'),
]
