import React from 'react';
import PropTypes from 'prop-types';
import './top-bar.css'; // CSS file for styling

const TopBar = ({ logo, buttons }) => {
  return (
    <div className="top-bar">
      <div className="bar-content">
        <img src={logo} alt="Logo" className="logo" />

        <div className="button-container">
          {buttons.map((button, index) => (
            <a href={button.route} key={index} className="button">
              {button.name}
            </a>
          ))}
        </div>
      </div>

      <div className="line" />
    </div>
  );
};

TopBar.propTypes = {
  logo: PropTypes.string.isRequired,
  buttons: PropTypes.arrayOf(
    PropTypes.shape({
      name: PropTypes.string.isRequired,
      route: PropTypes.string.isRequired,
    })
  ).isRequired,
};

export default TopBar;
