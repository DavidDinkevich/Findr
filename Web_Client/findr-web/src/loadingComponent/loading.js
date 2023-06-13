import React from 'react';
import './loading.css'; // Import CSS file for styling (optional)

const LoadingSpinner = ({ show, message }) => {
    if (!show) {
      return null; // Don't render anything if show is false
    }
  
    return (
      <div className="loading-overlay">
        <div className="loading-content">
          <div className="loading-spinner"></div>
          <p >{message}</p>
        </div>
      </div>
    );
  };
  
  export default LoadingSpinner;