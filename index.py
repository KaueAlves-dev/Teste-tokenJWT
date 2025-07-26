from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from datetime import timedelta

db = {}
bluep = Blueprint("bluep", __name__)

@bluep.route('/register', methods=['POST'])
def register():
  data = request.json
  username = data['username']
  password = generate_password_hash(data['password'])

  if username in db:
    return jsonify(msg='Usuário já cadastrado'), 409
  
  db[username] = password
  return jsonify(msg='Usuário cadastrado com sucesso'), 201

@bluep.route('/login', methods=['POST'])
def login():
  data = request.json
  username = data['username']
  password = data['password']

  if username not in db:
    return jsonify(msg='Usuário não encontrado'), 404
  
  if not check_password_hash(db[username], password):
    return jsonify(msg='Senha incorreta'), 401
  
  token = create_access_token(identity=username, 
                              expires_delta=timedelta(seconds=120),
                                additional_claims={"role":"user"}) # client id
  refresh = create_refresh_token(identity=username,
                                 expires_delta=timedelta(hours=240))
  return jsonify(token=f'Bearer {token}', refresh_token=f'Bearer {refresh}') 

@bluep.route('/refresh', methods=['GET'])
@jwt_required(refresh=True)
def refresh():
  id = get_jwt_identity()
  token = create_access_token(identity=id, expires_delta=timedelta(seconds=120)) # client id
  return jsonify(token=token)

@bluep.route('/paisagem', methods=['GET'])
@jwt_required()
def paisagem():
  id = get_jwt_identity()
  return jsonify(identity= f'Olá {id}', msg='Você está vendo a CN-Tower from Canada')





