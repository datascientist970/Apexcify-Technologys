import cv2
import numpy as np
from ultralytics import YOLO
from sort import Sort
import argparse
import time
from collections import defaultdict

class ObjectTracker:
    def __init__(self, model_path='yolov8n.pt', video_source=0, conf_threshold=0.5):
        # Load YOLOv8 model
        print(f"Loading YOLOv8 model: {model_path}")
        self.model = YOLO(model_path)
        
        # Initialize SORT tracker
        self.tracker = Sort(max_age=30, min_hits=3, iou_threshold=0.3)
        
        # Video source
        self.video_source = video_source
        self.cap = cv2.VideoCapture(video_source)
        
        if not self.cap.isOpened():
            raise ValueError(f"Could not open video source: {video_source}")
        
        # Get video properties
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        
        # Settings
        self.conf_threshold = conf_threshold
        self.classes_to_detect = None  # None means detect all classes
        
        # Colors for different classes
        self.colors = np.random.randint(0, 255, size=(100, 3), dtype=np.uint8)
        
        # Statistics
        self.frame_count = 0
        self.fps_history = []
        self.object_counts = defaultdict(int)
        
        # COCO class names (for YOLOv8)
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
    
    def process_frame(self, frame):
        # Start timer for FPS calculation
        start_time = time.time()
        
        # Run YOLOv8 detection
        results = self.model(frame, conf=self.conf_threshold, classes=self.classes_to_detect)[0]
        
        # Extract detections
        detections = []
        if results.boxes is not None:
            boxes = results.boxes.xyxy.cpu().numpy()
            confidences = results.boxes.conf.cpu().numpy()
            class_ids = results.boxes.cls.cpu().numpy().astype(int)
            
            for box, conf, class_id in zip(boxes, confidences, class_ids):
                # Format: [x1, y1, x2, y2, score]
                detections.append([box[0], box[1], box[2], box[3], conf])
        
        # Convert to numpy array
        detections = np.array(detections) if detections else np.empty((0, 5))
        
        # Update tracker
        tracked_objects = self.tracker.update(detections)
        
        # Draw detections and tracking
        frame = self.draw_objects(frame, tracked_objects, detections, results)
        
        # Calculate FPS
        end_time = time.time()
        fps = 1.0 / (end_time - start_time + 1e-6)
        self.fps_history.append(fps)
        
        # Draw FPS
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        self.frame_count += 1
        return frame
    
    def draw_objects(self, frame, tracked_objects, detections, results):
        # Draw tracked objects (with IDs)
        for obj in tracked_objects:
            x1, y1, x2, y2, track_id = obj.astype(int)
            
            # Get color based on track ID
            color = tuple(int(c) for c in self.colors[track_id % len(self.colors)])
            
            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
            
            # Draw track ID
            label = f"ID: {track_id}"
            (label_w, label_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(frame, (x1, y1 - 25), (x1 + label_w + 10, y1), color, -1)
            cv2.putText(frame, label, (x1 + 5, y1 - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Draw YOLO detections (original)
        if results.boxes is not None:
            boxes = results.boxes.xyxy.cpu().numpy()
            class_ids = results.boxes.cls.cpu().numpy().astype(int)
            confidences = results.boxes.conf.cpu().numpy()
            
            for box, class_id, conf in zip(boxes, class_ids, confidences):
                x1, y1, x2, y2 = box.astype(int)
                class_name = self.class_names[class_id] if class_id < len(self.class_names) else f"Class {class_id}"
                
                # Update count
                self.object_counts[class_name] += 1
                
                # Draw class label
                label = f"{class_name} {conf:.2f}"
                (label_w, label_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                cv2.rectangle(frame, (x1, y2), (x1 + label_w + 10, y2 + 20), (0, 0, 0), -1)
                cv2.putText(frame, label, (x1 + 5, y2 + 15), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return frame
    
    def run(self):
        print(f"Starting object detection and tracking...")
        print(f"Video source: {self.video_source}")
        print(f"Resolution: {self.width}x{self.height}")
        print(f"Confidence threshold: {self.conf_threshold}")
        print("Press 'q' to quit, 's' to save frame, 'p' to pause")
        
        paused = False
        frame_count = 0
        
        while True:
            if not paused:
                ret, frame = self.cap.read()
                if not ret:
                    print("End of video stream")
                    break
                
                # Process frame
                processed_frame = self.process_frame(frame)
                
                # Add info overlay
                cv2.putText(processed_frame, f"Frame: {self.frame_count}", 
                           (10, self.height - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # Display
                cv2.imshow("Object Detection and Tracking (YOLOv8 + SORT)", processed_frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("Quitting...")
                break
            elif key == ord('p'):
                paused = not paused
                print("Paused" if paused else "Resumed")
            elif key == ord('s') and not paused:
                # Save current frame
                filename = f"frame_{self.frame_count}.jpg"
                cv2.imwrite(filename, processed_frame)
                print(f"Saved {filename}")
        
        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()
        
        # Print statistics
        self.print_statistics()
    
    def print_statistics(self):
        """
        Print tracking statistics
        """
        print("\n" + "="*50)
        print("TRACKING STATISTICS")
        print("="*50)
        print(f"Total frames processed: {self.frame_count}")
        print(f"Average FPS: {np.mean(self.fps_history):.2f}")
        print(f"Objects detected:")
        
        # Group by class
        for class_name, count in self.object_counts.items():
            print(f"  {class_name}: {count}")
    
    def set_classes(self, class_ids):
        """
        Set specific classes to detect
        """
        self.classes_to_detect = class_ids
        print(f"Detecting only classes: {[self.class_names[i] for i in class_ids]}")

def main():
    parser = argparse.ArgumentParser(description='Object Detection and Tracking with YOLOv8 + SORT')
    parser.add_argument('--source', type=str, default='0',
                        help='Video source: 0 for webcam, or path to video file')
    parser.add_argument('--model', type=str, default='yolov8n.pt',
                        help='YOLOv8 model path (yolov8n.pt, yolov8s.pt, yolov8m.pt, etc.)')
    parser.add_argument('--conf', type=float, default=0.5,
                        help='Confidence threshold')
    parser.add_argument('--classes', type=int, nargs='+',
                        help='Class IDs to detect (e.g., --classes 0 1 for person and bicycle)')
    
    args = parser.parse_args()
    
    # Convert video source to int if it's a number (webcam index)
    if args.source.isdigit():
        video_source = int(args.source)
    else:
        video_source = args.source
    
    # Create tracker
    tracker = ObjectTracker(
        model_path=args.model,
        video_source=video_source,
        conf_threshold=args.conf
    )
    
    # Set specific classes if provided
    if args.classes:
        tracker.set_classes(args.classes)
    
    # Run
    tracker.run()

if __name__ == "__main__":
    main()