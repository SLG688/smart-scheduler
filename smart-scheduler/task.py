from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional, Set
from enum import Enum

class Priority(Enum):
    URGENT = "urgent"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class Task:
    id: str
    name: str
    description: str = ""
    duration: int = 60  # 分钟
    priority: Priority = Priority.MEDIUM
    deadline: Optional[datetime] = None
    dependencies: List[str] = None
    tags: List[str] = None
    completed: bool = False
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.tags is None:
            self.tags = []
    
    def __lt__(self, other):
        priority_order = {
            Priority.URGENT: 0,
            Priority.HIGH: 1,
            Priority.MEDIUM: 2,
            Priority.LOW: 3
        }
        
        if priority_order[self.priority] != priority_order[other.priority]:
            return priority_order[self.priority] < priority_order[other.priority]
        
        if self.deadline and other.deadline:
            return self.deadline < other.deadline
        
        return self.id < other.id
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "duration": self.duration,
            "priority": self.priority.value,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "dependencies": self.dependencies,
            "tags": self.tags,
            "completed": self.completed,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            duration=data.get("duration", 60),
            priority=Priority(data.get("priority", "medium")),
            deadline=datetime.fromisoformat(data["deadline"]) if data.get("deadline") else None,
            dependencies=data.get("dependencies", []),
            tags=data.get("tags", []),
            completed=data.get("completed", False),
            start_time=datetime.fromisoformat(data["start_time"]) if data.get("start_time") else None,
            end_time=datetime.fromisoformat(data["end_time"]) if data.get("end_time") else None
        )
