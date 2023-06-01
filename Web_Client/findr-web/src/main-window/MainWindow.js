import React, { useState } from 'react';
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
  const [checkboxValues, setCheckboxValues] = useState({
    clip: false,
    resnet: false,
    inceptionv3: false,
    yolov5: false,
    efficientnet: false
  });
  const [showModal, setShowModal] = useState(false);

  const handleQueryChange = (event) => {
    setQuery(event.target.value);
  };

  function generateStringFromCheckboxValues(checkboxValues) {
    const trueValues = Object.entries(checkboxValues)
      .filter(([key, value]) => value === true)
      .map(([key, value]) => key);
    
    return trueValues.join(", ");
  }

  const handleCheckboxChange = (event) => {
    const { name, checked } = event.target;
    setCheckboxValues((prevValues) => ({
      ...prevValues,
      [name]: checked
    }));
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
      console.log(checkboxValues);
      const response = await axios.post(`http://localhost:5002/uploadfile/${query}/${generateStringFromCheckboxValues(checkboxValues)}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      const jumpPoints = [10, 20, 30];
      console.log(response.data);
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
  };

  return (
    <div id='main_div'>
      <div className="logo_header">
        <img src={Logo} alt="Logo" className="logo" />
      </div>
      <div className="container-div">
      <div className="content-wrapper">
        <div className="video-section">
          {!videoFile ? (
            <Dropzone onDrop={handleDrop}>
              {({ getRootProps, getInputProps }) => (
                <div className='video-drop-zone' {...getRootProps()}>
                  <input {...getInputProps()} accept="video/*" />
                  <p>Upload your video</p>
                </div>
              )}
            </Dropzone>
          ) : (
            <div className="video-player-wrapper">
              <ReactPlayer
                url={URL.createObjectURL(videoFile)}
                className="video-player"
                controls
                width="100%"
                height="auto"
              />
              <button type="button" className="btn btn-light main-window-button" onClick={button_uploadNewVideo}>
                Choose a different video
              </button>
            </div>
          )}
        </div>
  
        <div className="query-section">
          <input id='query_bar' type="text" className="form-control" placeholder="Enter your query here" value={query} onChange={handleQueryChange}/>
          <button type="button" className="btn btn-custom get-results-button" onClick={getResults}>Find results</button>
        </div>
  

      </div>
      <div className="checkbox-section">
        <h7>Choose which algorithms we should run for you(hover above for explanations):</h7>
          <table>
            <tbody>
              <tr>
                <td>
                  <label>
                    <input
                      type="checkbox"
                      name="clip"
                      checked={checkboxValues.clip}
                      onChange={handleCheckboxChange}
                    />
                    clip
                  </label>
                </td>
                </tr>
                <tr>
                <td>
                <label>
                    <input
                      type="checkbox"
                      name="resnet"
                      checked={checkboxValues.resnet}
                      onChange={handleCheckboxChange}
                    />
                    resnet
                  </label>
                </td>
              </tr>
                <tr>
                <td>
                <label>
                    <input
                      type="checkbox"
                      name="inceptionv3"
                      checked={checkboxValues.inceptionv3}
                      onChange={handleCheckboxChange}
                    />
                    inceptionv3
                  </label>
                </td>
              </tr>
              <tr>
                <td>
                <label>
                    <input
                      type="checkbox"
                      name="yolov5"
                      checked={checkboxValues.yolov5}
                      onChange={handleCheckboxChange}
                    />
                    yolov5
                  </label>
                </td>
              </tr>
              <tr>
                <td>
                <label>
                    <input
                      type="checkbox"
                      name="efficientnet"
                      checked={checkboxValues.efficientnet}
                      onChange={handleCheckboxChange}
                    />
                    efficientnet
                  </label>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        </div>
  
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
