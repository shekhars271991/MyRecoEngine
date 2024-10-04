from flask import Flask
from routes.routes_movies import movie_routes
from routes.routes_products import products_routes
from routes.routes_users import users_routes

from services.db.redisvl_service import initialize
from flask_cors import CORS

app = Flask(__name__)

CORS(app)


# Register blueprint for main routes
app.register_blueprint(movie_routes)
app.register_blueprint(products_routes)
app.register_blueprint(users_routes)


if __name__ == '__main__':
    initialize()
    app.run(debug=True)

