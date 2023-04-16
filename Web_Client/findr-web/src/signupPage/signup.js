import React from 'react';
import './signup.css';
import RightDesign from '../right_design.png';
import LeftDesign from '../left_design.png';
import Logo from '../only_logo.png';

function Signup() {
  return (
    <div className="signup-container">
      <div className="logo-container left">
        <img src={LeftDesign} alt="logo" />
      </div>
      <div className="form-container">
      <div className="form-header">
            <h2>Create Account</h2>
        </div>
        <img src={Logo} alt="Image" />
        <form className="signup-form">
          <div className="form-row">
            <input type="text" placeholder="First Name" required />
          </div>
          <div className="form-row">
            <input type="text" placeholder="Last Name" required />
          </div>
          <div className="form-row">
            <input type="email" placeholder="Email Address" required />
          </div>
          <div className="form-row">
            <input type="password" placeholder="Password" required />
          </div>
          <div className="form-row">
            <input type="password" placeholder="Confirm Password" required />
          </div>
          <div className="form-row">
            <button type="submit">Sign Up</button>
          </div>
        </form>
      </div>
      <div className="logo-container right">
        <img src={RightDesign} alt="logo" />
      </div>
    </div>
  );
}

export default Signup;
