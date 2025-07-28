from flask import Flask, jsonify, request
from get import get_bdd_data
from append import append_row_to_bdd
from update import update_row_by_immat, normalize_immat  # imported normalize

app = Flask(__name__)

# GET all data
@app.route('/data', methods=['GET'])
def data_route():
    try:
        data = get_bdd_data()
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# POST append row
@app.route('/data', methods=['POST'])
def append_route():
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({"success": False, "error": "No JSON payload received"}), 400

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


# PUT update row by normalized immatriculation
@app.route('/data/<immat>', methods=['PUT'])
def update_route(immat):
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({"success": False, "error": "No JSON payload"}), 400

        headers = [
            "Immatriculation",
            "Date",
            "Client",
            "Modèle",
            "lieu",
            "prestataire",
            "commentaire"
        ]

        new_row = [json_data.get(col, "") for col in headers]
        result = update_row_by_immat(immat, new_row)

        return jsonify({"success": True, "update": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
