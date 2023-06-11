import React, { useState } from 'react';
import axios from 'axios';
import TopBar from '../topBar/topBar'
import Logo from '../only_logo.png';
import PersonPhoto from '../cute_findr_person.png';
import './signup.css';



function Signup() {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const buttons = [
    {
      name: 'Login',
      route: '/',
    },
    {
      name: 'Signup',
      route: '/signup',
    },
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setErrorMessage('Passwords do not match');
      return;
    }
    try {
      const response = await axios.post(`http://localhost:5002/users?full_name=${fullName}&username=${username}&password=${password}&email=${email}`)
   
      console.log(response.data);
      if (response.status === 200) {
        // Redirect to login page
        window.location.href = '/';
      }
    } catch (error) {
      console.error(error);
      setErrorMessage('Error creating account');
    }
  };

  return (
<div>
<TopBar logo={Logo} buttons={buttons} />
    <div className="signup-container">

      <div className="form-container">
        <div className="form-header">
          <h2>Welcome to findR!</h2>
        </div>
        <form className="signup-form" onSubmit={handleSubmit}>
          <div className="form-row">
            <input
              type="text"
              placeholder="Full Name"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              required
            />
          </div>

          <div className="form-row">
            <input
              type="email"
              placeholder="Email Address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
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
          <div className="form-row">
            <input
              type="password"
              placeholder="Confirm Password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>
          {errorMessage && <p style={{ color: 'black' }}>{errorMessage}</p>}
          <div className="form-row">
            <button type="submit" >Sign Up</button>
          </div>
        </form>
      </div>
      <div className="image-container">
          <img src={PersonPhoto} alt="cute_person" className="image" />
        </div>
    </div>
    </div>
  );
}

export default Signup;
