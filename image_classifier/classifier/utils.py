import numpy as np
import tensorflow as tf
from PIL import Image, ImageOps
import os
from django.conf import settings

# Disable scientific notation
np.set_printoptions(suppress=True)

# Model paths - now using TFLite
TFLITE_PATH = os.path.join(settings.BASE_DIR, 'model_files', 'model.tflite')
LABELS_PATH = os.path.join(settings.BASE_DIR, 'model_files', 'labels.txt')

print("="*50)
print("LOADING TFLITE MODEL")
print("="*50)
print(f"TFLITE_PATH: {TFLITE_PATH}")
print(f"File exists: {os.path.exists(TFLITE_PATH)}")
print(f"LABELS_PATH: {LABELS_PATH}")
print(f"File exists: {os.path.exists(LABELS_PATH)}")

# Load TFLite model
try:
    interpreter = tf.lite.Interpreter(model_path=TFLITE_PATH)
    interpreter.allocate_tensors()
    
    # Get input and output details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    print(f" TFLite model loaded successfully!")
    print(f"Input shape: {input_details[0]['shape']}")
    print(f"Output shape: {output_details[0]['shape']}")
    
except Exception as e:
    print(f" Error loading TFLite model: {e}")
    interpreter = None

# Load labels
try:
    with open(LABELS_PATH, 'r') as f:
        class_names = [line.strip() for line in f.readlines()]
    print(f" Loaded {len(class_names)} classes: {class_names}")
except Exception as e:
    print(f" Error loading labels: {e}")
    class_names = ["Happy", "Sad", "Neutral"]

print("="*50)

def classify_image(image_path):
    """
    Classify an image using the TFLite model
    """
    if interpreter is None:
        return {
            'success': False,
            'error': 'Model not loaded properly. Check server console.'
        }
    
    try:
        # Open and preprocess image
        image = Image.open(image_path).convert("RGB")
        
        # Resize image to 224x224 and crop from center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
        
        # Turn image into numpy array
        image_array = np.asarray(image)
        
        # Normalize the image (same as Teachable Machine)
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
        
        # Add batch dimension
        input_data = np.expand_dims(normalized_image_array, axis=0).astype(np.float32)
        
        # Run inference
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        
        # Get prediction
        prediction = interpreter.get_tensor(output_details[0]['index'])
        
        # Get the class with highest probability
        index = np.argmax(prediction[0])
        
        # Get class name (handle different label formats)
        if index < len(class_names):
            class_name = class_names[index]
            # Clean up class name (remove number if present like "0 Happy")
            if ' ' in class_name:
                parts = class_name.split(' ', 1)
                if len(parts) > 1 and parts[0].isdigit():
                    class_name = parts[1]
        else:
            class_name = f"Class {index}"
        
        confidence_score = float(prediction[0][index])
        
        return {
            'success': True,
            'class': class_name,
            'confidence': round(confidence_score * 100, 2),
            'raw_predictions': prediction[0].tolist()
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def get_class_names():
    """Return list of class names"""
    clean_names = []
    for name in class_names:
        if ' ' in name:
            parts = name.split(' ', 1)
            if len(parts) > 1 and parts[0].isdigit():
                name = parts[1]
        clean_names.append(name)
    return clean_names