import React, { useEffect, useState } from "react";
import Card from "../../components/Card";
import UserDetails from "./components/UserDetails";
import { Activity, Sun1 } from "iconsax-react";
import CameraControl from "../../components/CameraControl";
import axios from "axios";

function Home({ src }) {
  const [level, setLevel] = useState("None");
  const [alertnessLevel, setAlertnessLevel] = useState(100);
  const [timer, setTimer] = useState(0);
  const [cameraOn, setCameraOn] = useState(false);
  const [refreshKey, setRefreshKey] = useState(0);
  const user=localStorage.getItem('user');
  console.log(user)

  const formatTime = (seconds) => {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hrs.toString().padStart(2, "0")}:${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
  };
  useEffect(() => {
    const interval = setInterval(() => {
      axios
        .get("http://127.0.0.1:5000/drowsiness_level")
        .then((response) => {
          setLevel(response.data.level);
          setAlertnessLevel(mapDrowsinessToAlertness(response.data.level));
        })
        .catch((error) => console.error("Error fetching drowsiness level:", error));
    }, 10000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    console.log("cameraOn:", cameraOn);
  }, [cameraOn]);

  const handleCameraToggle = (status) => {
    setCameraOn(status);
    setRefreshKey(refreshKey + 1);
  };

  const mapDrowsinessToAlertness = (drowsiness) => {
    switch (drowsiness) {
      case "None":
        return 100;
      case "Low":
        return 70;
      case "Major":
        return 50;
      case "Critical":
        return 30;
      default:
        return 100;
    }
  };

  return (
    <div className="p-4">
      <div className="grid grid-cols-2 gap-10">
        <div>
        {cameraOn && (
          <div className="h-100 w-full bg-gray-300 rounded-md mb-5 relative">
            <img key={refreshKey} src={`${src}?key=${refreshKey}`} alt="Live Feed" className="object-cover w-full h-full rounded-md" />{" "}
            <span className="absolute top-5 left-[45%] bg-gray-900 text-white  py-1 px-4  rounded-xl ">{formatTime(timer)}</span>
          </div>
          )}
          <CameraControl 
            timer={timer} 
            setTimer={setTimer} 
            cameraOn={cameraOn} 
            setCameraOn={setCameraOn}
            handleCameraToggle={handleCameraToggle}
            />
        </div>
        <div>
          <UserDetails name={user} />
          <Card>
            <div className="grid grid-cols-2 py-6">
              <h4 className="font-bold text-lg">Alertness Level</h4>
              <button className="font-semibold bg-transparent border border-gray-300 py-1 rounded-md w-full hover:bg-gray-100 transition-all">Calibrate</button>
            </div>
            <div className="flex items-center gap-2 py-6">
              <Sun1 size="35" /> <h1 className="font-bold text-5xl">{alertnessLevel}%</h1>
            </div>
          </Card>
          <Card>
            <div className="grid grid-cols-2 py-6">
              <h4 className="font-bold text-lg">Drowsiness Status</h4>
            </div>
            <div className="flex items-center gap-2 py-6">
              <Activity size="35" /> <h1 className="font-bold text-5xl">{level}</h1>
            </div>
          </Card>
          <Card>
            <div className="grid grid-cols-2 py-6">
              <h4 className="font-bold text-lg">Warnings</h4>
            </div>
            <div className="py-6">
              <ul className="list-none flex gap-2 flex-col">
                <li className="flex gap-2">
                  <Sun1 /> Your alertness level is decreasing. Consider taking a break
                </li>
                <li className="flex gap-2">
                  {" "}
                  <Activity /> Drowsiness detected. Roll down the windows or play some music to stay awake
                </li>
              </ul>
            </div>
          </Card>
          <Card>
            <div className="grid grid-cols-2 py-6">
              <h4 className="font-bold text-lg">Ride History</h4>
            </div>
            <div className="py-6">
              <div className="relative overflow-x-auto shadow-md sm:rounded-lg">
                <table className="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
                  <thead className="text-sm text-gray-700 font-semibold capitalize bg-gray-50  dark:text-gray-600">
                    <tr>
                      <th scope="col" className="px-6 py-3">
                        Date
                      </th>
                      <th scope="col" className="px-6 py-3">
                        Duration
                      </th>
                      <th scope="col" className="px-6 py-3">
                        Alertness
                      </th>
                      <th scope="col" className="px-6 py-3">
                        Drowsiness
                      </th>
                    </tr>
                  </thead>
                  <tbody className="text-black">
                    <tr className="bg-white border-b ">
                      <th scope="row" className="px-6 py-4 font-medium whitespace-nowrap ">
                        April 23, 2024
                      </th>
                      <td className="px-6 py-4">Silver</td>
                      <td className="px-6 py-4">88%</td>
                      <td className="px-6 py-4">Low</td>
                    </tr>
                    <tr className="bg-white border-b ">
                      <th scope="row" className="px-6 py-4 font-medium whitespace-nowrap ">
                        March 23, 2024
                      </th>
                      <td className="px-6 py-4">White</td>
                      <td className="px-6 py-4">92%</td>
                      <td className="px-6 py-4">High</td>
                    </tr>
                    <tr className="bg-white ">
                      <th scope="row" className="px-6 py-4 font-medium whitespace-nowrap ">
                        February 23, 2024
                      </th>
                      <td className="px-6 py-4">Black</td>
                      <td className="px-6 py-4">88%</td>
                      <td className="px-6 py-4">Medium</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </Card>
          <Card></Card>
        </div>
      </div>
    </div>
  );
}

export default Home;
