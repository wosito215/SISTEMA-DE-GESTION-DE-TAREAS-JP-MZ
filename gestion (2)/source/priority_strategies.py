from abc import ABC, abstractmethod
from datetime import datetime


class PriorityStrategy(ABC):
    # Interfaz base para todas las estrategias de prioridad

    @abstractmethod
    def calculate_priority(self, task):
        pass

    def assign_priority(self, task):

        # Método estándar llamado desde TaskManager.
        # Todas las estrategias usan calculate_priority para definir la prioridad.
        task.priority = self.calculate_priority(task)
        return task


class ManualPriorityStrategy(PriorityStrategy):
    # Prioridad manual: usa el valor ya ingresado por el usuario
    def calculate_priority(self, task):
        return task.priority


class DatePriorityStrategy(PriorityStrategy):

    # Prioridad basada en fecha límite.
    # Las tareas más cercanas a la fecha límite tendrán prioridad más alta.
    def calculate_priority(self, task):
        days_remaining = (task.deadline - datetime.now()).days
        if days_remaining <= 0:
            return 100  # urgencia máxima
        return max(1, 30 - days_remaining)


class CategoryPriorityStrategy(PriorityStrategy):

    # Prioridad basada en categoría.
    def calculate_priority(self, task):
        return self.CATEGORY_PRIORITY.get(task.category, 0)
