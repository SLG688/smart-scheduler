import json
import heapq
from datetime import datetime, timedelta
from typing import List, Dict, Set
from collections import defaultdict, deque
from task import Task, Priority

class TaskScheduler:
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.task_counter = 0
        self.work_start_hour = 9
        self.work_end_hour = 18
        self.break_duration = 60  # 分钟
    
    def add_task(self, **kwargs) -> Task:
        task_id = f"task_{self.task_counter}"
        self.task_counter += 1
        
        if 'id' not in kwargs:
            kwargs['id'] = task_id
        
        task = Task(**kwargs)
        self.tasks[task.id] = task
        return task
    
    def get_task(self, task_id: str) -> Task:
        return self.tasks.get(task_id)
    
    def update_task(self, task_id: str, **kwargs):
        task = self.get_task(task_id)
        if task:
            for key, value in kwargs.items():
                if hasattr(task, key):
                    setattr(task, key, value)
    
    def delete_task(self, task_id: str):
        if task_id in self.tasks:
            del self.tasks[task_id]
    
    def build_dependency_graph(self) -> Dict[str, List[str]]:
        graph = defaultdict(list)
        for task_id, task in self.tasks.items():
            for dep in task.dependencies:
                graph[dep].append(task_id)
        return graph
    
    def topological_sort(self) -> List[str]:
        in_degree = defaultdict(int)
        graph = self.build_dependency_graph()
        
        for task_id in self.tasks:
            in_degree[task_id] = len(self.tasks[task_id].dependencies)
        
        queue = deque([task_id for task_id in self.tasks if in_degree[task_id] == 0])
        result = []
        
        while queue:
            task_id = queue.popleft()
            result.append(task_id)
            
            for neighbor in graph[task_id]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        if len(result) != len(self.tasks):
            raise ValueError("存在循环依赖，无法完成任务调度")
        
        return result
    
    def calculate_priority_score(self, task: Task) -> float:
        priority_weights = {
            Priority.URGENT: 1.0,
            Priority.HIGH: 0.8,
            Priority.MEDIUM: 0.5,
            Priority.LOW: 0.3
        }
        
        score = priority_weights[task.priority]
        
        if task.deadline:
            time_until_deadline = (task.deadline - datetime.now()).total_seconds() / 3600
            if time_until_deadline < 24:
                score += 0.5
            elif time_until_deadline < 48:
                score += 0.3
        
        return score
    
    def optimize(self, start_date: datetime = None) -> List[Task]:
        if start_date is None:
            start_date = datetime.now().replace(minute=0, second=0, microsecond=0)
        
        sorted_task_ids = self.topological_sort()
        tasks = [self.tasks[tid] for tid in sorted_task_ids]
        
        current_time = start_date.replace(hour=self.work_start_hour)
        scheduled_tasks = []
        
        for task in tasks:
            if task.completed:
                continue
            
            task.start_time = current_time
            task.end_time = current_time + timedelta(minutes=task.duration)
            
            scheduled_tasks.append(task)
            
            current_time = task.end_time + timedelta(minutes=15)
            
            if current_time.hour >= self.work_end_hour:
                current_time = (current_time + timedelta(days=1)).replace(
                    hour=self.work_start_hour,
                    minute=0,
                    second=0,
                    microsecond=0
                )
        
        return scheduled_tasks
    
    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        return [task for task in self.tasks.values() if task.priority == priority]
    
    def get_overdue_tasks(self) -> List[Task]:
        now = datetime.now()
        return [
            task for task in self.tasks.values()
            if task.deadline and task.deadline < now and not task.completed
        ]
    
    def get_upcoming_tasks(self, hours: int = 24) -> List[Task]:
        now = datetime.now()
        future = now + timedelta(hours=hours)
        
        return [
            task for task in self.tasks.values()
            if task.deadline and now <= task.deadline <= future and not task.completed
        ]
    
    def mark_completed(self, task_id: str):
        task = self.get_task(task_id)
        if task:
            task.completed = True
    
    def get_statistics(self) -> Dict:
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks.values() if task.completed)
        in_progress = sum(1 for task in self.tasks.values() 
                         if not task.completed and task.start_time and task.start_time <= datetime.now())
        
        total_duration = sum(task.duration for task in self.tasks.values())
        completed_duration = sum(task.duration for task in self.tasks.values() if task.completed)
        
        return {
            "total_tasks": total,
            "completed_tasks": completed,
            "in_progress_tasks": in_progress,
            "pending_tasks": total - completed - in_progress,
            "completion_rate": (completed / total * 100) if total > 0 else 0,
            "total_duration": total_duration,
            "completed_duration": completed_duration,
            "avg_duration": total_duration / total if total > 0 else 0
        }
    
    def export_to_json(self, filepath: str):
        data = {
            "tasks": [task.to_dict() for task in self.tasks.values()],
            "exported_at": datetime.now().isoformat()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def import_from_json(self, filepath: str):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.tasks = {}
        for task_data in data["tasks"]:
            task = Task.from_dict(task_data)
            self.tasks[task.id] = task
        
        self.task_counter = max(int(task.id.split('_')[1]) for task in self.tasks.values()) + 1
    
    def clear_all(self):
        self.tasks = {}
        self.task_counter = 0
