import logging
import os
import uuid
from threading import Thread

# In-memory dictionary to store task status and results
# In a production environment, you would use a more robust solution like Redis or a database.
tasks = {}

def run_task_async(func, *args, **kwargs):
    """
    Runs a function in a background thread and tracks its progress.
    
    :param func: The function to run.
    :param args: Arguments for the function.
    :param kwargs: Keyword arguments for the function.
    :return: The ID of the created task.
    """
    task_id = str(uuid.uuid4())
    tasks[task_id] = {'status': 'pending', 'result': None, 'error': None}

    def task_wrapper():
        try:
            result = func(*args, **kwargs)
            tasks[task_id]['status'] = 'success'
            tasks[task_id]['result'] = result
        except Exception as e:
            logging.error(f"Task {task_id} failed: {e}", exc_info=True)
            tasks[task_id]['status'] = 'failed'
            tasks[task_id]['error'] = str(e)

    thread = Thread(target=task_wrapper)
    thread.start()
    
    tasks[task_id]['status'] = 'running'
    logging.info(f"Started task {task_id} for function {func.__name__}")
    
    return task_id

def get_task_status(task_id):
    """
    Retrieves the status and result of a task.
    
    :param task_id: The ID of the task to check.
    :return: A dictionary with the task's status and result, or None if not found.
    """
    return tasks.get(task_id)
