import React, { useEffect, useRef, useState, useCallback } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import './App.css';
import logo from './public/safewalk.png';
import { AnimatePresence, motion } from "framer-motion";

function HomePage() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 3 }}
      className="HomePage"
    >
      <header className="HomePage-header">
        <img src={logo} className='HomePage-logo' alt="Logo" />
        <h1>Safe Step</h1>
        <Link to="/main" className="HomePage-button">Tap to Start</Link>
      </header>
    </motion.div>
  );
}

function MainPage() {
  const videoRef = useRef(null);
  const [crosswalkDetected, setCrosswalkDetected] = useState(false);
  const [crosswalkConfidence, setCrosswalkConfidence] = useState(0);
  const [pedestrianDetected, setPedestrianDetected] = useState(false);
  const [pedestrianConfidence, setPedestrianConfidence] = useState(0);
  const [announcementMade, setAnnouncementMade] = useState(false);

  const announceMessage = (message) => {
    const utterance = new SpeechSynthesisUtterance(message);
    utterance.pitch = 0.75;
    utterance.rate = 0.9;
    utterance.volume = 1;
    window.speechSynthesis.speak(utterance);
  };

  useEffect(() => {
    const getVideo = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        console.error('Error accessing camera: ', err);
      }
    };
    getVideo();
  }, []);

  const fetchDetectionData = useCallback(async () => {
    try {
      const response = await fetch('http://localhost:5001/api/detections');
      const data = await response.json();

      // Update state based on the received data
      setCrosswalkDetected(data.crosswalk.detected);
      setCrosswalkConfidence(data.crosswalk.confidence);
      setPedestrianDetected(data.pedestrian_green.detected);
      setPedestrianConfidence(data.pedestrian_green.confidence);

      // Only proceed if both detections are present with confidence above 0.5
      if (
        data.crosswalk.detected &&
        data.crosswalk.confidence > 0.5 &&
        data.pedestrian_green.detected &&
        data.pedestrian_green.confidence > 0.5
      ) {
        if (!announcementMade) {
          const message = 'It is safe to cross.';
          announceMessage(message);
          setAnnouncementMade(true);
        }
      } else {
        setAnnouncementMade(false);
      }
    } catch (error) {
      console.error("Error fetching detection data:", error);
    }
  }, [announcementMade]);

  useEffect(() => {
    const intervalId = setInterval(fetchDetectionData, 1000);
    return () => clearInterval(intervalId);
  }, [fetchDetectionData]);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 1 }}
      className="App"
    >
      <header className="App-header">
        <img src={logo} className='App-logo' alt="Logo" />
        <h1>Safe Step</h1>
      </header>
      <div className="App-camera">
        <video ref={videoRef} autoPlay playsInline />
      </div>
      <div className="output-section">
        {crosswalkDetected && crosswalkConfidence > 0.5 && pedestrianDetected && pedestrianConfidence > 0.5 ? (
          <div>
            <h2>It is safe to cross.</h2>
            <p>
              Crosswalk Confidence: {crosswalkConfidence.toFixed(2)} | Pedestrian Symbol Confidence: {pedestrianConfidence.toFixed(2)}
            </p>
          </div>
        ) : null}
      </div>
    </motion.div>
  );
}

function App() {
  return (
    <Router>
      <AnimatePresence mode="wait">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/main" element={<MainPage />} />
        </Routes>
      </AnimatePresence>
    </Router>
  );
}

export default App;
