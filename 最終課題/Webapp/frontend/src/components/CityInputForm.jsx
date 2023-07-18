import React, { useState } from "react";

const CityInputForm = ({ setCities }) => {
  const [input, setInput] = useState("");

  const handleInputChange = (event) => {
    setInput(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    setCities(input.split(","));
    setInput("");
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Cities:
        <input type="text" value={input} onChange={handleInputChange} />
      </label>
      <input type="submit" value="Submit" />
    </form>
  );
};

export default CityInputForm;
