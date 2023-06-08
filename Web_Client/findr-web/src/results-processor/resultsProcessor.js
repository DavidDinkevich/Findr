import React, { useState, useEffect, useRef } from "react";
import './results-processor.css';
import ReactPlayer from 'react-player';
import Logo from '../only_logo.png';

function ResultsProcessor(props) {

    const handleButtonClick = () => {
      console.log(props);
      console.log(props.video.duration)
    };
  
    return (
      <div id='main_div'>
        <div className="logo_header">
          <img src={Logo} alt="Logo" className="logo" />
        </div>
        <div className="jump-button-wrapper">
          <button className="jump-button" onClick={handleButtonClick}>
            Jump to Next Number
          </button>
        </div>
      </div>
    );
  }
  
  export default ResultsProcessor;