

def task_to_dict(task):
    return {
        "id": task.id,
        "task": task.task,
        "create_time": task.create_time,
        "modify_time": task.modify_time,
    }
