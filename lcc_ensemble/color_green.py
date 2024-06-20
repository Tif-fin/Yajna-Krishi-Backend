import cv2
import numpy as np

def color_green(image):

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define the range for green color in HSV
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])

    # Define the range for yellow color in HSV
    lower_yellow = np.array([20, 40, 40])
    upper_yellow = np.array([35, 255, 255])

    # Define the range for dark yellow color in HSV
    lower_dark_yellow = np.array([15, 30, 30])
    upper_dark_yellow = np.array([35, 255, 255])

    # Create a mask for green color
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Create a mask for yellow color
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Create a mask for dark yellow color
    mask_dark_yellow = cv2.inRange(hsv, lower_dark_yellow, upper_dark_yellow)

    # Combine all masks to include green, yellow, and dark yellow regions
    mask = cv2.bitwise_or(mask_green, mask_yellow)
    mask = cv2.bitwise_or(mask, mask_dark_yellow)

    # Invert the mask to get non-leaf regions
    mask_inv = cv2.bitwise_not(mask)

    # Create a white background image
    white_background = np.full_like(image, 255)

    # Mask the original image to extract the leaf regions
    result = cv2.bitwise_and(image, image, mask=mask)

    # Mask the white background image to extract the non-leaf regions
    result_bg = cv2.bitwise_and(white_background, white_background, mask=mask_inv)

    # Combine the leaf regions with the white background
    final_result = cv2.add(result, result_bg)
    
    return final_result