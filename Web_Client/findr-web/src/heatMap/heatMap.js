import React from 'react';
import BarChart from '../barChart/barChart';

const HeatMap = ({ data }) => {
  const renderBarCharts = () => {
    return Object.entries(data).map(([modelName, modelData]) => {
      const { intervals, accuracies, num_frames } = modelData;
      return (
        <BarChart
          key={modelName}
          modelName={modelName}
          intervals={intervals}
          accuracies={accuracies}
          numFrames={num_frames}
        />
      );
    });
  };

  return <div>{renderBarCharts()}</div>;
};

export default HeatMap;
