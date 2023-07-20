import React, { useState } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import About from './components/About';
import Contact from './components/Contact';
import Map from './Map';  
import { Button, TextField, List, ListItem, Typography, Box, Container, Grid, Paper, CircularProgress } from '@mui/material';
import './App.css';
import Navbar from './components/Navbar';
import HeroSection from './components/HeroSection';
import backgroundImage from './images/background.jpg';

function MainPage() {
  const [cities, setCities] = useState([]);
  const [inputCity, setInputCity] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);



  const calculateRoute = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8080/api/calculate-route', { cities: cities });
      console.log(response.data);
      setResult(response.data);
    } catch (error) {
      handleError(error);
    } finally {
      setLoading(false);
    }
  };

  
  const calculateRouteExact = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8080/api/calculate-route-exact', { cities: cities });
      console.log(response.data);
      setResult(response.data);
    } catch (error) {
      handleError(error);
    } finally {
      setLoading(false);
    }
  };

  const handleError = (error) => {
    if (error.response) {
      console.error(error.response.data);
    } else if (error.request) {
      console.error(error.request);
    } else {
      console.error('Error', error.message);
    }
    console.error(error.config);
  };



  const addCity = () => {
    if (inputCity !== '') { // 入力欄が空でないときのみ都市を追加する
      setCities(prevCities => [...prevCities, inputCity]);
      setInputCity("");
    }
  }

  const refreshPage = () => {
    window.location.reload();
  }


  return (

    <div>
      <HeroSection />
      <div style={{ height: '50px' }}></div> {/* Add a space */}
      <Container>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Paper>
              <Box padding={2}>
                <TextField value={inputCity} onChange={e => setInputCity(e.target.value)} label="City" fullWidth />
                <Button variant="contained" color="primary" onClick={addCity} disabled={inputCity === ''}>Add City</Button>
                <Button variant="contained" color="primary" onClick={refreshPage}>Refresh</Button>
                  <List>
                    {cities.map((city, index) => (
                      <ListItem key={index}>{city}</ListItem>
                    ))}
                  </List>
                  <Button variant="contained" color="secondary" onClick={calculateRoute}>近似最適化実行</Button>
                  <Button variant="contained" color="secondary" onClick={calculateRouteExact}>量子サンプラー実行</Button>
                </Box>
              </Paper>
            </Grid>
            {loading && (
              <Box
                sx={{
                  position: 'fixed',
                  top: 0,
                  left: 0,
                  width: '100%',
                  height: '100%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  backgroundColor: 'rgba(0, 0, 0, 0.3)',
                  zIndex: 9999,
                }}
              >
                
                <CircularProgress color="secondary" />
              </Box>
            )}
            {result && (
              <Grid item xs={12}>
                <Paper>
                  <Box padding={2}>
                    <Typography variant="h6">Total Distance: {result.total_distance} km</Typography>
                    <Typography variant="h6">Route:</Typography>
                    <List>
                      {result.route.map((city, index) => (
                        <ListItem key={index}>{city.city}</ListItem>
                      ))}
                    </List>
                    <Map route={result.route.map(city => city.coordinates)} />
                  </Box>
                </Paper>
              </Grid>
            )}
          </Grid>
        </Container>
    </div>


  );
};



function App() {
  return (
    <Router>
    <Navbar />
    <Routes>
      <Route path="/" element={<MainPage />} />
      <Route path="/about" element={<About />} />
      <Route path="/contact" element={<Contact />} />
    </Routes>
    </Router>


  );
}

export default App;
