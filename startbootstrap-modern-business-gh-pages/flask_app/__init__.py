from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import and register routes
    from .app import main
    app.register_blueprint(main)

    return app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)