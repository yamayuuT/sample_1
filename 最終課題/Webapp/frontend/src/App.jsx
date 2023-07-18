import React, { useState } from 'react';
import axios from 'axios';
import Map from './Map';  // Import the Map component

function App() {
  const [cities, setCities] = useState([]);
  const [inputCity, setInputCity] = useState("");
  const [result, setResult] = useState(null);

  const calculateRoute = async () => {
    try {
      const response = await axios.post('http://localhost:8080/api/calculate-route', {
        cities: cities
      });
      console.log(response.data);
      setResult(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const addCity = () => {
    setCities(prevCities => [...prevCities, inputCity]);
    setInputCity("");
  }

  return (
    <div className="App">
      <input type="text" value={inputCity} onChange={e => setInputCity(e.target.value)} />
      <button onClick={addCity}>Add City</button>
      <ul>
        {cities.map((city, index) => (
          <li key={index}>{city}</li>
        ))}
      </ul>
      <button onClick={calculateRoute}>Calculate Route</button>
      {result && (
        <div>
          <p>Total Distance: {result.total_distance} km</p>
          <p>Route:</p>
          <ul>
            {result.route.map((city, index) => (
              <li key={index}>{city.city}</li>
            ))}
          </ul>
          <Map route={result.route.map(city => city.coordinates)} />  {/* Use the Map component */}
        </div>
      )}
    </div>
  );
}

export default App;

