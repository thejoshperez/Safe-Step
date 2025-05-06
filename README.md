# SafeStep

SafeStep is a prototype application designed to help pedestrians cross streets more safely using computer vision and accessible audio cues. It detects crosswalks and green pedestrian signals in real time and announces when it is safe to cross, creating a hands-free experience.

## What It Does

- Detects crosswalks and pedestrian signals using live video input
- Announces when it's safe to cross using speech output
- Aims to make street crossing safer and more accessible, especially for people with visual impairments

## How It Works

SafeStep was built as a full-stack project with both a backend and a frontend:

- **Model Training**:  
  We trained a custom object detection model using the YOLOv8 framework. The model was trained on labeled images of crosswalks and pedestrian signals to accurately detect them in real time.

- **Backend**:  
  A Python Flask server runs the trained model using OpenCV to process live webcam video. It sends detection results to the frontend and manages updates.

- **Frontend**:  
  The frontend was built using React. It connects to the backend to get detection results and uses the Web Speech API to announce safety cues like “Safe to cross.”

## Current Status

The project currently runs locally on our machines. You need to start both the backend and frontend servers to use it. While it's not deployed online yet, we hope to host it in the future so it can be used on mobile or edge devices.

## Future Plans

- Deploy the application online or to a mobile platform
- Add support for more types of pedestrian signals
- Improve the user interface and performance
- Expand accessibility features

## Why It Matters

SafeStep was created during a hackathon to explore how computer vision could be used for real-world safety applications. It's still early in development, but it shows how accessible technology can make a meaningful difference in public spaces.

