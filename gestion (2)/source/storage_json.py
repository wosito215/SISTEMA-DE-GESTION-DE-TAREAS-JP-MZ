import json
import os
from models import Task

class JSONStorage:
    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                f.write("[]")

    def load_all(self):
        try:
            with open(self.filename, "r") as f:
                content = f.read().strip()
                if not content:
                    return []
                data = json.loads(content)

            return [Task.from_dict(item) for item in data]

        except (json.JSONDecodeError, ValueError):
            with open(self.filename, "w") as f:
                f.write("[]")
            return []

    def save_all(self, tasks):
        with open(self.filename, "w") as f:
            json.dump([task.to_dict() for task in tasks], f, indent=4)
