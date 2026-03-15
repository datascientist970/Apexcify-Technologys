# AI Image Classifier


## 📝 Overview

**EmotionAI** is a web application that recognizes human emotions from uploaded photos. Using a pre-trained model from Google's Teachable Machine, it can detect three emotional states with high accuracy.

The application features a modern, user-friendly interface where users can upload images and receive instant emotion predictions with confidence scores.

---

## ✨ Features

### Emotion Detection
- **😊 Happy** - Detects smiling, joyful expressions
- **😞 Sad** - Recognizes frowning, unhappy faces
- **😐 Neutral** - Identifies neutral expressions

### User Experience
- **Drag & Drop Upload** - Simple image upload with drag-and-drop support
- **Image Preview** - See uploaded image before processing
- **AI Thinking Animation** - 5-second modal with robot avatar and timer
- **Instant Results** - Clear display of emotion with emoji and confidence percentage
- **Responsive Design** - Works perfectly on all devices

### Visual Design
- **Glass Morphism UI** - Modern translucent design with gradient backgrounds
- **Smooth Animations** - Elegant transitions and hover effects
- **Interactive Elements** - Engaging buttons and feedback

---

## 🛠️ Technology Stack

- **Backend**: Python, Django
- **Machine Learning**: TensorFlow, Google Teachable Machine
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Bootstrap 5, Font Awesome
- **Image Processing**: Pillow, NumPy

---

## 🚀 How It Works

### User Journey
1. **Upload** - User drags or clicks to upload a photo
2. **Process** - AI thinks for 5 seconds with animated modal
3. **Result** - Emotion and confidence score displayed instantly

### Behind the Scenes
- Image is preprocessed to 224x224 pixels
- Normalized for model compatibility
- Passed through TensorFlow Lite model
- Returns emotion prediction with confidence percentage

---

## 💻 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Setup

```bash
# Clone repository
git clone https://github.com/yourusername/emotionai-classifier.git

# Install dependencies
pip install -r requirements.txt

# Add your Teachable Machine model files
# Place model.tflite and labels.txt in model_files folder

# Run the application
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---

## 📱 Usage

1. **Open the application** in your web browser
2. **Upload an image** by clicking or dragging a photo
3. **Click "Classify Expression"** to start analysis
4. **Wait 5 seconds** while AI thinks (animated modal appears)
5. **View results** showing emotion emoji and confidence percentage

### Example Results
- Happy face → 😊 Happy with 95% confidence
- Sad face → 😞 Sad with 87% confidence
- Neutral face → 😐 Neutral with 92% confidence

---

## 🧠 About the Model

The emotion recognition model was trained using **Google's Teachable Machine**:
- 3 classes: Happy, Sad, Neutral
- 200+ training images per class
- Exported as TensorFlow Lite for optimal performance
- ~95% accuracy on test images

---

## 🎯 Applications

- **Customer Feedback** - Analyze customer satisfaction through expressions
- **Mental Health** - Track emotional states over time
- **User Experience Research** - Study user reactions to products
- **Educational Tools** - Teach about AI and machine learning
- **Entertainment** - Fun emotion detection for photos

---

## 🔮 Future Enhancements

- Webcam capture for real-time detection
- Additional emotions (Angry, Surprised, Fearful)
- Batch processing for multiple images
- Historical data dashboard
- Export results functionality
- Multi-language support

---

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👏 Acknowledgments

- **Google Teachable Machine** - For making machine learning accessible
- **TensorFlow Team** - For the excellent framework
- **Django Community** - For the robust web framework
- **Apexcify Technologies** - For the internship opportunity

---

<div align="center">
  <strong>Made with ❤️ during internship at Apexcify Technologies</strong>
</div>

---
