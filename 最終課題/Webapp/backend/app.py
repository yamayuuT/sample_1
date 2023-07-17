from flask import Flask, request, jsonify
from dwave.system import LeapHybridSampler
from dwave_qbsolv import QBSolv
from tsp_solver import TSPSolver

app = Flask(__name__)

@app.route('/calculate-route', methods=['POST'])
def calculate_route():
    cities = request.json['cities']

    # TSP solver インスタンスを生成
    solver = TSPSolver(cities)

    # 最短経路を計算
    best_route = solver.solve()

    return jsonify({'best_route': best_route})

if __name__ == "__main__":
    app.run(debug=True)


from flask_cors import CORS

CORS(app)
