from flask_sqlalchemy import SQLAlchemy
from flask import Flask



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/tododb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

try:
    from app import todo
    app.register_blueprint(todo.task_api)
except Exception as e:
    print(f"Error: {e}")
