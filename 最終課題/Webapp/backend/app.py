from flask import Flask, jsonify, request
from flask_cors import CORS
from googlemaps import Client
import math
import numpy as np
from openjij import SQASampler
from scipy.optimize import linear_sum_assignment
from flask_socketio import SocketIO



app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Add this line
CORS(app)

gmaps = Client(key='AIzaSyC_3F7w0X1qdK37ObX3PSFBgnrPgCjQWSU')


<<<<<<< HEAD
def calculate_distance(lat1, lon1, lat2, lon2):
=======
    gmaps = Client(key='****')

    def calculate_distance(lat1, lon1, lat2, lon2):
>>>>>>> a5b38e0e27d2a5fd4b800b4497b402d1ba46699a
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


@app.route("/api/calculate-route", methods=['POST'])
def calculate_route():    
    cities = request.get_json()['cities']
    geocoded_cities = []
    
    for city in cities:
        geocode_result = gmaps.geocode(city)
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            geocoded_cities.append({'city': city, 'location': location})
        else:
            return jsonify({'error': 'Geocoding API returned no results for the city {}'.format(city)}), 400
    data = request.get_json()
    if not data or 'cities' not in data:
        return jsonify({"error": "Missing 'cities' in the request body"}), 400

    cities = data['cities']

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



@app.route("/api/calculate-route-exact", methods=['POST'])
def calculate_route_exact():
    data = request.get_json()
    if not data or 'cities' not in data:
        return jsonify({"error": "Missing 'cities' in the request body"}), 400

    cities = data['cities']
    n_cities = len(cities)

    # Get the latitude and longitude of each city
    locations = []
    for city in cities:
        socketio.emit('progress', {'message': f'Geocoding the location {city}...'}, namespace='/api')
        geocode_result = gmaps.geocode(city)

        if not geocode_result:
            print(f"Error: Geocode API returned an empty result for the city '{city}'")
            return jsonify({"error": f"Geocode API returned an empty result for the city '{city}'"}), 500
        else:
            location = geocode_result[0]['geometry']['location']
            locations.append({"city": city, "coordinates": location})

    # Calculate the distance matrix
    distance_matrix = np.zeros((n_cities, n_cities))
    for i in range(n_cities):
        for j in range(i+1, n_cities):
            dist = calculate_distance(locations[i]['coordinates']['lat'],
                                      locations[i]['coordinates']['lng'],
                                      locations[j]['coordinates']['lat'],
                                      locations[j]['coordinates']['lng'])
            distance_matrix[i, j] = dist
            distance_matrix[j, i] = dist

    # Define QUBO
    socketio.emit('progress', {'message': 'Defining QUBO...'}, namespace='/api')
    Q_dict = {}
    for i in range(n_cities):
        for j in range(n_cities):
            if i != j:
                for k in range(n_cities):
                    Q_dict[(n_cities * i + j, n_cities * k + j)] = distance_matrix[i][k]

    # Define the constraint that each city is visited exactly once
    for i in range(n_cities):
        for j in range(n_cities):
            for k in range(j+1, n_cities):
                Q_dict[(n_cities * i + j, n_cities * i + k)] = 2 * 1e9  # Very large number
    for j in range(n_cities):
        for i in range(n_cities):
            for k in range(i+1, n_cities):
                Q_dict[(n_cities * i + j, n_cities * k + j)] = 2 * 1e9  # Very large number

    # Add an additional constraint to the QUBO to ensure every city is visited
    for i in range(n_cities):
        for j in range(n_cities):
            if i != j:
                Q_dict[(n_cities * i + j, n_cities * i + j)] = -1e9  # Negative large number

    socketio.emit('progress', {'message': f'QUBO defined. Sample size: {len(Q_dict)}'}, namespace='/api')

    # Solve QUBO with SQA
    socketio.emit('progress', {'message': 'Solving QUBO with SQA...'}, namespace='/api')
    sampler = SQASampler()
    response = sampler.sample_qubo(Q_dict, num_reads=5000)

    socketio.emit('progress', {'message': f'Solution found. Energy: {response.first.energy}'}, namespace='/api')

    # Get the solution with the smallest energy
    solution = response.first.sample

    # Process the solution
    try:
        # Create a list of tuples (visit_order, city_index)
        route_tuples = [(i // n_cities, i % n_cities) for i, value in solution.items() if value == 1]
        # Sort by visit_order and keep the city indices
        route_indices = [city_index for visit_order, city_index in sorted(route_tuples)]
    except Exception as e:
        return jsonify({"error": "Error while processing the solution: {}".format(str(e))}), 500

    # Construct the route from the indices
    route = [locations[i] for i in route_indices]

    # If the calculated route does not cover all cities, use the nearest-neighbor method to add remaining cities
    if len(route) < len(locations):
        remaining_locations = [loc for loc in locations if loc not in route]
        while remaining_locations:
            current_location = route[-1]
            nearest_location = min(remaining_locations, key=lambda loc: calculate_distance(
                current_location["coordinates"]["lat"],
                current_location["coordinates"]["lng"],
                loc["coordinates"]["lat"],
                loc["coordinates"]["lng"]
            ))
            route.append(nearest_location)
            remaining_locations.remove(nearest_location)

    # Calculate the total distance
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += calculate_distance(
            route[i]["coordinates"]["lat"],
            route[i]["coordinates"]["lng"],
            route[i + 1]["coordinates"]["lat"],
            route[i + 1]["coordinates"]["lng"]
        )
    total_distance += calculate_distance(
        route[-1]["coordinates"]["lat"],
        route[-1]["coordinates"]["lng"],
        route[0]["coordinates"]["lat"],
        route[0]["coordinates"]["lng"]
    )

    return jsonify({
        "total_distance": total_distance,
        "route": [{"city": r["city"], "coordinates": r["coordinates"]} for r in route]
    })





    

if __name__ == '__main__':
    app.run(port=8080)
