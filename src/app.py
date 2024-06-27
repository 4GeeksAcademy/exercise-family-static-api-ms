"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
       
        "family": members
    }
    return jsonify(response_body), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    # this is how you can use the Family datastructure by calling its methods
    member = jackson_family.get_member(member_id)
    if not member:
        return jsonify({"Error":"the member does not exist"}), 400
    return jsonify(member), 200

@app.route('/member', methods=['POST'])
def add_member():
    request_data = request.get_json()

    # Verificar que los datos requeridos estén presentes
    required_fields = ['first_name', 'age', 'lucky_numbers']
    for field in required_fields:
        if field not in request_data:
            return jsonify({"error": f"'{field}' es un campo requerido"}), 400

    added_member = {
        "first_name": request_data['first_name'],
        "age": request_data['age'],
        "lucky_numbers": request_data['lucky_numbers']
    }

    # Suponiendo que jackson_family.add_member agrega el miembro a la familia
    jackson_family.add_member(added_member)

    return jsonify(added_member), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_family_member(member_id):
    # this is how you can use the Family datastructure by calling its methods
    eliminate_familiar = jackson_family.delete_member(member_id)
    if not eliminate_familiar:
        return jsonify({"Error":"familiar no encontrado"}), 400
    return jsonify({"Hecho":"familiar borrado "}), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
