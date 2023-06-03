import './App.css';
import { BrowserRouter as Router,  Routes,Route , useLocation} from 'react-router-dom';
import VideoUploader from './main-window/MainWindow';
import Login from './login-page/LoginPage';
import SignupPage from './signupPage/signup';
import VideoPlayer from './results/results';
import ResultsProcessor from './results-processor/resultsProcessor'


function App() {

  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<Login/>} />
        <Route path="/uploadVideo" element={<VideoUploader />} />
        <Route path="/signup" element={<SignupPage/>} />
        {/* <Route path="/results" element={<SignupPage/>} /> */}
        <Route path="/videoPlayer" element={<VideoPlayerWrapper />} />
        <Route path="/resultsProcessor" element={<ResultsProcessorWrapper />} />
      </Routes>
    </Router>
  );
}
function ResultsProcessorWrapper() {
  const location = useLocation();
  const { videoFile: file, response} = location.state;
  return (
    <VideoPlayer video={file} results={response}/>
  );
}
function VideoPlayerWrapper() {
  const location = useLocation();
  const { videoFile: file, jumpPoints, model} = location.state;
  return (
    <VideoPlayer video={file} numberList={jumpPoints} modelName={model}/>
  );
}

export default App;
