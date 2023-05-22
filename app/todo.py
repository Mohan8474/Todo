from flask import request , Blueprint
from sqlalchemy import desc
from app import app, db
from datetime import datetime, timezone, date
from app.models import Task



class TaskException(Exception):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code

@app.errorhandler(TaskException)
def handle_exception(e):
    app.logger.exception(e)
    return {"success": False, "error": e.message}, e.code


task_api = Blueprint("task_api", __name__, url_prefix="/tasks")

def task_to_dict(task):
    return{
        "id" :task.id,
        "task":task.task,
        "create_time":task.create_time,
        "modify_time":task.modify_time
    }


@task_api.route("/", methods=["GET"])
@task_api.route("/<int:id>", methods=["GET"])
def get_tasks(id=None):
    
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 5, type=int)
    order = request.args.get("order", "asc")
    sort = request.args.get("sort", "task")
    search = request.args.get("search")
    task = Task.query

    if id:
        task = task.filter(Task.id == id)
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
        "total":task.total,
        "order":order
    }

@task_api.route("/", methods=["POST"])
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


@task_api.route("/", methods=["PUT"])
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

@task_api.route("/", methods = ["DELETE"])
@task_api.route("/<int:id>", methods = ["DELETE"])
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