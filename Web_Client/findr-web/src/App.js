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
  const { videoFile: file, jumpPoints, processedResults, query} = location.state;
  return (
    <VideoPlayer video={file} numberList={jumpPoints} results={processedResults} query={query}/>
  );
}

export default App;

// import React from 'react';
// import TopBar from './topBar/topBar';
// import Logo from './only_logo.png';

// import React from 'react';
// import ParentComponent from './parent/parent';

// const App = () => {
//   return (
//     <div>
//       <h1>App Component</h1>
//       <ParentComponent />
//     </div>
//   );
// };

// export default App;











