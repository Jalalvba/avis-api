from flask import Flask, jsonify, request
from get import get_bdd_data
from append import append_row_to_bdd

app = Flask(__name__)

@app.route('/data', methods=['GET'])
def data_route():
    try:
        data = get_bdd_data()
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/data', methods=['POST'])
def append_route():
    try:
        # Get JSON from client
        json_data = request.get_json()
        if not json_data:
            return jsonify({"success": False, "error": "No JSON payload received"}), 400

        # Ordered row to match the sheet headers
        headers = [
            "Immatriculation",
            "Date",
            "Client",
            "Modèle",
            "lieu",
            "prestataire",
            "commentaire"
        ]

        row = [json_data.get(col, "") for col in headers]

        result = append_row_to_bdd(row)
        return jsonify({"success": True, "update": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
