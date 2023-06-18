import React, { useState, useEffect, useRef } from "react";
import "./results.css";
import ReactPlayer from "react-player";
import Logo from "../only_logo.png";
import TopBar from "../topBar/topBar";
import HeatMap from "../heatMap/heatMap";
import { useNavigate } from 'react-router-dom';

function VideoPlayer(props) {
  const videoRef = useRef(null);
  const [playing, setPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [currentIndex, setCurrentIndex] = useState(-1);
  const navigate = useNavigate();
  const data = JSON.parse(props.results.replace(/'/g, '"'));
  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.seekTo(currentTime);
    }
  }, [currentTime]);



  const buttons = [
    {
      name: "Sign out",
      route: "/",
    },
    {
      name: "Sign up",
      route: "/signup",
    },
  ];

  const handleJumpButtonClick = () => {
    const lastIndex = props.numberList.length - 1;

    if (lastIndex >= 0) {
      if (currentIndex < lastIndex) {
        const nextIndex = currentIndex + 1;
        const nextNumber = props.numberList[nextIndex];
        setCurrentIndex(nextIndex);
        if (typeof nextNumber === "number" && isFinite(nextNumber)) {
          setCurrentTime(nextNumber);
        }
        setPlaying(false);
      } else {
        setCurrentIndex(0);
        setCurrentTime(props.numberList[0]);
        setPlaying(false);
      }
    } else {
      console.log("Number list is empty");
    }
  };

  const handleSeek = (seconds) => {
    setCurrentTime(seconds);
  };

  const handleNextQuery=()=>{
    navigate('/uploadVideo');
  }

  const handleCaptureFrame = () => {
    console.log(videoRef.current);  
    const player = videoRef.current.getInternalPlayer();
    console.log(player)
    if (player) {
      const canvas = document.createElement('canvas');
      canvas.width = player.clientWidth;
      canvas.height = player.clientHeight;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(player, 0, 0, canvas.width, canvas.height);
      canvas.toBlob((blob) => {
        const imageURL = URL.createObjectURL(blob);
        downloadImage(imageURL);
      });
    }
  };



  const downloadImage = (imageURL) => {
    const link = document.createElement("a");
    link.href = imageURL;
    link.download = `captured_frame_${props.query}.png`;
    link.click();
  };

  return (
    <div>
      <TopBar logo={Logo} buttons={buttons} />
      <div id="main_results_div">
        <div className="logo_header"></div>
        <div className="results-wrapper">
          <div className="video-wrapper">
            <p>Query: {props.query}</p>
            <div className="video-container">
              <ReactPlayer
                ref={videoRef}
                url={URL.createObjectURL(props.video)}
                playing={playing}
                onSeek={handleSeek}
                onEnded={() => setPlaying(false)}
                controls
                width="100%"
                height="100%"
              />
            </div>
            <div className="jump-button-wrapper">
              <button
                className={`jump-button ${
                  props.numberList.length === 0 ? "disabled" : ""
                }`}
                onClick={handleJumpButtonClick}
                disabled={props.numberList.length === 0}
              >
                Jump to Next Result {currentIndex + 1} / {props.numberList.length}
              </button>
              <button className="download-button" onClick={handleCaptureFrame}>Download Frame</button>
              
            </div>
            <div className="next-query-wrapper"><button className="another-query-button" onClick={handleNextQuery}>Next query</button></div>
            
          </div>
          <div className="heat-map-wrapper">
            <HeatMap data={data} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default VideoPlayer;
