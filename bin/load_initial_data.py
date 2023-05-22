import os
import sys
import json


parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(parentdir)
sys.path.insert(0, parentdir)

from app import app
from app.models import db, Task


def create_object_in_db_at_startup(json_file_path):
    with open(json_file_path) as json_file:
        data = json.load(json_file).get("Task")

        for item in data:
            id = item["id"]
            task = Task.query.filter(Task.id == id).first()
            if not task:
                task = Task(
                    id=item["id"],
                    task=item["task"],
                    create_time=item["create_time"],
                    modify_time=item["modify_time"],
                )
                db.session.add(task)
        db.session.commit()


create_object_in_db_at_startup("bin/initial_data.json")
