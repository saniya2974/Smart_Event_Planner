from flask import Flask
from flask_cors import CORS
from routes.event_routes import event_routes

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow frontend access

# Register all routes
app.register_blueprint(event_routes)

if __name__ == "__main__":
    app.run(debug=True)
