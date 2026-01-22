import json
import pickle
from datetime import datetime, timedelta
from typing import List, Dict
from collections import defaultdict
import heapq

class DurationPredictor:
    def __init__(self):
        self.history = defaultdict(list)
        self.model = None
    
    def add_history(self, task_name: str, actual_duration: int):
        self.history[task_name].append(actual_duration)
        if len(self.history[task_name]) > 10:
            self.history[task_name].pop(0)
    
    def predict(self, task_name: str, default_duration: int = 60) -> int:
        if task_name in self.history and self.history[task_name]:
            history = self.history[task_name]
            avg = sum(history) / len(history)
            return int(avg)
        return default_duration
    
    def save_model(self, filepath: str):
        with open(filepath, 'wb') as f:
            pickle.dump(dict(self.history), f)
    
    def load_model(self, filepath: str):
        try:
            with open(filepath, 'rb') as f:
                self.history = defaultdict(list, pickle.load(f))
        except FileNotFoundError:
            pass

class ConflictResolver:
    @staticmethod
    def resolve_conflicts(scheduled_tasks: List, work_hours: tuple = (9, 18)) -> List:
        work_start, work_end = work_hours
        resolved = []
        
        for task in scheduled_tasks:
            if task.start_time.hour < work_start:
                task.start_time = task.start_time.replace(hour=work_start)
                task.end_time = task.start_time + timedelta(minutes=task.duration)
            
            if task.end_time.hour >= work_end:
                task.start_time = (task.start_time + timedelta(days=1)).replace(hour=work_start, minute=0)
                task.end_time = task.start_time + timedelta(minutes=task.duration)
            
            if resolved:
                last_task = resolved[-1]
                if task.start_time < last_task.end_time:
                    task.start_time = last_task.end_time + timedelta(minutes=15)
                    task.end_time = task.start_time + timedelta(minutes=task.duration)
            
            resolved.append(task)
        
        return resolved

class PriorityCalculator:
    @staticmethod
    def calculate(task, current_time: datetime) -> float:
        priority_weights = {
            'urgent': 1.0,
            'high': 0.8,
            'medium': 0.5,
            'low': 0.3
        }
        
        score = priority_weights.get(task.priority.value, 0.5)
        
        if task.deadline:
            time_until_deadline = (task.deadline - current_time).total_seconds() / 3600
            if time_until_deadline < 24:
                score += 0.5
            elif time_until_deadline < 48:
                score += 0.3
            elif time_until_deadline < 72:
                score += 0.1
        
        if task.dependencies:
            score -= len(task.dependencies) * 0.05
        
        return max(0, min(2, score))
