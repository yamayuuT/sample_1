from flask import Flask, jsonify, request
from flask_cors import CORS
from googlemaps import Client
import math
import numpy as np
from openjij import SQASampler
from scipy.optimize import linear_sum_assignment
from flask_socketio import SocketIO



app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*") 
CORS(app)

gmaps = Client(key='AIzaSyC_3F7w0X1qdK37ObX3PSFBgnrPgCjQWSU')


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


@app.route("/api/calculate-route", methods=['POST'])
def calculate_route():    
    cities = request.get_json()['cities']
    geocoded_cities = []
    
    # 各都市の座標を取得
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

    # 距離行列を計算
    num_cities = len(cities)
    distance_matrix = np.zeros((num_cities, num_cities))
    for i in range(num_cities):
        for j in range(i+1, num_cities):
            distance = calculate_distance(locations[i]['coordinates']['lat'], locations[i]['coordinates']['lng'], locations[j]['coordinates']['lat'], locations[j]['coordinates']['lng'])
            distance_matrix[i, j] = distance
            distance_matrix[j, i] = distance

    # Greedy法を使ってTSPを解く
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

    # 都市の順序リストと総距離を返す
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

    # 各都市の緯度と経度を取得
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

    # 距離行列を計算
    distance_matrix = np.zeros((n_cities, n_cities))
    for i in range(n_cities):
        for j in range(i+1, n_cities):
            dist = calculate_distance(locations[i]['coordinates']['lat'],
                                      locations[i]['coordinates']['lng'],
                                      locations[j]['coordinates']['lat'],
                                      locations[j]['coordinates']['lng'])
            distance_matrix[i, j] = dist
            distance_matrix[j, i] = dist

    # QUBOの定義
    socketio.emit('progress', {'message': 'Defining QUBO...'}, namespace='/api')
    Q_dict = {}
    for i in range(n_cities):
        for j in range(n_cities):
            if i != j:
                for k in range(n_cities):
                    Q_dict[(n_cities * i + j, n_cities * k + j)] = distance_matrix[i][k]

    # 各都市がちょうど一度だけ訪れられる 制約条件1
    for i in range(n_cities):
        for j in range(n_cities):
            for k in range(j+1, n_cities):
                Q_dict[(n_cities * i + j, n_cities * i + k)] = 2 * 1e9  # Very large number
    for j in range(n_cities):
        for i in range(n_cities):
            for k in range(i+1, n_cities):
                Q_dict[(n_cities * i + j, n_cities * k + j)] = 2 * 1e9  # Very large number

    # QUBOに制約を追加
    for i in range(n_cities):
        for j in range(n_cities):
            if i != j:
                Q_dict[(n_cities * i + j, n_cities * i + j)] = -1e9  # Negative large number

    socketio.emit('progress', {'message': f'QUBO defined. Sample size: {len(Q_dict)}'}, namespace='/api')

    # SQAでQUBOを解く
    socketio.emit('progress', {'message': 'Solving QUBO with SQA...'}, namespace='/api')
    sampler = SQASampler()
    response = sampler.sample_qubo(Q_dict, num_reads=5000)

    socketio.emit('progress', {'message': f'Solution found. Energy: {response.first.energy}'}, namespace='/api')

    # コスト関数の最小値(基底)
    solution = response.first.sample

    # Process the solution
    try:
        #タプルのリストを作成（visit_order, city_index）
        route_tuples = [(i // n_cities, i % n_cities) for i, value in solution.items() if value == 1]
        # visit_order でソートし、都市のインデックスを保持
        route_indices = [city_index for visit_order, city_index in sorted(route_tuples)]
    except Exception as e:
        return jsonify({"error": "Error while processing the solution: {}".format(str(e))}), 500

     # インデックスからルートを構築
    route = [locations[i] for i in route_indices]

     # 計算されたルートがすべての都市をカバーしていない場合、最近傍メソッドを使用して残りの都市を追加(量子サンプラーだと、入力=出力にならず数が勝手に減ることがあるため)
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

    # total距離の計算
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
