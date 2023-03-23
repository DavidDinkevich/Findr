// export function MainWindow() {


//     return (<>
        
    
//     </>);
// }


import React, { useState } from 'react';
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

  return (
    <div id='main_div'>
      <label id='logo'>Findr</label>
      <Dropzone onDrop={handleDrop}>
        {({ getRootProps, getInputProps }) => (
          <div id='video-drop-zone' {...getRootProps()} style={{ border: 'dashed 2px gray', display: 'flex', justifyContent: 'center', width: '80%', height: '200px' }}>
            <input {...getInputProps()} accept="video/*" />
            <p style={{margin: 'auto'}}>Drag and drop a video or image file here.</p>
          </div>
        )}
      </Dropzone>
      {videoFile && (
        <div>
          <ReactPlayer url={URL.createObjectURL(videoFile)} controls width="100%" height="auto" />
        </div>
      )}
      <input id='query_bar' type="text" class="form-control" placeholder="Enter your query here"/>

    </div>
  );
}

export default VideoUploader;
