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
        <Route path="/results" element={<VideoPlayerWrapper />} />
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

// import React, { useState } from 'react';
// import LoadingSpinner from './loadingComponent/loading';

// const App = () => {
//   const [isLoading, setIsLoading] = useState(false);

//   const fetchData = () => {
//     setIsLoading(true);
//     // Simulate an asynchronous operation
//     setTimeout(() => {
//       setIsLoading(false);
//     }, 2000);
//   };

//   return (
//     <div>
//       <h1>Welcome to My App</h1>
//       <button onClick={fetchData}>Fetch Data</button>
//       <LoadingSpinner show={isLoading} message="Please wait while we process your request..." />
//     </div>
//   );
// };

// export default App;








