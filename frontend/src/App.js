import React from "react";
import CameraFeed from "./components/CameraFeed";
import CameraControl from "./components/CameraControl";
import DrowsinessLevel from "./components/DrowsinessLevel";
import "@fontsource-variable/nunito";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import SignIn from "./pages/Authentication/SignIn";
import SignUp from "./pages/Authentication/SignUp";

function App() {
  const videoStreamUrl = "http://127.0.0.1:5000/video";

  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<SignIn />}></Route>
          <Route path="/createaccount" element={<SignUp />}></Route>
        </Routes>
      </BrowserRouter>
      {/* <h1>Drowsiness Detection System</h1>
      <CameraFeed src={videoStreamUrl} />
      <CameraControl videoStreamUrl={videoStreamUrl} />
      <DrowsinessLevel /> */}
    </div>
  );
}

export default App;
