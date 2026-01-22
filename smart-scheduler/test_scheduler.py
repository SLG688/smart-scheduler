import unittest
from datetime import datetime, timedelta
from scheduler import TaskScheduler
from task import Task, Priority
from advanced_features import DurationPredictor, ConflictResolver, PriorityCalculator

class TestTaskScheduler(unittest.TestCase):
    def setUp(self):
        self.scheduler = TaskScheduler()
    
    def test_add_task(self):
        task = self.scheduler.add_task(
            name="测试任务",
            duration=60,
            priority=Priority.HIGH
        )
        self.assertIsNotNone(task)
        self.assertEqual(task.name, "测试任务")
    
    def test_topological_sort(self):
        self.scheduler.add_task(name="任务1", duration=30)
        self.scheduler.add_task(name="任务2", duration=30, dependencies=["task_0"])
        self.scheduler.add_task(name="任务3", duration=30, dependencies=["task_1"])
        
        sorted_ids = self.scheduler.topological_sort()
        self.assertEqual(len(sorted_ids), 3)
    
    def test_optimize_schedule(self):
        self.scheduler.add_task(name="任务1", duration=60)
        self.scheduler.add_task(name="任务2", duration=60)
        self.scheduler.add_task(name="任务3", duration=60)
        
        scheduled = self.scheduler.optimize()
        self.assertEqual(len(scheduled), 3)
        
        for i in range(len(scheduled) - 1):
            self.assertLess(scheduled[i].start_time, scheduled[i+1].start_time)
    
    def test_circular_dependency(self):
        self.scheduler.add_task(name="任务1", duration=30, dependencies=["task_1"])
        self.scheduler.add_task(name="任务2", duration=30, dependencies=["task_0"])
        
        with self.assertRaises(ValueError):
            self.scheduler.topological_sort()
    
    def test_statistics(self):
        self.scheduler.add_task(name="任务1", duration=60)
        self.scheduler.add_task(name="任务2", duration=90)
        self.scheduler.mark_completed("task_0")
        
        stats = self.scheduler.get_statistics()
        self.assertEqual(stats['total_tasks'], 2)
        self.assertEqual(stats['completed_tasks'], 1)
        self.assertEqual(stats['completion_rate'], 50.0)

class TestDurationPredictor(unittest.TestCase):
    def setUp(self):
        self.predictor = DurationPredictor()
    
    def test_predict_without_history(self):
        predicted = self.predictor.predict("新任务")
        self.assertEqual(predicted, 60)
    
    def test_predict_with_history(self):
        self.predictor.add_history("重复任务", 50)
        self.predictor.add_history("重复任务", 55)
        self.predictor.add_history("重复任务", 60)
        
        predicted = self.predictor.predict("重复任务")
        self.assertEqual(predicted, 55)
    
    def test_save_load_model(self):
        self.predictor.add_history("测试任务", 45)
        self.predictor.save_model("test_model.pkl")
        
        new_predictor = DurationPredictor()
        new_predictor.load_model("test_model.pkl")
        
        predicted = new_predictor.predict("测试任务")
        self.assertEqual(predicted, 45)

class TestPriorityCalculator(unittest.TestCase):
    def test_calculate_priority(self):
        task = Task(
            id="task_0",
            name="紧急任务",
            duration=60,
            priority=Priority.URGENT,
            deadline=datetime.now() + timedelta(hours=12)
        )
        
        score = PriorityCalculator.calculate(task, datetime.now())
        self.assertGreater(score, 1.0)

class TestConflictResolver(unittest.TestCase):
    def test_resolve_conflicts(self):
        from task import Task
        
        task1 = Task(
            id="task_0",
            name="任务1",
            duration=60,
            priority=Priority.HIGH
        )
        task1.start_time = datetime.now().replace(hour=9, minute=0)
        task1.end_time = task1.start_time + timedelta(minutes=60)
        
        task2 = Task(
            id="task_1",
            name="任务2",
            duration=60,
            priority=Priority.HIGH
        )
        task2.start_time = datetime.now().replace(hour=9, minute=30)
        task2.end_time = task2.start_time + timedelta(minutes=60)
        
        resolver = ConflictResolver()
        resolved = resolver.resolve_conflicts([task1, task2])
        
        self.assertEqual(len(resolved), 2)
        self.assertGreaterEqual(resolved[1].start_time, resolved[0].end_time)

if __name__ == '__main__':
    unittest.main()
