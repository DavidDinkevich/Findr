import './App.css';
import { BrowserRouter as Router,  Routes,Route } from 'react-router-dom';
import VideoUploader from './main-window/MainWindow';
import Login from './login-page/LoginPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<Login/>} />
        <Route path="/uploadVideo" element={<VideoUploader />} />
        <Route path="/contact" element={<>sdf</>} />
      </Routes>
    </Router>
  );
}

export default App;
