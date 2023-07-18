import React, { useEffect, useRef } from 'react';

const Map = ({ route }) => {
  const mapRef = useRef();

  useEffect(() => {
    if (!route.length || !route[0].hasOwnProperty('lat') || !route[0].hasOwnProperty('lng')) {
      console.error('Invalid route data');
      return;
    }

    const map = new google.maps.Map(mapRef.current, {
      zoom: 5,
      center: route[0],
      mapTypeId: 'roadmap',
    });

    const path = new google.maps.Polyline({
      path: route,
      geodesic: true,
      strokeColor: '#FF0000',
      strokeOpacity: 1.0,
      strokeWeight: 2,
    });

    path.setMap(map);
  }, [route]);

  return (
    <div id="map" ref={mapRef} style={{ width: '100%', height: '400px' }}></div>
  );
};

export default Map;
