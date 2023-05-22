from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:postgres@localhost:5432/tododb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.app_context().push()

try:
    from app import todo, models

    app.register_blueprint(todo.task_api)
    models.db.create_all()
except Exception as e:
    print(f"Error: {e}")


# try:
#     from app import todo

#     app.register_blueprint(todo.task_api)
# except Exception as e:
#     import traceback

#     traceback.print_exc()
#     app.logger.error(e)