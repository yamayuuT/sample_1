from flask import Flask, jsonify, request
from flask_cors import CORS
from googlemaps import Client
import math
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route("/api/calculate-route", methods=['POST'])
def calculate_route():
    data = request.get_json()
    if not data or 'cities' not in data:
        return jsonify({"error": "Missing 'cities' in the request body"}), 400

    cities = data['cities']

    gmaps = Client(key='****')

    def calculate_distance(lat1, lon1, lat2, lon2):
        R = 6371.0
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c
        return distance

    locations = []
    for city in cities:
        geocode_result = gmaps.geocode(city)
        location = geocode_result[0]['geometry']['location']
        locations.append({"city": city, "coordinates": location})

    # Calculate distance matrix
    num_cities = len(cities)
    distance_matrix = np.zeros((num_cities, num_cities))
    for i in range(num_cities):
        for j in range(i+1, num_cities):
            distance = calculate_distance(locations[i]['coordinates']['lat'], locations[i]['coordinates']['lng'], locations[j]['coordinates']['lat'], locations[j]['coordinates']['lng'])
            distance_matrix[i, j] = distance
            distance_matrix[j, i] = distance

    # Solve TSP using greedy method
    current_city = 0
    route = [current_city]
    total_distance = 0.0
    unvisited_cities = set(range(1, num_cities))

    while unvisited_cities:
        next_city = min(unvisited_cities, key=lambda city: distance_matrix[current_city][city])
        total_distance += distance_matrix[current_city][next_city]
        unvisited_cities.remove(next_city)
        route.append(next_city)
        current_city = next_city

    # Return ordered list of cities and total distance
    ordered_cities = [locations[i] for i in route]
    total_distance += distance_matrix[route[-1]][route[0]]  # Add distance back to the start city

    return jsonify({
        "total_distance": total_distance,
        "route": ordered_cities
    })

if __name__ == '__main__':
    app.run(port=8080)
