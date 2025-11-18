import uuid
from models import Task
from storage_json import JSONStorage


class TaskManager:
    def __init__(self, storage: JSONStorage):
        self.storage = storage
        self.tasks = self.storage.load_all()

    def get_all_tasks(self):
        return self.tasks

    def get_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def add_task(self, task: Task):
        # asignar id si no tiene
        if not getattr(task, "id", None):
            task.id = str(uuid.uuid4())
        self.tasks.append(task)
        self.save()

    def update_task(self, updated_task: Task):
        for i, task in enumerate(self.tasks):
            if task.id == updated_task.id:
                self.tasks[i] = updated_task
                break
        self.save()

    def delete_task(self, task_id):
        self.tasks = [t for t in self.tasks if t.id != task_id]
        self.save()

    def sort_tasks(self, reverse=True):
        """Ordena la lista de tareas por prioridad.
        reverse=True  -> de mayor prioridad a menor 
        reverse=False -> de menor a mayor """
        self.tasks.sort(key=lambda t: t.priority, reverse=reverse)

    def save(self):
        self.storage.save_all(self.tasks)
