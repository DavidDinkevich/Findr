import React, { useState } from 'react';
import DropdownSearch from '../dropDownSearch/dropDownSearch';

const ParentComponent = () => {
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (value) => {
    setInputValue(value);
    console.log(inputValue)
  };

  return (
    <div>
      <h1>Parent Component</h1>
      <DropdownSearch inputValue={inputValue} onInputChange={handleInputChange} />
      <p>Input Value in Parent Component: {inputValue}</p>
    </div>
  );
};

export default ParentComponent;
