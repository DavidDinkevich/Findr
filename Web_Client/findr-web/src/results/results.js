import React, { useState, useEffect, useRef } from "react";
import './results.css';
import ReactPlayer from 'react-player';
import Logo from '../only_logo.png';
import HeatMap from '../heatMap/heatMap';

function VideoPlayer(props) {
  const videoRef = useRef(null);
  const [playing, setPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [currentIndex, setCurrentIndex] = useState(-1);
//   const data = {
//     'efficientnet': {
//         'intervals': [[0, 155], [264, 458], [459, 481]],
//         'accuracies': ['30', '94.15', '94.29'],
//         'num_frames': 482
//     },
//     'resnet': {
//         'intervals': [[0, 155], [264, 458], [459, 481]],
//         'accuracies': ['99.88', '88.52', '99.86'],
//         'num_frames': 482
//     },
//     'inceptionv3': {
//         'intervals': [[0, 155], [264, 458], [459, 481]],
//         'accuracies': ['100.00', '100.00', '99.99'],
//         'num_frames': 482
//     },
//     'yolov5': {
//         'intervals': [],
//         'accuracies': [],
//         'num_frames': 482
//     },
//     'clip': {
//         'intervals': [[0, 155], [156, 263], [264, 481]],
//         'accuracies': [93, 69, 87],
//         'num_frames': 482
//     }
// };
  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.seekTo(currentTime);
    }
  }, [currentTime]);

  const handleReady = () => {
    console.log('hi')
    //console.log("data",typeof data, data)
    const data_try = JSON.parse(props.results.replace(/'/g, '"'))
    console.log("results",typeof data_try, data_try)
    console.log('hi')
  };

  const data = JSON.parse(props.results.replace(/'/g, '"'))


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
      <div>
      <HeatMap data={data} />
      </div>
    </div>
  );
}

export default VideoPlayer;