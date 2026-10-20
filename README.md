# AI Engineering Internship Projects — Apexcify Technologys

> A collection of the AI/ML projects built during my AI Engineering internship at Apexcify Technologys: an NLP FAQ chatbot, an emotion-recognition image classifier, a real-time object detection & tracking app, and an adaptive AI game opponent.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-Web_Apps-green)
![TensorFlow](https://img.shields.io/badge/ML-TensorFlow_/_Keras-orange)
![YOLOv8](https://img.shields.io/badge/CV-YOLOv8_+_SORT-purple)

## Overview

This repository documents my AI Engineering internship at **Apexcify Technologys**. Each folder is a self-contained project with its own code (and its own README where provided), covering a different applied-AI area: natural language processing, image classification, real-time computer vision, and game AI.

## Projects Inside

### 1. FAQ Chatbot — `faq_chatbot/`
A Django web app whose chatbot answers user questions by NLP-matching them against an admin-managed FAQ database (`chatbot/nlp_processor.py`), with confidence scoring, session/conversation tracking, and multi-intent handling. FAQs are managed through the Django admin panel.
→ See `faq_chatbot/Readme.md`

### 2. AI Image Classifier (EmotionAI) — `image_classifier/`
A Django web app that recognizes human emotions — **Happy, Sad, Neutral** — from uploaded photos, using a model trained with Google's Teachable Machine and exported as Keras (`.h5`) and TFLite (`model_files/`). Features drag-and-drop upload, image preview, and instant predictions with confidence scores.
→ See `image_classifier/README.md`

### 3. Object Detection & Tracking — `object_detector/`
A Django web app for video object detection and multi-object tracking: objects are detected per frame and assigned persistent tracking IDs using a SORT-style tracker (`detector/tracker.py`, `detector/sort.py`), with bounding boxes, class labels, and confidence scores shown in real time.
→ See `object_detector/readme.md`

### 4. Rock–Paper–Scissors with AI Opponent — `Rock-Paper-Scissors-with-AI-Opponent.py`
A single-file Python game with two AI modes: **basic** (random play) and **advanced** — an adaptive opponent that learns from the player's move history and patterns to predict the next move, with full game statistics tracking.

## Tech Stack

| Area | Technology |
|---|---|
| Language | Python 3.12 |
| Web framework | Django (chatbot, classifier, detector apps) |
| ML / DL | Keras / TensorFlow models (Teachable Machine exports, `.h5` / `.tflite`) |
| Computer vision | YOLOv8-style detection + SORT tracking |
| NLP | Custom NLP processor for FAQ question matching |
| Database | SQLite |
| Tools | Git & GitHub |

## Project Structure

```
├── faq_chatbot/          # Django + NLP FAQ chatbot
├── image_classifier/     # Django + Teachable Machine emotion classifier
├── object_detector/      # Django + detection & SORT tracking for video
└── Rock-Paper-Scissors-with-AI-Opponent.py
```

## Getting Started

Each Django project runs the same way — for example, the FAQ chatbot:

```bash
git clone https://github.com/datascientist970/Apexcify-Technologys.git
cd Apexcify-Technologys/faq_chatbot

python -m venv venv
venv\Scripts\activate        # Windows  (use source venv/bin/activate on Linux/macOS)
pip install django
python manage.py migrate
python manage.py runserver
```

Repeat with `image_classifier/` or `object_detector/` (the classifier also needs TensorFlow/Keras to load the bundled model files). The game needs nothing beyond Python:

```bash
python Rock-Paper-Scissors-with-AI-Opponent.py
```

## What I Learned

Building production-style AI features end-to-end: training and exporting ML models, integrating them into Django web apps, NLP intent matching, real-time video processing and tracking, and documenting technical work professionally.

## Author

**Muhammad Dawood** — AI & Data Science Engineer (AI Engineer Intern, Apexcify Technologys)
GitHub: https://github.com/datascientist970 · Mardan, Pakistan
