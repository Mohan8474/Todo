from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify
from flask import Blueprint, request
from datetime import datetime, timezone, date
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/tododb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

# task_api = Blueprint("task_api", __name__, url_prefix="/tasks")
# app.unregister_blueprint(task_api)
# try:
#     app.register_blueprint(task_api)

# except Exception as e:
#     import traceback

#     traceback.print_exc()
#     app.logger.error(e)


class Task(db.Model):

    id: int = db.Column(db.Integer, primary_key=True)
    task: str = db.Column(db.Text, nullable=False)
    create_time: date = db.Column(
        db.DateTime(timezone.utc), nullable=False, default=datetime.utcnow
    )
    modify_time: date = db.Column(
        db.DateTime(timezone.utc), nullable=False, default=datetime.utcnow
    )

def task_to_dict(task):
    return{
        "id" :task.id,
        "task":task.task,
        "create_time":task.create_time,
        "modify_time":task.modify_time
    }

class TaskException(Exception):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code

@app.errorhandler(TaskException)
def handle_exception(e):
    app.logger.exception(e)
    return {"success": False, "error": e.message}, e.code


@app.route("/", methods=["GET"])
@app.route("/<int:id>", methods=["GET"])
def get_tasks(id=None):
    
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 5, type=int)
    order = request.args.get("order", "asc")
    sort = request.args.get("sort", "task")
    search = request.args.get("search")
    task = Task.query

    if id:
        task = task.filter(Task.id == id).first()
        if not task:
            raise TaskException(
                f"Task with id {id} doesn't exist.",
                404,
            )

    if order == "asc":
        task = task.order_by(sort)
    else:
        task = task.order_by(desc(sort))
    
    if search:
        task = task.filter(Task.task.ilike(f"%{search}%"))
    
    task = task.paginate(page=page, per_page=limit, error_out =False)

    tasks = [task_to_dict(task) for task in task.items]
    if len(tasks) == 0:
        raise TaskException(
                f"No tasks found.",
                404,
            )

    return {
        "tasks":tasks,
        "total":task.total
    }

@app.route("/", methods=["POST"])
def add_tasks():
    now = datetime.now(timezone.utc)
    for data in request.get_json():
        if data is None:
            raise TaskException("No Data Exists", 204)
        
        task = data.get("task")
        new_task = Task(task=task)
        db.session.add(new_task)

    db.session.commit()


    return {
        "message": "created task succesfully"
    }


@app.route("/", methods=["PUT"])
def update_task(id=None):
    now = datetime.now(timezone.utc)
    
    for data in request.get_json():
        id = data.get("id")
        if id is None:
            raise TaskException("No Data Exists", 400)
        task = Task.query.get(id)
        task.task = data.get("task", task.task)
        db.session.commit()
   
    return {
        "message" :"Successfully updated"
    }

@app.route("/", methods = ["DELETE"])
@app.route("/<int:id>", methods = ["DELETE"])
def delete_task(id=None):
    if id:
        task = Task.query.get(id)
        if id is None:
            raise TaskException("No Data Exists", 400)
        db.session.delete(task)
    else:
        task = Task.query.all()
        for task in task:
            db.session.delete(task)

    db.session.commit()
    return {
        "message" :"Successfully deleted"
    }

if __name__ == "__main__":
    
    app.run(debug=True)