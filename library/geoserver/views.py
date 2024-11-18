from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageUploadSerializer
from django.shortcuts import render, redirect

class ImageUploadView(APIView):

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        
        serializer = ImageUploadSerializer(data=request.data)
        
        if serializer.is_valid():
            image = serializer.validated_data['image']
            
            geo_path = './dir_data/uploaded_image.tif'
            
            with open(geo_path, 'wb') as f:
                for chunk in image.chunks():
                    f.write(chunk)
            
            return Response({"message": "Image uploaded successfully."}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def upload_image_page(request):
    return render(request, 'upload_image.html')