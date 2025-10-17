from flask import Flask
# from .routes.hello_world_routes import hello_world_bp
from .routes.book_routes import book_bp

def create_app():
    app = Flask(__name__)
    # Register Blueprints here
    # app.register_blueprint(hello_world_bp)
    app.register_blueprint(book_bp)

    return app