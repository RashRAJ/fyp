import React from 'react';
import CameraFeed from './components/CameraFeed';
import CameraControl from './components/CameraControl';
import DrowsinessLevel from './components/DrowsinessLevel';

function App() {
  const videoStreamUrl = "http://127.0.0.1:5000/video";

  return (
    <div className="App">
      <h1>Drowsiness Detection System</h1>
      <CameraFeed src={videoStreamUrl} />
      <CameraControl videoStreamUrl={videoStreamUrl} />
      <DrowsinessLevel />
    </div>
  );
}

export default App;
