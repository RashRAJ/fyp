import React, { useState } from 'react';
import axios from 'axios';

const CameraControl = ({ videoStreamUrl }) => {
    const [timer, setTimer] = useState(0);
    const [timerActive, setTimerActive] = useState(false);
    const [intervalId, setIntervalId] = useState(null);

    const startCamera = () => {
        // Start the camera via Flask API
        axios.post('http://127.0.0.1:5000/control_camera', { state: 'start' })
            .then(response => console.log(response))
            .catch(error => console.error('Error starting camera:', error));
        // Start the timer
        if (!timerActive) {
            const id = setInterval(() => {
                setTimer(prev => prev + 1);
            }, 1000);
            setIntervalId(id);
            setTimerActive(true);
        }
    };

    const pauseCamera = () => {
        // Pause the camera via Flask API (if applicable)
        axios.post('http://127.0.0.1:5000/control_camera', { state: 'stop' })
            .then(response => console.log(response))
            .catch(error => console.error('Error stopping camera:', error));
        // Pause the timer
        if (timerActive) {
            clearInterval(intervalId);
            setTimerActive(false);
        }
    };

    const stopCamera = () => {
        // Stop the camera via Flask API
        axios.post('http://127.0.0.1:5000/control_camera', { state: 'stop' })
            .then(response => console.log(response))
            .catch(error => console.error('Error stopping camera:', error));
        // Stop and reset the timer
        if (timerActive) {
            clearInterval(intervalId);
            setTimerActive(false);
            setTimer(0);
        }
    };

    const formatTime = (seconds) => {
        const hrs = Math.floor(seconds / 3600);
        const mins = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    };

    return (
        <div>
            <button onClick={startCamera}>Start Camera</button>
            <button onClick={pauseCamera}>Pause Camera</button>
            <button onClick={stopCamera}>Stop Camera</button>
            <div>
                Timer: {formatTime(timer)}
            </div>
        </div>
    );
};

export default CameraControl;
