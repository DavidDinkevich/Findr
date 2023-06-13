import React, { useState, useEffect, useRef } from "react";
import './results.css';
import ReactPlayer from 'react-player';
import Logo from '../only_logo.png';
import TopBar from '../topBar/topBar'
import HeatMap from '../heatMap/heatMap';

function VideoPlayer(props) {
  const videoRef = useRef(null);
  const [playing, setPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [currentIndex, setCurrentIndex] = useState(-1);
  const data = JSON.parse(props.results.replace(/'/g, '"'))
  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.seekTo(currentTime);
    }
  }, [currentTime]);

  const handleReady = () => {
    const data_try = JSON.parse(props.results.replace(/'/g, '"'))
    console.log(data_try)
  };

  const buttons = [
    {
      name: 'Sign out',
      route: '/',
    },
    {
      name: 'Sign up',
      route: '/signup',
    },
  ];

  


  const handleJumpButtonClick = () => {
    const lastIndex = props.numberList.length - 1;
    if (currentIndex < lastIndex) {
      const nextIndex = currentIndex + 1;
      const nextNumber = props.numberList[nextIndex];
      setCurrentIndex(nextIndex);
      if (typeof nextNumber === 'number' && isFinite(nextNumber)) {
        setCurrentTime(nextNumber);
      }
      setPlaying(false);
    } else {
      setCurrentIndex(0);
      setCurrentTime(props.numberList[0]);
      setPlaying(false);
    }
  };

  const handleSeek = (seconds) => {
    setCurrentTime(seconds);
  };


  return (
    <div>
      <TopBar logo={Logo} buttons={buttons} />
    <div id='main_div'>
      
      <div className="logo_header">
      
      </div>
      <div className="results-wrapper">
      <div className="video-wrapper">
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
      <div className="heat-map-wrapper">
      <HeatMap data={data} />
      </div>
      </div>
    </div>
    </div>
  );
}

export default VideoPlayer;