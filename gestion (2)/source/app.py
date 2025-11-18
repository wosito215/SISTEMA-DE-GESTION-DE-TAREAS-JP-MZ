import os
from storage_json import JSONStorage
from task_manager import TaskManager
from ui import TaskUI


def run_app():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    project_root = os.path.dirname(current_dir)

    # Crear carpeta data
    data_folder = os.path.join(project_root, "data")
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # Archivo de guardado(data)
    tasks_file = os.path.join(data_folder, "tasks.json")

    print(f"Guardando datos en: {tasks_file}")  # verificar la ruta

    storage = JSONStorage(tasks_file)

    # Administrador de tareas
    manager = TaskManager(storage)

    # Interfaz gráfica
    ui = TaskUI(manager)
    ui.run()


if __name__ == "__main__":
    run_app()
