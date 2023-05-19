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
  const { videoFile: file, jumpPoints } = location.state;

  return (
    <VideoPlayer video={file} numberList={jumpPoints} />
  );
}

export default App;
