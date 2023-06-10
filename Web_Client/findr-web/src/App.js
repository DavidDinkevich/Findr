import './App.css';
import { BrowserRouter as Router,  Routes,Route , useLocation} from 'react-router-dom';
import VideoUploader from './main-window/MainWindow';
import Login from './login-page/LoginPage';
import SignupPage from './signupPage/signup';
import VideoPlayer from './results/results';


function App() {

  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<Login/>} />
        <Route path="/uploadVideo" element={<VideoUploader />} />
        <Route path="/signup" element={<SignupPage/>} />
        <Route path="/videoPlayer" element={<VideoPlayerWrapper />} />
      </Routes>
    </Router>
  );
}

function VideoPlayerWrapper() {
  const location = useLocation();
  const { videoFile: file, jumpPoints, processedResults} = location.state;
  return (
    <VideoPlayer video={file} numberList={jumpPoints} results={processedResults}/>
  );
}

export default App;




// import React from 'react';
// import HeatMap from './heatMap/heatMap';

// const App = () => {
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

//   return <HeatMap data={data} />;
// };

// export default App;


