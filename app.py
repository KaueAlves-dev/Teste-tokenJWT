from flask import Flask
from flask_jwt_extended import JWTManager
from index import bluep

jwt = JWTManager() # JWTManager precisa ler a config (JWT_SECRET_KEY) antes de ser inicializado.
app = Flask(__name__)

# configure antes de iniciar o JWT
app.config["JWT_SECRET_KEY"] = "minha-chave-secreta"

# inicie o JWT com o app
jwt.init_app(app)

# registre os blueprints depois
app.register_blueprint(bluep)

if __name__ == "__main__":
  print('teste git revert')
  app.run(debug=True)