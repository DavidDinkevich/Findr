import React, { useState, useEffect, useRef } from "react";
import './results.css';
import ReactPlayer from 'react-player';
import Logo from '../only_logo.png';

function VideoPlayer(props) {
  const videoRef = useRef(null);
  const [playing, setPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [currentIndex, setCurrentIndex] = useState(-1);
  const [frameCount, setFrameCount] = useState(0);
  const [length, setLength] = useState(0);
  const model = props.modelName;

  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.seekTo(currentTime);
    }
  }, [currentTime]);

  const handleReady = () => {
    if (videoRef.current) {
      const videoElement = videoRef.current.getInternalPlayer();
      const duration = videoElement.duration;
      const frameRate = videoElement.webkitDecodedFrameRate || 30; // Assuming a default frame rate of 30 if not available
      const frames = Math.floor(duration * frameRate);
      setFrameCount(frames);
      setLength(videoRef.current.getDuration());
      console.log("inside handle ready")
      console.log("video length",length);
    }
  };

  function frameToSecond(frame, numFrames, numSeconds) {
    return numSeconds * (frame / numFrames);
  }


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
      <h1> Algorithm results</h1>
        <div className="video-container">
          <ReactPlayer
            ref={videoRef}
            url={URL.createObjectURL(props.video)}
            playing={playing}
            onSeek={handleSeek}
            onReady={handleReady}
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