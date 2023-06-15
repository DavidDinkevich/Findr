import React from 'react';
import './bar-chart.css';

const BarChart = ({ modelName, intervals, accuracies, numFrames, color }) => {
  const barWidth = 500; // Width of the bar (in pixels)
  const barHeight = 20; // Height of the bar (in pixels)

  //To calculate the position of the interval depending on the frame intervals returned from BE
  const calculateIntervalPosition = (interval) => {
    const [start, end] = interval;
    const intervalWidth = (end - start) / numFrames * barWidth;
    const intervalPosition = (start / numFrames) * barWidth;
    return [intervalWidth, intervalPosition];
  };

  //To assign color to intervals by accuracy of model returned from BE 
  const getColorForAccuracy = (accuracy) => {
    const minColor = [225,245,254]; // light blue
    const maxColor = [64, 196, 255]; // bright blue
  
    const colorByAccuracy = minColor.map((min, i) => {
      const max = maxColor[i];
      const range = max - min;
      const colorValue = Math.round(min + range * (accuracy/100));
      return colorValue;
    });
  
    const colorString = `rgb(${colorByAccuracy[0]}, ${colorByAccuracy[1]}, ${colorByAccuracy[2]})`;
    return colorString;
  };
  
  
  
  
//Renders the intervals on the bar depending on the intevel and the color calculated for it
const renderIntervals = () => { 
  return intervals.map((interval, index) => {
    //getting the position and the accuracy to detemine the color
    const [intervalWidth, intervalPosition] = calculateIntervalPosition(interval);
    const accuracy = accuracies[index];
    const intervalColor = getColorForAccuracy(accuracy);

    // Style of interval
    const intervalStyle = {
      width: intervalWidth,
      backgroundColor: intervalColor,
      display: 'inline-block',
      height: barHeight,
      position: 'absolute',
      left: intervalPosition,
    };

    // Return a <div> element for the interval
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
    backgroundColor: 'white',
    position: 'relative',
    marginTop: '10px',
  };
  const backroundColor= 'rgb(255, 255, 255)';

  return (
    <div>
      <h2 style={{ color: {backroundColor}, fontSize: '26px' }}>{modelName} results</h2>
      <div style={barStyle} className="heat-bar">
        <div style={{ position: 'relative', width: '100%' }}>{renderIntervals()}</div>
      </div>
    </div>
  );
};

export default BarChart;
