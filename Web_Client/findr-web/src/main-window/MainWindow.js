// export function MainWindow() {


//     return (<>


//     </>);
// }


import React, { useState, useEffect } from 'react';
import Dropzone from 'react-dropzone';
import ReactPlayer from 'react-player';
import './main-window.css';

function VideoUploader() {
  const [videoFile, setVideoFile] = useState(null);

  const handleDrop = (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file.type.startsWith('video/')) {
      setVideoFile(file);
    } else {
      console.log('Please upload a video file.');
    }
  };

  const button_uploadNewVideo = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'video/*,image/*';
    input.onchange = (event) => {
      setVideoFile(event.target.files[0]);
    };
    input.click();
  }

  return (
    <div id='main_div'>
      <label id='logo'>Findr</label>
      {!videoFile ? (
        <Dropzone onDrop={handleDrop}>
          {({ getRootProps, getInputProps }) => (
            <div id='video-drop-zone' {...getRootProps()} style={{ border: 'dashed 2px gray', display: 'flex', justifyContent: 'center', width: '80%', height: '200px' }}>
              <input {...getInputProps()} accept="video/*" />
              <p style={{ margin: 'auto' }}>Drag and drop a video or image file here.</p>
            </div>
          )}
        </Dropzone>)
        : <div>
            <ReactPlayer url={URL.createObjectURL(videoFile)} style={{margin:'auto'}} controls width="80%" height="400px" />
            <button type="button" className="btn btn-light main-window-button" onClick={button_uploadNewVideo}>Choose a different video</button>
          </div>
      }

      <input id='query_bar' type="text" className="form-control" placeholder="Enter your query here" />

    </div>
  );
}

export default VideoUploader;
