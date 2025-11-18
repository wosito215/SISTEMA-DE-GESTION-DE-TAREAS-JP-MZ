import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from models import Task


class TaskUI:
    def __init__(self, task_manager):
        self.task_manager = task_manager
        self.root = tk.Tk()
        self.root.title("Gestión de Tareas Inteligente")
        self.root.geometry("850x450")

        # Tabla con columnas en español
        self.tree = ttk.Treeview(
            self.root,
            columns=("Título", "Descripción", "Categoría",
                     "Fecha límite", "Estado", "Prioridad"),
            show="headings"
        )

        headers = {
            "Título": 150,
            "Descripción": 200,
            "Categoría": 120,
            "Fecha límite": 120,
            "Estado": 100,
            "Prioridad": 80
        }

        for col, width in headers.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Botones
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Button(frame, text="Agregar tarea",
                  command=self.add_task).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Editar tarea", command=self.edit_task).pack(
            side=tk.LEFT, padx=5)
        tk.Button(frame, text="Eliminar tarea",
                  command=self.delete_task).pack(side=tk.LEFT, padx=5)
        # El botón de actualizar ahora solicita ordenamiento (sort=True)
        tk.Button(frame, text="Actualizar lista", command=lambda: self.refresh_list(
            sort=True)).pack(side=tk.LEFT, padx=5)

        # Mostrar lista sin ordenar al inicio
        self.refresh_list(sort=False)

    def run(self):
        self.root.mainloop()

    def refresh_list(self, sort=False):

        # Carga y muestra las tareas. Si sort=True, primero ordena por prioridad.
        if sort:
            # ordena de mayor prioridad a menor (reverse=True)
            self.task_manager.sort_tasks(reverse=True)

        for row in self.tree.get_children():
            self.tree.delete(row)

        for task in self.task_manager.get_all_tasks():
            # Manejo seguro de fecha (puede ser datetime o string)
            try:
                due = task.deadline.strftime(
                    "%Y-%m-%d") if hasattr(task.deadline, "strftime") else str(task.deadline)
            except Exception:
                due = str(task.deadline)

            self.tree.insert(
                "",
                "end",
                iid=task.id,
                values=(
                    task.title,
                    task.description,
                    task.category,
                    due,
                    task.status,
                    task.priority
                )
            )

    def add_task(self):
        self._open_task_editor()

    def edit_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "Atención", "Seleccione una tarea para editar.")
            return

        task_id = selected[0]
        task = self.task_manager.get_task(task_id)
        if not task:
            messagebox.showerror(
                "Error", "No se encontró la tarea seleccionada.")
            return

        self._open_task_editor(task)

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "Atención", "Seleccione una tarea para eliminar.")
            return

        task_id = selected[0]

        if messagebox.askyesno("Confirmar", "¿Desea eliminar esta tarea?"):
            self.task_manager.delete_task(task_id)
            self.refresh_list(sort=False)  # no ordenar automáticamente

    # ===========================
    # VENTANA PARA EDITAR O CREAR
    # ===========================
    def _open_task_editor(self, task=None):
        editor = tk.Toplevel(self.root)
        editor.title("Editar tarea" if task else "Agregar tarea")
        editor.geometry("400x550")

        # Campos
        labels = ["Título", "Descripción", "Categoría",
                  "Fecha límite (YYYY-MM-DD)", "Estado", "Prioridad (1-5)"]
        fields = {}

        for label in labels:
            tk.Label(editor, text=label).pack()
            entry = tk.Entry(editor, width=40)
            entry.pack(pady=5)
            fields[label] = entry

        # Si es edición, cargar datos
        if task:
            fields["Título"].insert(0, task.title)
            fields["Descripción"].insert(0, task.description)
            fields["Categoría"].insert(0, task.category)
            fields["Fecha límite (YYYY-MM-DD)"].insert(0, task.deadline.strftime(
                "%Y-%m-%d") if hasattr(task.deadline, "strftime") else str(task.deadline))
            fields["Estado"].insert(0, task.status)
            fields["Prioridad (1-5)"].insert(0, str(task.priority))

        # Guardar cambios
        def save():
            try:
                title = fields["Título"].get()
                description = fields["Descripción"].get()
                category = fields["Categoría"].get()
                deadline_str = fields["Fecha límite (YYYY-MM-DD)"].get()
                status = fields["Estado"].get() or "Pendiente"
                priority_text = fields["Prioridad (1-5)"].get()
                priority = int(priority_text) if priority_text.isdigit() else 5

                # convertir fecha (si el usuario ingresó), si falla se guarda como string
                try:
                    deadline = datetime.strptime(
                        deadline_str, "%Y-%m-%d") if deadline_str else ""
                except Exception:
                    deadline = deadline_str

                if task:
                    # Actualizar tarea existente
                    task.title = title
                    task.description = description
                    task.category = category
                    task.status = status
                    task.priority = priority
                    task.deadline = deadline
                    self.task_manager.update_task(task)
                else:
                    # Nueva tarea
                    new_task = Task(title, description, category,
                                    deadline, priority, status)
                    self.task_manager.add_task(new_task)

                editor.destroy()
                # no ordenar automáticamente al guardar
                self.refresh_list(sort=False)
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {e}")

        tk.Button(editor, text="Guardar", command=save).pack(pady=20)
