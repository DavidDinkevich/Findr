import './App.css';
import { BrowserRouter as Router,  Routes,Route } from 'react-router-dom';
import VideoUploader from './main-window/MainWindow';
import Login from './login-page/LoginPage';
import SignupPage from './signupPage/signup';
import UserList from './test/test';

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<Login/>} />
        <Route path="/uploadVideo" element={<VideoUploader />} />
        <Route path="/signup" element={<SignupPage/>} />
        <Route path="/test" element={<UserList/>} />
      </Routes>
    </Router>
  );
}

export default App;
