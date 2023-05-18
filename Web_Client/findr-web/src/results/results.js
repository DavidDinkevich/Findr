import React, { useState,useEffect, useRef } from "react";
import './results.css';
import ReactPlayer from 'react-player';

function VideoPlayer(props) {
    const videoRef = useRef(null);
    const [playing, setPlaying] = useState(false);
    const [currentTime, setCurrentTime] = useState(0);
  
    useEffect(() => {
      if (videoRef.current) {
        videoRef.current.seekTo(currentTime);
      }
    }, [currentTime]);
  
    const handleJumpButtonClick = (time) => {
      setCurrentTime(time);
      setPlaying(true);
    };
  
  
    const handleSeek = (seconds) => {
      setCurrentTime(seconds);
    };
  
    return (
      <div>
        <ReactPlayer
          ref={videoRef}
          url={URL.createObjectURL(props.video)}
          playing={playing}
          onSeek={handleSeek}
          onEnded={() => setPlaying(false)}
          controls
        />
        <div>
          {props.numberList.map((number, index) => (
            <button key={index} onClick={() => handleJumpButtonClick(number)}>
              Jump to {number}
            </button>
          ))}
        </div>
      </div>
    );
  }
  
export default VideoPlayer;
  

