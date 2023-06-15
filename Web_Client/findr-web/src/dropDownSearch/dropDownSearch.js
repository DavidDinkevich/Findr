import React, { useState, useEffect } from 'react';

const DropdownSearch = ({ onInputChange }) => {
  const [inputValue, setInputValue] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const wordList = [  'person', 'bicycle', 'car', 'motorbike', 'aeroplane', 'bus', 'train', 'truck', 'boat', 'traffic_light', 'fire_hydrant', 'stop_sign', 'parking_meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports_ball', 'kite', 'baseball_bat', 'baseball_glove', 'skateboard', 'surfboard', 'tennis_racket', 'bottle', 'wine_glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot_dog', 'pizza', 'donut', 'cake', 'chair', 'sofa', 'pottedplant', 'bed', 'diningtable', 'toilet', 'tvmonitor', 'laptop', 'mouse', 'remote', 'keyboard', 'cell_phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy_bear', 'hair_drier', 'toothbrush'  ];

  useEffect(() => {
    setSuggestions(getFilteredSuggestions(inputValue));
    onInputChange(inputValue);
  }, [inputValue, onInputChange]);

  const handleInputChange = (e) => {
    const value = e.target.value;
    setInputValue(value);
  };

  const getFilteredSuggestions = (value) => {
    return wordList
      .filter((word) => word.toLowerCase().startsWith(value.toLowerCase()))
      .sort();
  };

  const handleSelectSuggestion = (suggestion) => {
    setInputValue(suggestion);
    setSuggestions([]);
    onInputChange(suggestion);
  };

  return (
    <div>
      <input
        type="text"
        value={inputValue}
        onChange={handleInputChange}
        placeholder="Enter a word..."
      />
      {inputValue && suggestions.length > 0 && (
        <ul className="dropdown-list">
          {suggestions.map((suggestion) => (
            <li
              key={suggestion}
              onClick={() => handleSelectSuggestion(suggestion)}
              className="dropdown-item"
            >
              {suggestion}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default DropdownSearch;
