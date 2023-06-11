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

// import React from 'react';
// import TopBar from './topBar/topBar';
// import Logo from './only_logo.png';

// const App = () => {

//   const buttons = [
//     {
//       name: 'Button 1',
//       route: '/route1',
//     },
//     {
//       name: 'Button 2',
//       route: '/route2',
//     },
//   ];

//   return (
//     <div>
//       <TopBar logo={Logo} buttons={buttons} />
//       {/* Rest of your application */}
//     </div>
//   );
// };

// export default App;










