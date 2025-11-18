import unittest
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'source')))

from models import Task
from task_manager import TaskManager
from storage_json import JSONStorage
from priority_strategies import ManualPriorityStrategy, DatePriorityStrategy


print("PRUEBAS SISTEMA GESTIÓN DE TAREAS")



class TestTask(unittest.TestCase):
    """Pruebas básicas de Task"""
    
    def test_crear_y_convertir_tarea(self):
        """Crear tarea, convertir a dict y desde dict"""
        tarea = Task("Test", "Descripción", "Personal", "2025-12-31", priority=5)
        
        self.assertEqual(tarea.title, "Test")
        self.assertIsNotNone(tarea.id)
        
        # Convertir a dict y back
        tarea_dict = tarea.to_dict()
        tarea_nueva = Task.from_dict(tarea_dict)
        self.assertEqual(tarea_nueva.title, "Test")
        print("✓ Task - Creación y conversión: OK")


class TestStorage(unittest.TestCase):
    """Pruebas de almacenamiento JSON"""
    
    def setUp(self):
        self.test_file = "test_temp.json"
    
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_guardar_y_cargar(self):
        """Guardar tareas y cargarlas después"""
        storage = JSONStorage(self.test_file)
        
        tareas = [
            Task("T1", "D1", "Cat1", "2025-12-31", priority=5),
            Task("T2", "D2", "Cat2", "2025-11-30", priority=3)
        ]
        
        storage.save_all(tareas)
        tareas_cargadas = storage.load_all()
        
        self.assertEqual(len(tareas_cargadas), 2)
        self.assertEqual(tareas_cargadas[0].title, "T1")
        print("✓ Storage - Guardar y cargar: OK")


class TestTaskManager(unittest.TestCase):
    """Pruebas del gestor de tareas"""
    
    def setUp(self):
        self.test_file = "test_manager.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.manager = TaskManager(JSONStorage(self.test_file))
    
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_crud_completo(self):
        """Probar crear, leer, actualizar y eliminar"""
        # Crear
        tarea = Task("Nueva", "Desc", "Personal", "2025-12-31")
        self.manager.add_task(tarea)
        self.assertEqual(len(self.manager.get_all_tasks()), 1)
        
        # Leer
        tarea_encontrada = self.manager.get_task(tarea.id)
        self.assertIsNotNone(tarea_encontrada)
        self.assertEqual(tarea_encontrada.title, "Nueva")
        
        # Actualizar
        tarea.title = "Modificada"
        tarea.priority = 10
        self.manager.update_task(tarea)
        tarea_actualizada = self.manager.get_task(tarea.id)
        self.assertEqual(tarea_actualizada.title, "Modificada")
        
        # Eliminar
        self.manager.delete_task(tarea.id)
        self.assertEqual(len(self.manager.get_all_tasks()), 0)
        print("✓ Manager - CRUD completo: OK")
    
    def test_ordenar_por_prioridad(self):
        """Ordenar tareas por prioridad"""
        self.manager.add_task(Task("Baja", "D", "C", "2025-12-31", priority=2))
        self.manager.add_task(Task("Alta", "D", "C", "2025-12-31", priority=10))
        self.manager.add_task(Task("Media", "D", "C", "2025-12-31", priority=5))
        
        self.manager.sort_tasks(reverse=True)
        tareas = self.manager.get_all_tasks()
        
        self.assertEqual(tareas[0].priority, 10)
        self.assertEqual(tareas[2].priority, 2)
        print("✓ Manager - Ordenamiento: OK")
    
    def test_persistencia(self):
        """Verificar que se guarda correctamente"""
        self.manager.add_task(Task("Persistente", "D", "C", "2025-12-31"))
        
        nuevo_manager = TaskManager(JSONStorage(self.test_file))
        self.assertEqual(len(nuevo_manager.get_all_tasks()), 1)
        print("✓ Manager - Persistencia: OK")


class TestStrategies(unittest.TestCase):
    """Pruebas de estrategias de prioridad"""
    
    def test_manual_strategy(self):
        """Estrategia manual mantiene prioridad"""
        strategy = ManualPriorityStrategy()
        tarea = Task("Test", "D", "C", "2025-12-31", priority=7)
        tarea = strategy.assign_priority(tarea)
        self.assertEqual(tarea.priority, 7)
        print("✓ Strategy - Manual: OK")
    
    def test_date_strategy(self):
        """Estrategia de fecha calcula prioridad"""
        strategy = DatePriorityStrategy()
        
        # Tarea vencida = urgente
        tarea_vencida = Task("Urgente", "D", "C", datetime.now() - timedelta(days=1))
        tarea_vencida = strategy.assign_priority(tarea_vencida)
        self.assertEqual(tarea_vencida.priority, 100)
        
        # Tarea en 5 días = alta prioridad
        tarea_cercana = Task("Cercana", "D", "C", datetime.now() + timedelta(days=5))
        tarea_cercana = strategy.assign_priority(tarea_cercana)
        self.assertEqual(tarea_cercana.priority, 25)
        
        # Tarea lejana = baja prioridad
        tarea_lejana = Task("Lejana", "D", "C", datetime.now() + timedelta(days=50))
        tarea_lejana = strategy.assign_priority(tarea_lejana)
        self.assertEqual(tarea_lejana.priority, 1)
        print("✓ Strategy - Fecha: OK")


class TestIntegracion(unittest.TestCase):
    """Prueba de integración completa"""
    
    def setUp(self):
        self.test_file = "test_integration.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.manager = TaskManager(JSONStorage(self.test_file))
    
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_flujo_completo(self):
        """Flujo completo: crear, modificar, ordenar, estrategias"""
        # Crear tareas
        t1 = Task("Tarea 1", "D1", "Universidad", "2025-12-15", priority=3)
        t2 = Task("Tarea 2", "D2", "Personal", "2025-11-20", priority=8)
        
        self.manager.add_task(t1)
        self.manager.add_task(t2)
        self.assertEqual(len(self.manager.get_all_tasks()), 2)
        
        # Modificar estado
        t1.status = "Completado"
        self.manager.update_task(t1)
        self.assertEqual(self.manager.get_task(t1.id).status, "Completado")
        
        # Ordenar
        self.manager.sort_tasks(reverse=True)
        self.assertEqual(self.manager.get_all_tasks()[0].priority, 8)
        
        # Aplicar estrategia
        date_strategy = DatePriorityStrategy()
        t1 = date_strategy.assign_priority(t1)
        self.manager.update_task(t1)
        
        print("✓ Integración - Flujo completo: OK")


def main():
    print("\n EJECUTANDO PRUEBAS...\n")
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestTask))
    suite.addTests(loader.loadTestsFromTestCase(TestStorage))
    suite.addTests(loader.loadTestsFromTestCase(TestTaskManager))
    suite.addTests(loader.loadTestsFromTestCase(TestStrategies))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegracion))
    
    runner = unittest.TextTestRunner(verbosity=1)
    resultado = runner.run(suite)
    

    print(" RESUMEN")
  
    print(f"Total: {resultado.testsRun}")
    print(f" Exitosas: {resultado.testsRun - len(resultado.failures) - len(resultado.errors)}")
    print(f" Fallidas: {len(resultado.failures)}")
    
    if resultado.failures:
        print("\n FALLOS:")
        for test, trace in resultado.failures:
            print(f"- {test}\n{trace}")
    
    if resultado.wasSuccessful():
        print("\n TODAS LAS PRUEBAS PASARON ")
        return 0
    return 1


if __name__ == '__main__':
    sys.exit(main())