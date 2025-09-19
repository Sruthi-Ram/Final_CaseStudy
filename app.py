from flask import Flask
from config import Config
from models import db
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)

# Register routes
from routes.auth import auth_bp
from routes.tasks import tasks_bp

app.register_blueprint(auth_bp)
app.register_blueprint(tasks_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

