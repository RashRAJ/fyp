import React, { useState } from "react";
import axios from "axios";
import { Pause, Play } from "iconsax-react";

const CameraControl = ({ videoStreamUrl, timer, setTimer, cameraOn, setCameraOn }) => {
  const [timerActive, setTimerActive] = useState(false);
  const [intervalId, setIntervalId] = useState(null);

  const startCamera = () => {
    // Start the camera via Flask API
    axios
      .post("http://127.0.0.1:5000/control_camera", { state: "start" })
      .then((response) => {
        setCameraOn(true);
        console.log(response)
      })
      .catch((error) => console.error("Error starting camera:", error));
    // Start the timer
    if (!timerActive) {
      const id = setInterval(() => {
        setTimer((prev) => prev + 1);
      }, 1000);
      setIntervalId(id);
      setTimerActive(true);
    }
  };

  const pauseCamera = () => {
    // Pause the camera via Flask API (if applicable)
    axios
      .post("http://127.0.0.1:5000/control_camera", { state: "stop" })
      .then((response) => 
      {
      console.log(response)
      })
      .catch((error) => console.error("Error stopping camera:", error));
    // Pause the timer
    if (timerActive) {
      clearInterval(intervalId);
      setTimerActive(false);
    }
  };

  const stopCamera = () => {
    // Stop the camera via Flask API
    axios
      .post("http://127.0.0.1:5000/control_camera", { state: "stop" })
      .then((response) => {
        console.log(response)
        setCameraOn(false);
      })
      .catch((error) => console.error("Error stopping camera:", error));
    // Stop and reset the timer
    if (timerActive) {
      clearInterval(intervalId);
      setTimerActive(false);
      setTimer(0);
    }
  };

  return (
    <div className="grid grid-cols-2 gap-2">
      <button onClick={startCamera} className="flex justify-center gap-2 font-semibold bg-gray-900 text-white border border-black py-1 rounded-md w-full hover:bg-black transition-all">
        <Play /> Start Camera
      </button>
      <button onClick={stopCamera} className="flex justify-center gap-2 font-semibold bg-transparent border border-gray-300 py-1 rounded-md w-full hover:bg-gray-100 transition-all">
        <Pause />
        Stop Camera
      </button>
      {/* <button>Start Camera</button>
      <button>Pause Camera</button>
      <button onClick={stopCamera}>Stop Camera</button>
      <div>Timer: {formatTime(timer)}</div> */}
    </div>
  );
};

export default CameraControl;
