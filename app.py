from flask import Flask, jsonify, request
from flask_cors import CORS
from get import get_bdd_data                 # Fonction pour lire les données depuis Google Sheets
from append import append_row_to_bdd        # Fonction pour ajouter une ligne
from update import update_row_by_immat      # Fonction pour mettre à jour une ligne par immatriculation
from delete import delete_row_by_immat      # Fonction pour supprimer une ligne
import os
import time                                 # Pour gérer l’expiration du cache

# === Initialisation de l’application Flask ===
app = Flask(__name__)
CORS(app)  # Autoriser toutes les origines (utile pour frontend local)

# === Configuration des en-têtes des colonnes du tableau ===
HEADERS = [
    "Immatriculation", "Date", "Client", "Modèle",
    "lieu", "prestataire", "commentaire"
]

# === Configuration du cache ===
CACHE_TTL = 300         # Durée de vie du cache : 300 secondes = 5 minutes
_data_cache = None      # Contenu du cache (liste des lignes)
_cache_time = 0         # Horodatage du dernier chargement depuis Google Sheets

# === GET /data : Obtenir toutes les données ===
@app.route('/data', methods=['GET'])
def data_route():
    global _data_cache, _cache_time

    # ✅ Si cache est valide (pas expiré), retourne les données mises en cache
    if _data_cache and (time.time() - _cache_time < CACHE_TTL):
        return jsonify({"success": True, "data": _data_cache})

    try:
        # ❗Sinon, on recharge depuis Google Sheets
        data = get_bdd_data()
        _data_cache = data           # Met à jour le cache
        _cache_time = time.time()    # Met à jour l'horodatage
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# === POST /data : Ajouter une nouvelle ligne ===
@app.route('/data', methods=['POST'])
def append_route():
    global _data_cache, _cache_time

    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({"success": False, "error": "No JSON payload received"}), 400

        # Construire la ligne à partir des champs envoyés
        row = [json_data.get(col, "") for col in HEADERS]
        result = append_row_to_bdd(row)

        # ❌ Invalider le cache (prochaine lecture fera appel à Google Sheets)
        _data_cache = None
        _cache_time = 0

        return jsonify({"success": True, "update": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# === PUT /data/<immat> : Mettre à jour une ligne selon l'immatriculation ===
@app.route('/data/<immat>', methods=['PUT'])
def update_route(immat):
    global _data_cache, _cache_time

    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({"success": False, "error": "No JSON payload"}), 400

        # update_row_by_immat s’occupe de normaliser et trouver la ligne à modifier
        result = update_row_by_immat(immat, json_data)

        # ❌ Invalider le cache après la modification
        _data_cache = None
        _cache_time = 0

        return jsonify({
            "success": True,
            "update": result["result"],
            "updated_row": result["updated_row"]
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# === DELETE /data/<immat> : Supprimer une ligne par immatriculation ===
@app.route('/data/<immat>', methods=['DELETE'])
def delete_route(immat):
    global _data_cache, _cache_time

    try:
        result = delete_row_by_immat(immat)

        # ❌ Invalider le cache après suppression
        _data_cache = None
        _cache_time = 0

        return jsonify({"success": True, "deleted": True, "details": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# === Lancement de l'application sur le port Cloud Run ou 8080 par défaut ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
