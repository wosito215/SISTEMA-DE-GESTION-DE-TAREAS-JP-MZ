from uuid import uuid4
from datetime import datetime

class Task:
    def __init__(self, title, description, category, deadline, priority=5, status="Pendiente", task_id=None):
        self.id = task_id if task_id else str(uuid4())
        self.title = title
        self.description = description
        self.category = category
        self.priority = priority
        self.status = status

        # Convertir la fecha
        if isinstance(deadline, str):
            self.deadline = datetime.strptime(deadline, "%Y-%m-%d")
        else:
            self.deadline = deadline


    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "deadline": self.deadline.strftime("%Y-%m-%d"),
            "priority": self.priority,
            "status": self.status
        }


    @staticmethod
    def from_dict(data):
        return Task(
            title=data.get("title", "Sin título"),
            description=data.get("description", ""),
            category=data.get("category", "General"),
            deadline=data.get("deadline", "2000-01-01"),
            priority=data.get("priority", 5),
            status=data.get("status", "Pendiente"),
            task_id=data.get("id")
        )
