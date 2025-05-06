import os
from ultralytics import YOLO

base_path = "/Users/brianpires/PycharmProjects/SafeStep/code/runs/detect/combined_results"
os.makedirs(base_path, exist_ok=True)

"""
1. Build a new YOLO model using (.yaml) 
#model = YOLO("yolov8n.yaml")

After training this model, you can
resume training by Loading a model with 
all pre-trained weights generated previously

--------> Code below is resumed training for pedestrian go lights
"""

#Load a current model
model = YOLO("/users/brianpires/PycharmProjects/SafeStep/code/runs/detect/crosswalk_model/train3/weights/best1.pt")

"""
Train model on new class without retraining the entire model. 
Instead 'appending' any new learned information onto the models already existing
knowledge
"""

# Update the model's number of classes
model.model.nc = 2  # Number of classes (crosswalk and pedestrian_green)
model.model.names = ['crosswalk', 'pedestrian_green']  # Class names

results = model.train(data = "config.yaml",
                      epochs=50,
                      resume = False,
                      project = base_path,
                      name = "combinedResults1")

