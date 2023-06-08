import React, { useState,useRef } from 'react';
import Dropzone from 'react-dropzone';
import ReactPlayer from 'react-player';
import './main-window.css';
import axios from 'axios';
import Logo from '../only_logo.png';
import { useNavigate } from 'react-router-dom';

function VideoUploader() {
  const videoRef = useRef(null);
  const [videoFile, setVideoFile] = useState(null);
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
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
  
    // Add 'clip' if the list is empty
    if (trueValues.length === 0) {
      trueValues.push('clip');
    }
    
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

  function getFirstIntervalValues(data) {
    const result = [];
    const jsonData = JSON.stringify(data)
    console.log(typeof jsonData)
    for (const model of Object.values(jsonData)) {
      console.log("went in",model,"bla")
      if (Array.isArray(model)) {
        
        for (const item of model) {
          if (item.hasOwnProperty('interval') && Array.isArray(item.interval) && item.interval.length > 0) {
            result.push(item.interval[0]);
          }
        }
      }
    }
  
    return result;
  }
  
  
  

  const getResults = async () => {
    if (!videoFile) {
      setErrorMessage('Please upload a video.');
      setShowModal(true);
      return;
    }
    if (query.trim() === '') {
      setErrorMessage('Please enter a query.');
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
      //const jumpPoints = [2, 4, 6];   
      const model = 'clip'
      const parts = response.data.split('&')
      console.log("parts zero",typeof parts[0],parts[0])
      const jumpPoints = JSON.parse(parts[0]).map(Number)
      console.log("parts zero",typeof jumpPoints,jumpPoints)
      console.log("second",parts[1])
      if (response.status === 200) {
        console.log('File uploaded successfully');
        navigate('/videoPlayer/', { state: { videoFile: videoFile, jumpPoints, model} });
        // const results = response.data
        // console.log('hi')
        // console.log(results);
        // navigate('/resultsProcessor/', { state: { videoFile: videoFile, results:results} });
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
                ref={videoRef}
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
                  <label title="CLIP (Contrastive Language-Image Pretraining) is an AI model that learns to understand images and their corresponding textual descriptions. It is trained on a large dataset of image-text pairs to associate visual and textual representations. This allows CLIP to perform various tasks such as image classification, object detection, and generating textual descriptions for images.">
                    <input
                      type="checkbox"
                      name="clip"
                      checked={checkboxValues.clip}
                      onChange={handleCheckboxChange}
                    />
                    CLIP
                  </label>
                </td>
                </tr>
                <tr>
                <td>
                <label title="ResNet (Residual Neural Network) is an AI model architecture that revolutionized image classification tasks. It introduces the concept of residual connections, allowing the model to effectively train very deep neural networks. ResNet's key innovation is the use of skip connections that bypass certain layers, enabling the network to learn residual functions. This helps to address the problem of vanishing gradients and enables successful training of deep networks. With its deep architecture, ResNet can learn intricate features and representations, leading to improved accuracy in image classification tasks.">
                    <input
                      type="checkbox"
                      name="resnet"
                      checked={checkboxValues.resnet}
                      onChange={handleCheckboxChange}
                    />
                    ResNet
                  </label>
                </td>
              </tr>
                <tr>
                <td>
                <label title="InceptionV3 is an AI model architecture that excels in image recognition and classification tasks. It utilizes a deep convolutional neural network with multiple layers, including inception modules. Inception modules employ various filter sizes to capture different scales of features in parallel, enabling the model to capture both local and global information. InceptionV3 reduces the number of parameters and computational complexity by using 1x1 convolutions to perform dimensionality reduction. This architecture allows InceptionV3 to achieve high accuracy in image classification tasks while maintaining efficiency.">
                    <input
                      type="checkbox"
                      name="inceptionv3"
                      checked={checkboxValues.inceptionv3}
                      onChange={handleCheckboxChange}
                    />
                    Inceptionv3
                  </label>
                </td>
              </tr>
              <tr>
                <td>
                <label title="YOLOv5 (You Only Look Once) is an AI model architecture specifically designed for real-time object detection. It utilizes a single neural network to simultaneously predict bounding boxes and class probabilities for objects within an image. YOLOv5 achieves this by dividing the image into a grid and associating each grid cell with multiple anchor boxes. The model then predicts the bounding box coordinates and class probabilities for each anchor box. YOLOv5 employs a backbone network (such as CSPDarknet53 or EfficientNet) for feature extraction and applies additional convolutional layers for detection. YOLOv5 is known for its speed and accuracy, making it well-suited for applications that require real-time object detection.">
                    <input
                      type="checkbox"
                      name="yolov5"
                      checked={checkboxValues.yolov5}
                      onChange={handleCheckboxChange}
                    />
                    YOLOv5
                  </label>
                </td>
              </tr>
              <tr>
                <td>
                <label title="EfficientNet is an AI model architecture that achieves high accuracy while maintaining efficiency by using a compound scaling method. It scales the depth, width, and resolution of the model in a balanced manner to optimize performance. EfficientNet employs a mobile inverted bottleneck convolutional (MBConv) block, which consists of depth-wise convolutions, point-wise convolutions, and skip connections. This block reduces computational complexity while capturing complex patterns and features. EfficientNet achieves state-of-the-art performance on various image classification tasks with fewer parameters and computations compared to other models.">
                    <input
                      type="checkbox"
                      name="efficientnet"
                      checked={checkboxValues.efficientnet}
                      onChange={handleCheckboxChange}
                    />
                    EfficientNet
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
          <p>{errorMessage}</p>
          <button type="button" onClick={handleCloseModal}>Close</button>
        </div>
      )}
    </div>
  );
  
  
}

export default VideoUploader;
