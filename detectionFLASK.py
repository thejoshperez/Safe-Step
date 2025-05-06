import cv2
from ultralytics import YOLO
from flask import Flask, jsonify
from flask_cors import CORS 
import threading 

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})  

detection_data = {
    "crosswalk": {"detected":False,"confidence":0.0},
    "pedestrian_green": {"detected": False,"confidence":0.0},
}

class WebcamDetection:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.cap = cv2.VideoCapture(0)  
        if not self.cap.isOpened():
            print("Error: Could not open webcam")

    def check_detections(self, boxes):
        """Check for crosswalk detection with confidence above 80%."""
        global detection_data

        #RESET ALL DETECTION DATA
        detection_data["crosswalk"]["detected"] = False
        detection_data["crosswalk"]["confidence"] = 0.0
        detection_data["pedestrian_green"]["detected"] = False
        detection_data["pedestrian_green"]["confidence"] = 0.0
        
        for box in boxes:
            conf = box.conf[0].item() 
            cls = int(box.cls[0])
            class_name = self.model.names[cls]

            if class_name == "crosswalk" and conf > 0.50:
                detection_data["crosswalk"]["detected"] = True
                detection_data["crosswalk"]["confidence"] = conf
            elif class_name == "pedestrian_green" and conf > 0.50:
                detection_data["pedestrian_green"]["detected"] = True
                detection_data["pedestrian_green"]["confidence"] = conf

            print(detection_data)


    def run_detection(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Failed to capture frame")
                break

            results = self.model.predict(source=frame, conf=0.25)

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

@app.route('/api/detections', methods=['GET'])
def get_detections():
    return jsonify(detection_data)

def run_flask():
    app.run(port=5001)  


if __name__ == "__main__":
    threading.Thread(target=run_flask).start()  
    detector = WebcamDetection("/Users/joshuaperez/Desktop/Safe-Step FINAL copy/VisualAssistance/code/runs/detect/combined_results/combinedResults2/weights/best.pt")
    detector.run_detection()
    detector.cleanup()
