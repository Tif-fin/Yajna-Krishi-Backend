from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from .late_blight_segmentation import LateBlightSegmentation
import os 
import cv2
import uuid

@api_view(['POST'])
def late_blight_segmentation(request):
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file uploaded'}, status=400)
    
    uploaded_file = request.FILES['file']
    
    # Instantiate the processing class/function
    late_blight_segmentation = LateBlightSegmentation()
    
    # Process the uploaded file
    try:
        (processed_image, diseases) = late_blight_segmentation.segmentation(uploaded_file)  # Replace with actual processing logic
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    # Generate a file name and save the processed image to the media directory
    processed_image_name = f'{str(uuid.uuid4())}.png'
    processed_image_path = os.path.join(settings.MEDIA_ROOT, processed_image_name)
    
    try:
        # Save the processed image using OpenCV's imwrite function
        cv2.imwrite(processed_image_path, processed_image)
    except Exception as e:
        return JsonResponse({'error': f'Failed to save processed image: {str(e)}'}, status=500)
    
    # Return success response
    # Disease is a list of unique diseases predicted in the image
    class_colors = {
    'earlyblight' : 'Green',
    'lateblight' : 'Blue',
    'leafminer' : 'Red'
}
    return JsonResponse({'success': 'Processed image saved successfully', 'processed_image_url': settings.MEDIA_URL + processed_image_name, 'diseases': diseases, 'class_colors': class_colors})
