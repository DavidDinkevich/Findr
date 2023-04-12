import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Logo from '../only_logo.png';
import './login-page.css';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    // handle login logic here
    if (username === 'cor' && password === 'cor') {
      navigate('/uploadVideo');
    }
    else {
      setErrorMessage('Invalid username or password');
    }
  };


  return (
    <div className="container">
      <img src={Logo} alt="Logo" className="logo" />
      <div className="sidebar">
      <h1>Introducing findR</h1>     
        <p>findR is a powerful tool that allows you to extract frames from a video based on a text description of the content. Simply enter the text description of the frame you want to extract, and our app will analyze the video to find the corresponding frame.</p>
      </div>
    <div className="login-container">

      <form onSubmit={handleSubmit}>
        <h2>Login</h2>
        <label>
          Username:
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </label>
        <label>
          Password:
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>
        <p style={{ color: 'red', marginTop: '0.5rem' }}>{errorMessage}</p>
        <div className="button-container">
          <button type="submit">Submit</button>
          <button onClick={() => navigate('/signup')}>Sign up</button>
        </div>
      </form>
    </div>
    </div>
  );
}

export default Login;
