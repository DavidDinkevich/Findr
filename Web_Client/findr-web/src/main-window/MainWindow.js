import React, { useState,useRef } from 'react';
import Dropzone from 'react-dropzone';
import ReactPlayer from 'react-player';
import './main-window.css';
import axios from 'axios';
import Logo from '../only_logo.png';
import Upload from '../upload.png'
import LoadingSpinner from '../loadingComponent/loading';
import { useNavigate } from 'react-router-dom';
import TopBar from '../topBar/topBar'

function VideoUploader() {
  const videoRef = useRef(null);
  const [videoFile, setVideoFile] = useState("");
  const navigate = useNavigate();
  let query = ""
  const [errorMessage, setErrorMessage] = useState('');
  const [checkboxValues, setCheckboxValues] = useState({
    clip: false,
    resnet: false,
    inceptionv3: false,
    yolov5: false,
    efficientnet: false
  });
  const [showModal, setShowModal] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

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

  const handleQueryChange = (event) => {
    // event.preventDefault()
    // setQuery(event.target.value);
    query = event.target.value;
  };

  function generateStringFromCheckboxValues(checkboxValues) {
    const clip_cb = document.getElementById('clip_checkbox');
    const yolov5_cb = document.getElementById('yolov5_checkbox');
    const resnet_cb = document.getElementById('resnet_checkbox');
    const inceptionv3_cb = document.getElementById('inceptionv3_checkbox');
    const efficientnet_cb = document.getElementById('efficientnet_checkbox');

    let models = []
    if (clip_cb.checked) { models.push('clip') }
    if (yolov5_cb.checked) { models.push('yolov5') }
    if (resnet_cb.checked) { models.push('resnet') }
    if (inceptionv3_cb.checked) { models.push('inceptionv3') }
    if (efficientnet_cb.checked) { models.push('efficientnet') }

    console.log(`Sending this string: ${models.join(", ")}`)

    return models.join(", ");
    // const trueValues = Object.entries(checkboxValues)
    //   .filter(([key, value]) => value === true)
    //   .map(([key, value]) => key);
  
    // // Add 'clip' if the list is empty
    // if (trueValues.length === 0) {
    //   trueValues.push('clip');
    // }
    
    // return trueValues.join(", ");
  }

  const handleCheckboxChange = (event) => {
    event.preventDefault()
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
    //Error handling
    if (!videoFile) {
      setErrorMessage('Please upload a video.');
      setShowModal(true);
      return;
    }

    query = document.getElementById('query_bar').value
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
      setIsLoading(true);
      const response = await axios.post(`http://localhost:5002/uploadfile/${query}/${generateStringFromCheckboxValues(checkboxValues)}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setIsLoading(false);
      const parts = response.data.split('&')
      const jumpPoints = JSON.parse(parts[0]).map(Number)
      const processedResults = parts[1]
      if (response.status === 200) {
        console.log('File uploaded successfully');
        console.log(response.data)
        navigate('/results/', { state: { videoFile: videoFile, jumpPoints, processedResults,query} });
      }
    } catch (error) {
      setIsLoading(false);
      setErrorMessage('Network error');
      setShowModal(true);
      console.error('Error uploading file:', error);
    }
  };

  const handleDrop = async (acceptedFiles) => {
    const file = acceptedFiles[0];
    //input validation
    if (file.type.startsWith('video/')) {
      setVideoFile(file);
      
    } else {
      setErrorMessage('Please upload a video format file.');
      setShowModal(true);
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
  const backroundColor = 'rgb(0, 0, 0)';
  return (
    <div >
      <TopBar logo={Logo} buttons={buttons} />
    <div id='main_div'>     
      <div className="container-div">
      <div className="content-wrapper">
        <div className="video-section">
          {!videoFile ? (
            <Dropzone onDrop={handleDrop}>
              {({ getRootProps, getInputProps }) => (
                <div className='video-drop-zone' {...getRootProps()}>
                  <input {...getInputProps()} accept="video/*" />
                  <p>Upload your video</p>
                  <img src={Upload} alt="upload_icon" className="upload_icon" />
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
              <button type="button" className="btn change-video-button" onClick={button_uploadNewVideo}>
                Choose a different video
              </button>
            </div>
          )}
        </div>
  
        <div className="query-section">
          <input id='query_bar' type="text" className="form-control" placeholder="Enter your query here" />
          <button type="button" className="get-results-button" onClick={getResults}>Find results</button>
        </div>
  

      </div>
      <div className="checkbox-section">
        <p>Choose which AI models to run (hover above for explanations):</p>
          <table>
            <tbody>
            <tr>
              <td>
                <label class="checkbox-container" title="CLIP (Contrastive Language-Image Pretraining) is an AI model that learns to understand images and their corresponding textual descriptions. It is trained on a large dataset of image-text pairs to associate visual and textual representations. This allows CLIP to perform various tasks such as image classification, object detection, and generating textual descriptions for images.">
                  <input id="clip_checkbox" type="checkbox" name="clip" 
                  // checked={checkboxValues.clip}
                  />
                  <span class="checkmark"></span>
                  CLIP
                </label>
              </td>
            </tr>
                 <tr>
                <td>
                <label class="checkbox-container" title="ResNet (Residual Neural Network) is an AI model architecture that revolutionized image classification tasks. It introduces the concept of residual connections, allowing the model to effectively train very deep neural networks. ResNet's key innovation is the use of skip connections that bypass certain layers, enabling the network to learn residual functions. This helps to address the problem of vanishing gradients and enables successful training of deep networks. With its deep architecture, ResNet can learn intricate features and representations, leading to improved accuracy in image classification tasks.">
                    <input
                      id="resnet_checkbox"
                      type="checkbox"
                      name="resnet"
                      // checked={checkboxValues.resnet}
                    />
                    <span class="checkmark"></span>
                    ResNet
                  </label>
                </td>
              </tr>
               <tr>
                <td>
                <label class="checkbox-container" title="InceptionV3 is an AI model architecture that excels in image recognition and classification tasks. It utilizes a deep convolutional neural network with multiple layers, including inception modules. Inception modules employ various filter sizes to capture different scales of features in parallel, enabling the model to capture both local and global information. InceptionV3 reduces the number of parameters and computational complexity by using 1x1 convolutions to perform dimensionality reduction. This architecture allows InceptionV3 to achieve high accuracy in image classification tasks while maintaining efficiency.">
                    <input
                      id="inceptionv3_checkbox"
                      type="checkbox"
                      name="inceptionv3"
                      // checked={checkboxValues.inceptionv3}
                    />
                    <span class="checkmark"></span>
                    Inceptionv3
                  </label>
                </td>
              </tr>
              <tr>
                <td>
                <label class="checkbox-container" title="YOLOv5 (You Only Look Once) is an AI model architecture specifically designed for real-time object detection. It utilizes a single neural network to simultaneously predict bounding boxes and class probabilities for objects within an image. YOLOv5 achieves this by dividing the image into a grid and associating each grid cell with multiple anchor boxes. The model then predicts the bounding box coordinates and class probabilities for each anchor box. YOLOv5 employs a backbone network (such as CSPDarknet53 or EfficientNet) for feature extraction and applies additional convolutional layers for detection. YOLOv5 is known for its speed and accuracy, making it well-suited for applications that require real-time object detection.">
                    <input
                      id="yolov5_checkbox"
                      type="checkbox"
                      name="yolov5"
                      // checked={checkboxValues.yolov5}
                      // onChange={handleCheckboxChange}
                    />
                    <span class="checkmark"></span>
                    YOLOv5
                  </label>
                </td>
              </tr>
              <tr>
                <td>
                <label class="checkbox-container" title="EfficientNet is an AI model architecture that achieves high accuracy while maintaining efficiency by using a compound scaling method. It scales the depth, width, and resolution of the model in a balanced manner to optimize performance. EfficientNet employs a mobile inverted bottleneck convolutional (MBConv) block, which consists of depth-wise convolutions, point-wise convolutions, and skip connections. This block reduces computational complexity while capturing complex patterns and features. EfficientNet achieves state-of-the-art performance on various image classification tasks with fewer parameters and computations compared to other models.">
                    <input
                      id="efficientnet_checkbox"
                      type="checkbox"
                      name="efficientnet"
                      // checked={checkboxValues.efficientnet}
                      // onChange={handleCheckboxChange}
                    />
                    <span class="checkmark"></span>
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
          <h2 style={{ color: backroundColor, fontSize: '32px' }}>Error</h2>
          <p style={{ color: backroundColor, fontSize: '20px' }}>{errorMessage}</p>
          <button type="button" onClick={handleCloseModal}>Close</button>
        </div>
      )}
      <LoadingSpinner show={isLoading} message="Please wait while we process your request..." />
    </div>
    </div>
  );
  
  
}

export default VideoUploader;
