from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Eliezer technical test for Wazuh :DDD"
    }
)

app = Flask(__name__)
CORS(app)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'thisisasecretkey'

import routes
from model.User import Users



if __name__ == '__main__':
    app.run(debug= True, port= 8080)