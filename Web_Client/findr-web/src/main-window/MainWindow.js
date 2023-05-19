import React, { useState, useEffect } from 'react';
import Dropzone from 'react-dropzone';
import ReactPlayer from 'react-player';
import './main-window.css';
import axios from 'axios';
import Logo from '../only_logo.png';
import { useNavigate } from 'react-router-dom';
import Modal from 'react-modal';

function VideoUploader() {
  const [videoFile, setVideoFile] = useState(null);
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const [showModal, setShowModal] = useState(false);

  const handleQueryChange = (event) => {
    setQuery(event.target.value);
  };

  const handleCloseModal = () => {
    // Close the modal
    setShowModal(false);
  };

  const getResults = async () => {
    if (query.trim() === '') {
      // Show a popup or error message to prompt the user to enter a query
      setShowModal(true);
      return;
    }
    // Create a FormData object to send the file as a binary payload
    const formData = new FormData();
    formData.append('file', videoFile);
    try {
      console.log(query);
      const response = await axios.post('http://localhost:5002/uploadfile/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      const jumpPoints = [10, 20, 30];
  
      if (response.status === 200) {
        console.log('File uploaded successfully');
        navigate('/videoPlayer/', { state: { videoFile: videoFile, jumpPoints } });
      }
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  const handleDrop = async (acceptedFiles) => {
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
      <div className="logo_header">
      <img src={Logo} alt="Logo" className="logo" />
      </div>
      
      {!videoFile ? (
        <Dropzone onDrop={handleDrop}>
          {({ getRootProps, getInputProps }) => (
            <div id='video-drop-zone' {...getRootProps()} style={{ border: 'dashed 2px gray', display: 'flex', justifyContent: 'center', width: '80%', height: '200px'}}>
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

      <input id='query_bar' type="text" className="form-control" placeholder="Enter your query here" value={query} onChange={handleQueryChange}/>
      <button type="button" className="btn btn-custom get-results-button" onClick={getResults}>Find results</button>
      {showModal && (
        <div className="popup">
          <h2>Error</h2>
          <p>Please enter a query.</p>
          <button type="button" onClick={handleCloseModal}>Close</button>
        </div>
      )}
    </div>
  );
}

export default VideoUploader;
