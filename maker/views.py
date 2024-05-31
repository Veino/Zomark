# zomark/views.py

from rest_framework.decorators import api_view
from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework import status
from accounts.models import ZomarkUser
from .models import Image
from .serializers import ImageSerializer
from PIL import Image as PILImage
from io import BytesIO
import os

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'HTTP Method': 'GET',
            'Endpoint': '/api/tasks',
            'Description': 'Retrieves a list of all tasks.'
        },
        {
            'HTTP Method': 'DELETE',
            'Endpoint': '/api/tasks',
            'Description': 'Deletes all tasks.'

        },
        {
            'HTTP Method': 'POST',
            'Endpoint': '/api/tasks',
            'Description': 'Creates a new task'

        },
        {
            'HTTP Method': 'GET',
            'Endpoint': '/api/tasks/{id}',
            'Description': 'Retrieves a single task by its unique identifier.'

        },
        {
            'HTTP Method': 'DELETE',
            'Endpoint': '/api/tasks/{id}',
            'Description': 'Deletes a task by its unique identifier.'

        },
        {
            'HTTP Method': 'PUT',
            'Endpoint': '/api/tasks/{id}',
            'Description': 'Updates the priority of a task.'
        },
        {
            'HTTP Method': 'PATCH',
            'Endpoint': '/api/tasks/{id}/actionitems/{action_item_id}',
            'Description': 'Updates the progress of an action item within a task.'
        },
        {
            'HTTP Method': 'DELETE',
            'Endpoint': '/api/tasks/{id}/actionitems/{action_item_id}',
            'Description': 'Deletes an action item within a task.'
        },
    ]

    return Response(routes)

def watermark_image(image):
    # Open the original image
    with PILImage.open(image.image.path) as img:
        # Open the watermark image
        with PILImage.open('static/Logo/Zoe Clothing_-_Icon.png') as watermark:
            # Resize the watermark image to fit the original image
            width, height = img.size
            ratio = min(width, height) / max(watermark.size)
            
            watermark_resized = watermark.resize((100, 100))
            watermark_width, watermark_height = watermark_resized.size
            position = ((width - watermark_width) // 2, height - watermark_height - 100)
            # Apply watermark to the original image
            img.paste(watermark_resized, position, watermark_resized)

            # Save the watermarked image
            image_name, image_ext = os.path.splitext(image.image.name)
            watermarked_image_io = BytesIO()
            img.save(watermarked_image_io, format=image_ext[1:])
            
            # Rename the watermarked image 
            watermarked_image_name = f"{image_name}_watermarked{image_ext}"
            image.watermarked_image.save(watermarked_image_name, ContentFile(watermarked_image_io.getvalue()))

@api_view(['POST'])
def upload_image(request):
    if request.method == 'POST':
        data = request.data

        image = Image.objects.create(
            image = data['image'],
            user = request.user,
        )
    
    serializer = ImageSerializer(image, many = False)
    watermark_image(image)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_images(request):
    images = Image.objects.filter(user=request.user)
    serializer = ImageSerializer(images, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def download_image(request, pk):
    image = Image.objects.get(pk=pk)
    # Get the watermarked image path
    watermarked_image_path = image.watermarked_image.path
    # Open the watermarked image
    with open(watermarked_image_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='image/jpeg')
        response['Content-Disposition'] = 'attachment; filename="watermarked_image.jpg"'
        return response
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_image(request, pk):
    image = Image.objects.get(pk=pk)
    image.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


