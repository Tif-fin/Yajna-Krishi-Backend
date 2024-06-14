from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from .late_blight_segmentation import LateBlightSegmentation
import os 

@api_view(['POST'])
def late_blight_segmentation(request):
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file uploaded'}, status=400)
    
    uploaded_file = request.FILES['file']
    
    # Instantiate the processing class/function
    late_blight_segmentation = LateBlightSegmentation()
    
    # Process the uploaded file
    try:
        processed_image = late_blight_segmentation.segmentation(uploaded_file)  # Replace with actual processing logic
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    # Generate a file name and save the processed image to the media directory
    processed_image_name = 'processed_image.png'  # Adjust file name as needed
    processed_image_path = os.path.join(settings.MEDIA_ROOT, processed_image_name)
    
    try:
        with default_storage.open(processed_image_path, 'wb') as destination:
            destination.write(processed_image.read())
    except Exception as e:
        return JsonResponse({'error': f'Failed to save processed image: {str(e)}'}, status=500)
    
    # Return success response
    return JsonResponse({'success': 'Processed image saved successfully', 'processed_image_url': settings.MEDIA_URL + processed_image_name})
