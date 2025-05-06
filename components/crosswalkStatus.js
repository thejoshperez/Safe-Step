import React, { useEffect, useState } from 'react';

const CrosswalkStatus = () => {
    const [crosswalkData, setCrosswalkData] = useState({ detected: false, confidence: 0.0 });

    useEffect(() => {
        const fetchCrosswalkData = async () => {
            try {
                const response = await fetch('http://localhost:5000/api/crosswalk');
                const data = await response.json();
                setCrosswalkData(data);
            } catch (error) {
                console.error("Error fetching crosswalk data:", error);
            }
        };

        const intervalId = setInterval(fetchCrosswalkData, 1000); 

        return () => clearInterval(intervalId); 
    }, []);

    return (
        <div>
            <h1>Crosswalk Detection Status</h1>
            <p>Detected: {crosswalkData.detected ? 'Yes' : 'No'}</p>
            {crosswalkData.detected && <p>Confidence: {crosswalkData.confidence.toFixed(2)}</p>}
        </div>
    );
};

export default CrosswalkStatus;
