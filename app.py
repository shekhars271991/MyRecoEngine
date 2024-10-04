from flask import Flask
from routes import main_routes
from services.db.redisvl_service import initialize
from flask_cors import CORS

app = Flask(__name__)

CORS(app)


# Register blueprint for main routes
app.register_blueprint(main_routes)

if __name__ == '__main__':
    initialize()
    app.run(debug=True)

