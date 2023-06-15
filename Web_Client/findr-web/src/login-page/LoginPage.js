import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Logo from '../only_logo.png';
import axios from 'axios';
import TopBar from '../topBar/topBar'
import './login-page.css';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

    const buttons = [
    {
      name: 'Login',
      route: '/',
    },
    {
      name: 'Sign up',
      route: '/signup',
    },
  ];

  //when user clicks submit, send authentication to BE and when response arrives go to main window
  const handleSubmit = async (e, username, password) => {
    e.preventDefault();
    try {
      const response = await axios.get(`http://localhost:5002/login?username=${username}&password=${password}`);
      console.log(response.data)
      // handle login logic here
      if (response.status === 200) {
        navigate('/uploadVideo');
      }
    } catch (error) {
      if (error.response.status === 401) {
        setErrorMessage('Invalid username or password');
      }
    }
  };


  return (
    <div>
      <TopBar logo={Logo} buttons={buttons} />
    <div className="container">
      <div className="sidebar">
      <h1>Introducing findR</h1>     
        <p>findR is a powerful tool that allows you to find the place in a video based on a text description of the content. Simply enter the text description of the frame you want to extract, and our app will analyze the video to find the corresponding frame.</p>
      </div>
    <div className="login-container">
      <form onSubmit={(e) => handleSubmit(e, username, password)}>
        <h2>Login</h2>
        <div className="form-row">
            <input
              type="Username"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="form-row">
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
        <p style={{ color: 'red', marginTop: '0.5rem' }}>{errorMessage}</p>
        <div className="button-container" id="myButtonContainer">
          <button type="submit" className="styled-button">Login</button>
          <button onClick={() => navigate('/signup')} className="styled-button">Sign up</button>
        </div>
      </form>
    </div>
    </div>
    </div>
  );
}

export default Login;
