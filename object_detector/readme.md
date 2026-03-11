# Object Detection & Tracking with YOLOv8 + SORT
A real-time object detection and tracking application that identifies objects in videos and assigns unique tracking IDs to each object.

## What This Project Does
This application takes a video file and:

Detects objects (people, cars, animals, etc.) in each frame

Draws colored boxes around each detected object

Assigns a unique ID to each object that stays the same as it moves

Shows object names and confidence scores

Displays everything in real-time as the video plays

## How It Works
Upload any video file (MP4, AVI, MOV, MKV)

Watch as the video plays with colored boxes around objects

See each object gets its own ID number

View statistics showing what was detected

## Technologies Used
TensorFlow.js - Runs AI model in browser

COCO-SSD - Pre-trained model that can detect 80 different objects

HTML5/CSS3 - Modern, clean interface

JavaScript - Handles video processing and tracking

## Features
 Drag and drop video upload

 Real-time object detection

 Unique tracking IDs for each object

 Color-coded bounding boxes

 Live statistics (frames, detections, FPS)

 No installation needed - works in browser

 Works with any video format

## How to Use
Open the webpage using python manage.py runserver    in browser enter http://127.0.0.1:8000/

Drag a video file or click to browse

Watch as objects are detected automatically

See colored boxes with IDs appear on screen

Check statistics panel for detection info

## What You'll See
Colored Boxes around each detected object

ID Numbers that follow objects as they move

Object Names (person, car, dog, etc.)

Confidence Scores showing how sure the AI is

Live Counts of frames and detections

## Example Detections
Person detected → Box with "person 95%" and "ID: 1"

Car detected → Box with "car 87%" and "ID: 2"

Dog detected → Box with "dog 92%" and "ID: 3"

Each object keeps the same ID throughout the video.

## Why This Project Matters
This shows how AI can:

Understand what's in a video

Track objects as they move

Count and identify different items

Work in real-time in your browser

## Created For
Internship project at Apexcify Technologies

