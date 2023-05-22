# Builtin imports
from datetime import datetime, timezone, date

# Installed Imports
from flask import request, Blueprint, url_for
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

# Custom imports
from app import app, db, utils
from app.models import Task


task_api = Blueprint("task_api", __name__, url_prefix="/tasks")


class TaskException(Exception):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code


@task_api.errorhandler(TaskException)
def handle_exception(e):
    app.logger.exception(e)
    return {"success": False, "error": e.message}, e.code


@task_api.errorhandler(SQLAlchemyError)
def handle_sql_exception(e):
    app.logger.exception(e)
    return {"success": False, "error": f"{e.orig}"}, 400


# <<<<<<<<<<<<<<<<<< TODO APIS >>>>>>>>>>>>>>>>>>>>>>>>


@task_api.route("/", methods=["GET"])
@task_api.route("/<int:id>", methods=["GET"])
def get_tasks(id=None):
    """
    This API retrieves all tasks
    It gets all the tasks or a single task based on the request.
    query_params:
        limit(int): records per page
        sort(str): column to sort on.
        order(str): desc/asc
        page(int): fetch the requested page.
        search(str): search str in task
        id (int, Optional): Task id to retrieve task
    """
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

    task = task.paginate(page=page, per_page=limit, error_out=False)

    tasks = [utils.task_to_dict(task) for task in task.items]
    if len(tasks) == 0:
        raise TaskException(
            f"No tasks found.",
            404,
        )

    if task.has_next:
        next_url = url_for("task_api.get_tasks", page=task.next_num)
    else:
        next_url = None

    return {
        "all_tasks": tasks,
        "total": task.total,
        "order": order,
        "sort": sort,
        "total_pages": task.pages,
        "next_page": next_url,
    }, 200


@task_api.route("/", methods=["POST"])
def add_tasks():
    """
    This API creates tasks.
    when sending request there are the parameters that needs to be passed
    {
    "task" (str): name of the task
    }
    """
    now = datetime.now(timezone.utc)
    for data in request.get_json():
        if not data:
            raise TaskException("No Data Exists", 204)

        task = data.get("task")
        new_task = Task(task=task)
        db.session.add(new_task)

    db.session.commit()

    return {"message": "created task succesfully"}, 200


@task_api.route("/", methods=["PUT"])
def update_task():
    """
    This API updates tasks.
    when sending request these are the parameters that needs to be passed
    {
    "id" (int) : id of the task that needs to be updated
    "task" (str): name of the task
    }
    """
    now = datetime.now(timezone.utc)

    for data in request.get_json():
        id = data.get("id")
        if id is None:
            raise TaskException("No Data Exists", 400)
        task = Task.query.get(id)
        task.task = data.get("task", task.task)
        db.session.commit()

    return {"message": "Successfully updated"}, 200


@task_api.route("/", methods=["DELETE"])
@task_api.route("/<int:id>", methods=["DELETE"])
def delete_task(id=None):
    """
    This API deletes the tasks.
    Deletes single task and all tasks
    """
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
    return {"message": "Successfully deleted"}, 200
