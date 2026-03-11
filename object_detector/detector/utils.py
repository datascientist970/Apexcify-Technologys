import cv2
import numpy as np
from ultralytics import YOLO
from .sort import Sort
import time
from collections import defaultdict
import os
from django.conf import settings

class VideoProcessor:
    def __init__(self, model_path='yolov8n.pt', conf_threshold=0.5):
        self.model = YOLO(model_path)
        self.tracker = Sort(max_age=30, min_hits=3, iou_threshold=0.3)
        self.conf_threshold = conf_threshold
        
        # COCO class names
        self.class_names = [
            'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
            'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat',
            'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack',
            'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
            'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
            'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
            'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair',
            'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse',
            'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator',
            'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
        ]
        
        # Colors for visualization
        self.colors = np.random.randint(0, 255, size=(100, 3), dtype=np.uint8)
    
    def process_frame(self, frame, frame_number):
        # Run detection
        results = self.model(frame, conf=self.conf_threshold, verbose=False)[0]
        
        # Extract detections
        detections = []
        frame_detections = []
        
        if results.boxes is not None:
            boxes = results.boxes.xyxy.cpu().numpy()
            confidences = results.boxes.conf.cpu().numpy()
            class_ids = results.boxes.cls.cpu().numpy().astype(int)
            
            for box, conf, class_id in zip(boxes, confidences, class_ids):
                detections.append([box[0], box[1], box[2], box[3], conf])
                frame_detections.append({
                    'bbox': box.tolist(),
                    'confidence': float(conf),
                    'class_id': int(class_id),
                    'class_name': self.class_names[class_id]
                })
        
        detections = np.array(detections) if detections else np.empty((0, 5))
        
        # Update tracker
        tracked_objects = self.tracker.update(detections)
        
        # Draw on frame
        frame = self.draw_objects(frame, tracked_objects)
        
        # Prepare tracking results
        tracking_results = []
        for obj in tracked_objects:
            x1, y1, x2, y2, track_id = obj.astype(int)
            tracking_results.append({
                'bbox': [x1, y1, x2, y2],
                'track_id': int(track_id)
            })
        
        return frame, frame_detections, tracking_results
    
    def draw_objects(self, frame, tracked_objects):
        for obj in tracked_objects:
            x1, y1, x2, y2, track_id = obj.astype(int)
            color = tuple(int(c) for c in self.colors[track_id % len(self.colors)])
            
            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
            
            # Draw track ID
            label = f"ID: {track_id}"
            cv2.putText(frame, label, (x1 + 5, y1 - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        return frame
    
    def process_video(self, input_path, output_path, progress_callback=None):
        cap = cv2.VideoCapture(input_path)
        
        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_count = 0
        fps_history = []
        all_detections = []
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            start_time = time.time()
            
            # Process frame
            processed_frame, frame_detections, tracking_results = self.process_frame(frame, frame_count)
            
            # Calculate FPS
            end_time = time.time()
            fps = 1.0 / (end_time - start_time + 1e-6)
            fps_history.append(fps)
            
            # Add info to frame
            cv2.putText(processed_frame, f"Frame: {frame_count}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(processed_frame, f"FPS: {fps:.1f}", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Write frame
            out.write(processed_frame)
            
            # Store detections
            for det in frame_detections:
                det['frame'] = frame_count
                det['timestamp'] = frame_count / fps if fps > 0 else 0
                all_detections.append(det)
            
            frame_count += 1
            
            # Progress callback
            if progress_callback and frame_count % 30 == 0:
                progress = (frame_count / total_frames) * 100
                progress_callback(progress, frame_count, total_frames)
        
        cap.release()
        out.release()
        
        # Calculate statistics
        stats = {
            'total_frames': frame_count,
            'average_fps': np.mean(fps_history) if fps_history else 0,
            'detections': all_detections
        }
        
        return stats