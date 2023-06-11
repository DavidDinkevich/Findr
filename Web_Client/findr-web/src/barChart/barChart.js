import React from 'react';
import './bar-chart.css';

const BarChart = ({ modelName, intervals, accuracies, numFrames, color }) => {
  const barWidth = 500; // Width of the bar (in pixels)
  const barHeight = 20; // Height of the bar (in pixels)

  const calculateIntervalPosition = (interval) => {
    const [start, end] = interval;
    const totalFrames = numFrames - start; // Number of frames remaining in the bar after the start of the interval
    const intervalWidth = (end - start) / numFrames * barWidth;
    const intervalPosition = (start / numFrames) * barWidth;
    return [intervalWidth, intervalPosition];
  };

  const getColorForAccuracy = (accuracy) => {
    // Define the color range
    const minColor = [204,235,197]; // light green
    const maxColor = [6, 59, 0]; // dark green
  
    // Calculate the interpolated color based on the given accuracy value
    const interpolatedColor = minColor.map((min, i) => {
      const max = maxColor[i];
      const range = max - min;
      const interpolatedValue = Math.round(min + range * (accuracy/100));
      return interpolatedValue;
    });
  
    const colorString = `rgb(${interpolatedColor[0]}, ${interpolatedColor[1]}, ${interpolatedColor[2]})`;
    return colorString;
  };
  
  
  
  

  const renderIntervals = () => {
    return intervals.map((interval, index) => {
      const [intervalWidth, intervalPosition] = calculateIntervalPosition(interval);
      const accuracy = accuracies[index];
      const intervalColor = getColorForAccuracy(accuracy);

      const intervalStyle = {
        width: intervalWidth,
        backgroundColor: intervalColor,
        display: 'inline-block',
        height: barHeight,
        position: 'absolute',
        left: intervalPosition,
      };

      return (
        <div
          key={index}
          style={intervalStyle}
          title={`Accuracy: ${accuracy}`}
        ></div>
      );
    });
  };

  const barStyle = {
    width: barWidth,
    height: barHeight,
    backgroundColor: 'lightgray',
    position: 'relative',
    marginTop: '10px',
  };

  return (
    <div>
      <h2 style={{ color: 'rgb(0, 255, 42)', fontSize: '26px' }}>{modelName}</h2>
      <div style={barStyle}>
        <div style={{ position: 'relative', width: '100%' }}>{renderIntervals()}</div>
      </div>
    </div>
  );
};

export default BarChart;
