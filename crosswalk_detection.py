import cv2
from ultralytics import YOLO
from flask import Flask, jsonify
from flask_cors import CORS
import threading

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# Thread-safe detection data with a lock
detection_data = {
    "crosswalk": {"detected": False, "confidence": 0.0},
    "pedestrian_green": {"detected": False, "confidence": 0.0},
}
detection_data_lock = threading.Lock()

class WebcamDetection:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open webcam")
            exit(1) 

    def check_detections(self, boxes):
        """Check for crosswalk and pedestrian_green detection with confidence above 50%."""
        global detection_data

        # Use lock when modifying shared data
        with detection_data_lock:
            # RESET ALL DETECTION DATA
            detection_data["crosswalk"]["detected"] = False
            detection_data["crosswalk"]["confidence"] = 0.0
            detection_data["pedestrian_green"]["detected"] = False
            detection_data["pedestrian_green"]["confidence"] = 0.0

            for box in boxes:
                conf = box.conf.item()
                cls = int(box.cls.item())
                class_name = self.model.names[cls]

                if class_name == "crosswalk" and conf > 0.50:
                    detection_data["crosswalk"]["detected"] = True
                    detection_data["crosswalk"]["confidence"] = conf
                elif class_name == "pedestrian_green" and conf > 0.50:
                    detection_data["pedestrian_green"]["detected"] = True
                    detection_data["pedestrian_green"]["confidence"] = conf

            # Print detection data for debugging
            print(detection_data)

    def run_detection(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Failed to capture frame")
                break

            # Corrected predict method call
            results = self.model.predict(frame, conf=0.25)

            for result in results:
                boxes = result.boxes

                self.check_detections(boxes)

                annotated_frame = result.plot()
                cv2.imshow('Webcam', annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()

@app.route('/api/detection', methods=['GET'])
def get_detection():
    try:
        # Use lock when reading shared data
        with detection_data_lock:
            data_copy = detection_data.copy()
        return jsonify(data_copy)
    except Exception as e:
        print(f"Error in /api/detection: {e}")
        return jsonify({"error": "Internal server error"}), 500

def run_flask():
    app.run(port=5000, threaded=True)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    detector = WebcamDetection("VisualAssistance/code/runs/detect/combined_results/combinedResults2/weights/best.pt")
    detector.run_detection()
    detector.cleanup()
