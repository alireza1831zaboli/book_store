import requests
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

            local_path = './dir_data/temp_uploaded_image.tif'
            with open(local_path, 'wb') as f:
                for chunk in image.chunks():
                    f.write(chunk)
            
            geoserver_url = (
                "http://localhost:8080/geoserver/rest/workspaces/"
                "library_workspace/coveragestores/library_store/file.geotiff"
            )
            geoserver_username = "admin"
            geoserver_password = "geoserver" 
            
            with open(local_path, 'rb') as file:
                response = requests.put(
                    geoserver_url,
                    headers={"Content-Type": "image/tiff"},
                    auth=(geoserver_username, geoserver_password),
                    data=file,
                )

            if response.status_code in [200, 201]:
                return Response(
                    {"message": "Image uploaded successfully to GeoServer."},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"error": "Failed to upload to GeoServer.", "details": response.text},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def upload_image_page(request):
    return render(request, 'upload_image.html')

