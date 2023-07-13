from flask import Flask, request, jsonify
from flask_cors import CORS

from dwave.system import LeapHybridSampler
from dimod import BinaryQuadraticModel

app = Flask(__name__)
CORS(app)


@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()

    # D-Waveシステムへのリクエストを作成します。
    bqm = BinaryQuadraticModel.from_qubo(data)

    # D-Waveシステムにリクエストを送信し、結果を取得します。
    sampler = LeapHybridSampler(token='YOUR_API_TOKEN')
    response = sampler.sample(bqm)

    # 結果をクライアントに返します。
    return jsonify(response.first.sample)