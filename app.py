from flask import Flask
from routes import main_routes
from routes_movies import movies_routes
from routes_products import products_routes
from services.movies.redisvl_service import initialize
from flask_cors import CORS

app = Flask(__name__)

CORS(app)


# Register blueprints
app.register_blueprint(main_routes)
app.register_blueprint(movies_routes)
app.register_blueprint(products_routes)

if __name__ == '__main__':
    initialize()
    app.run(debug=True)

