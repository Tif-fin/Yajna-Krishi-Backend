import torch
import cv2
import numpy as np
from transformers import SegformerForSemanticSegmentation

class LateBlightSegmentation:
    def __init__(self):
        self.class_labels = [
            (0, "Background"),
            (1, "Early Blight"),
            (2, "Late Blight"),
            (3, "Leafminer")
        ]

        # Map Labels to IDs
        self.id2label = {str(class_id): label for class_id, label in self.class_labels}
        self.label2id = {v: k for k, v in self.id2label.items()}

        # Number of classes
        self.num_classes = len(self.id2label.keys())
        
        self.model = SegformerForSemanticSegmentation.from_pretrained(
            "nvidia/segformer-b0-finetuned-ade-512-512",
            return_dict = True,  # Changed to True
            num_labels = self.num_classes,
            id2label = self.id2label,
            label2id = self.label2id,
            ignore_mismatched_sizes = True,
        )
        
        # Path to your checkpoint file
        checkpoint_path = "./static/Segmentation_Model/model-version10.ckpt"

        # Load checkpoint
        checkpoint = torch.load(checkpoint_path, map_location=torch.device('cpu'))
        
        # Modify the checkpoint keys to match the model's state_dict keys
        new_state_dict = {}
        for k, v in checkpoint['state_dict'].items():
            new_key = k.replace("model.", "")
            new_state_dict[new_key] = v
            
        # Load state dictionary into the model
        self.model.load_state_dict(new_state_dict, strict=False)

        
    def segmentation(self, file):
        file = file.read()
        # Decode the image data using OpenCV
        image = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (512, 512))
        image_tensor = torch.tensor(image).permute(2, 0, 1).unsqueeze(0).float()

        # Run the model on the image
        outputs = self.model(image_tensor)

        # Process the output image
        output_image = outputs.logits.argmax(dim=1).squeeze().numpy()

        # Map class labels to colors
        class_colors = {
            0: [0, 0, 0],         # Background (Black)
            1: [0, 255, 0],       # Early Blight (Green)
            2: [0, 0, 255],       # Late Blight (Blue)
            3: [255, 0, 0]        # Leafminer (Red)
        }

        # Convert grayscale mask to color
        output_image_color = np.zeros((output_image.shape[0], output_image.shape[1], 3), dtype=np.uint8)
        for class_index, color in class_colors.items():
            output_image_color[output_image == class_index] = color

        # Resize the output image
        output_image_color = cv2.resize(output_image_color, (image.shape[1], image.shape[0]))

        # Overlay the mask on the original image
        alpha = 0.6  # Adjust the transparency of the mask
        overlay_image = cv2.addWeighted(image, 1, output_image_color, alpha, 0)
        
        # Initialize an empty set to store unique predicted diseases
        unique_diseases = set()

        # Iterate over each pixel and get the corresponding class label
        for row in range(output_image.shape[0]):
            for col in range(output_image.shape[1]):
                class_index = output_image[row, col]
                class_label = self.class_labels[class_index][1]
                # Exclude the "Background" class label
                if class_label != "Background":
                    unique_diseases.add(class_label)
        
        # convert the set to a list
        unique_diseases = list(unique_diseases)

        return (overlay_image, unique_diseases)
