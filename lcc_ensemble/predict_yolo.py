from ultralytics import YOLO
import numpy as np
import cv2
from .color_green import color_green

class YOLO_Ensemble:
    def __init__(self):
        self.model = YOLO('./static/lcc_ensemble_model/LCC_Newest_001_001_Best.pt')
        
    def predict(self, file):
        file = file.read()
        image = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (224, 224))
        
        image = color_green(image)
        results = self.model(image)
        arr = results[0].probs.data.cpu().numpy()
        max_index = np.argmax(arr)
        
        return max_index+1