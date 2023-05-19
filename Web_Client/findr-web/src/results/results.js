import React, { useState,useEffect, useRef } from "react";
import './results.css';
import ReactPlayer from 'react-player';
import Logo from '../only_logo.png';

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
        <div id='main_div'>
          <div className="logo_header">
            <img src={Logo} alt="Logo" className="logo" />
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '420px', marginTop: '20px' }}>
            <div style={{ display: 'grid', placeItems: 'center', width: '80%', aspectRatio: '16/9', backgroundColor: 'black' }}>
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
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: '10px' }}>
              {props.numberList.map((number, index) => (
                <button key={index} onClick={() => handleJumpButtonClick(number)}>
                  Jump to {number}
                </button>
              ))}
            </div>
          </div>
        </div>
      );
      
      
      
  }
  
export default VideoPlayer;
  

