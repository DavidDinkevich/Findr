// import './App.css';
// import { BrowserRouter as Router,  Routes,Route , useLocation} from 'react-router-dom';
// import VideoUploader from './main-window/MainWindow';
// import Login from './login-page/LoginPage';
// import SignupPage from './signupPage/signup';
// import VideoPlayer from './results/results';
// import ResultsProcessor from './results-processor/resultsProcessor'


// function App() {

//   return (
//     <Router>
//       <Routes>
//         <Route exact path="/" element={<Login/>} />
//         <Route path="/uploadVideo" element={<VideoUploader />} />
//         <Route path="/signup" element={<SignupPage/>} />
//         {/* <Route path="/results" element={<SignupPage/>} /> */}
//         <Route path="/videoPlayer" element={<VideoPlayerWrapper />} />
//         <Route path="/resultsProcessor" element={<ResultsProcessorWrapper />} />
//       </Routes>
//     </Router>
//   );
// }
// function ResultsProcessorWrapper() {
//   const location = useLocation();
//   const { videoFile: file, results } = location.state;

//   return (
//     <ResultsProcessor video={file} results={results} />
//   );
// }
// function VideoPlayerWrapper() {
//   const location = useLocation();
//   const { videoFile: file, jumpPoints, model} = location.state;
//   return (
//     <VideoPlayer video={file} numberList={jumpPoints} modelName={model}/>
//   );
// }

// export default App;

import React from 'react';
import BarChart from './barChart/barChart';

const App = () => {
  const modelName = 'Model A';
  const intervals = [[0, 3], [4, 5], [6, 9]];
  const accuracies = [98, 45.5, 80];
  const numFrames = 10;
  const barColor = 'blue'; // Specify the desired color here

  return (
    <div>
      <BarChart
        modelName={modelName}
        intervals={intervals}
        accuracies={accuracies}
        numFrames={numFrames}
        color={barColor}
      />
    </div>
  );
};

export default App;


