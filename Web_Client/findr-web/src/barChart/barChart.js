import React from 'react';

const BarChart = ({ modelName, intervals, accuracies, numFrames, color }) => {
  const barWidth = 400; // Width of the bar (in pixels)
  const barHeight = 20; // Height of the bar (in pixels)

  const calculateIntervalWidth = (interval) => {
    const [start, end] = interval;
    return ((end - start) / numFrames) * barWidth;
  };

  const getColorForAccuracy = (accuracy) => {
    // Sort the accuracies in ascending order
    const sortedAccuracies = [...accuracies].sort((a, b) => a - b);
  
    // Calculate the index of the accuracy within the sorted array
    const index = sortedAccuracies.indexOf(accuracy);
  
    // Calculate the color based on the position of the accuracy
    const minColor = [14,255,0]; // light green
    const maxColor = [6,59,0]; // dark Green
  
    const interpolatedColor = minColor.map((min, i) => {
      const max = maxColor[i];
      const range = max - min;
      const step = range / (sortedAccuracies.length - 1);
      const interpolatedValue = Math.round(min + step * index);
      return interpolatedValue;
    });
  
    const colorString = `rgb(${interpolatedColor[0]}, ${interpolatedColor[1]}, ${interpolatedColor[2]})`;
    return colorString;
  };
  
  
  
  
  

  const renderIntervals = () => {
    return intervals.map((interval, index) => {
      const intervalWidth = calculateIntervalWidth(interval);
      const accuracy = accuracies[index];
      const intervalColor = getColorForAccuracy(accuracy);

      const intervalStyle = {
        width: intervalWidth,
        backgroundColor: intervalColor,
        display: 'inline-block',
        height: barHeight,
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
      <h2>{modelName}</h2>
      <div style={barStyle}>{renderIntervals()}</div>
    </div>
  );
};

export default BarChart;
