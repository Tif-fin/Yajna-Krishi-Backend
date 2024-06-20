import tensorflow as tf
import numpy as np
import cv2
from .color_green import color_green

class MobileNet_Ensemble:
    def __init__(self, weights_path='./static/lcc_ensemble_model/best_model_checkpoint2.weights.h5'):
        # Load the base model
        base_model = tf.keras.applications.MobileNetV3Large(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
        x = base_model.output
        x = tf.keras.layers.GlobalAveragePooling2D()(x)
        x = tf.keras.layers.Dense(512, activation='relu')(x)
        x = tf.keras.layers.Dense(256, activation='relu')(x)
        x = tf.keras.layers.Dense(128, activation='relu')(x)
        prediction_layer = tf.keras.layers.Dense(4, activation='softmax')(x)  # Assuming 4 classes
        self.model = tf.keras.models.Model(inputs=base_model.input, outputs=prediction_layer)

        # Load weights
        self.model.load_weights(weights_path)
    
    def predict(self, file):
        # Read and decode the file
        file = file.read()
        image = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (224, 224))
        
        image = color_green(image)
        
        # Preprocess the image
        image = image.astype('float32') / 255.0
        image = np.expand_dims(image, axis=0)  # Add batch dimension
        
        # Perform prediction
        preds = self.model.predict(image)
        
        # Get the class index with the highest probability
        max_index = np.argmax(preds)
        
        return max_index + 1  # Assuming class indices start from 1
