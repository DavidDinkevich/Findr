import React, { useState, useEffect, useRef } from "react";
import './results.css';
import ReactPlayer from 'react-player';
import Logo from '../only_logo.png';

function VideoPlayer(props) {
  const videoRef = useRef(null);
  const [playing, setPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [currentIndex, setCurrentIndex] = useState(-1);
  const model = props.modelName;

  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.seekTo(currentTime);
    }
  }, [currentTime]);


  const handleJumpButtonClick = () => {
    if (currentIndex < props.numberList.length) {
      const nextIndex = currentIndex + 1;
      const nextNumber = props.numberList[nextIndex];
      setCurrentIndex(nextIndex);
      setCurrentTime(nextNumber);
      setPlaying(false);
    }
  };

  const handleSeek = (seconds) => {
    setCurrentTime(seconds);
  };


  return (
    <div id='main_div'>
      <div className="logo_header">
        <img src={Logo} alt="Logo" className="logo" />
      </div>
      
      <div className="video-wrapper">
      <h1> Presenting {model} results</h1>
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
          <button className="jump-button" onClick={handleJumpButtonClick}>
            Jump to Next Number
          </button>
        </div>
      </div>
    </div>
  );
}

export default VideoPlayer;