from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .predict_yolo import YOLO_Ensemble
from .predict_mobilenet import MobileNet_Ensemble
import numpy as np

@api_view(['POST'])
def predict(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
        
        uploaded_files = request.FILES.getlist('file')
        
        if len(uploaded_files) != 10:
            return JsonResponse({'error': 'Please upload 10 images'}, status=400)
        
        yolo_ensemble = YOLO_Ensemble()
        mobilenet_ensemble = MobileNet_Ensemble()
        
        yolo_predictions = []
        mobilenet_predictions = []
        
        for uploaded_file in uploaded_files:
            
            uploaded_file.seek(0)
            mobilenet_prediction = mobilenet_ensemble.predict(uploaded_file)
            mobilenet_predictions.append(mobilenet_prediction.tolist())
            
            uploaded_file.seek(0)
            yolo_prediction = yolo_ensemble.predict(uploaded_file)
            yolo_predictions.append(yolo_prediction.tolist())

        
        yolo_predictions = np.array(yolo_predictions)
        mobilenet_predictions = np.array(mobilenet_predictions)
        
        # Concatenate predictions from both models
        combined_predictions = np.concatenate((yolo_predictions, mobilenet_predictions), axis=0)
        
        combined_predictions = combined_predictions.tolist()
        
        probabilities = [int(combined_predictions.count(1))/20, int(combined_predictions.count(2))/20, int(combined_predictions.count(3))/20, int(combined_predictions.count(4))/20]
        
        max_index = np.argmax(probabilities) + 1
                
        return JsonResponse({'prediction': max_index.tolist()})