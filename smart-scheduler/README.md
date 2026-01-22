# 🗓️ Smart Scheduler - 智能日程管理系统

一个基于AI和算法优化的智能日程管理系统，采用拓扑排序、优先级调度、机器学习预测等先进技术，实现任务的智能安排和效率优化。

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)
![Code Quality](https://img.shields.io/badge/Code%20Quality-A-yellow.svg)

## ✨ 核心功能

### 🤖 智能调度算法
- **拓扑排序** - 处理复杂的任务依赖关系
- **优先级调度** - 基于紧急度和截止时间优化任务顺序
- **冲突检测与解决** - 自动检测时间冲突并智能调整
- **负载均衡** - 避免任务过度集中，合理分配时间

### ⏱️ 机器学习预测
- **耗时预测模型** - 基于历史数据预测任务完成时间
- **自适应学习** - 随着使用不断优化预测准确性
- **模型持久化** - 保存和加载训练好的模型

### 📊 可视化分析
- **甘特图** - 直观展示任务时间线
- **日历视图** - 按日期查看任务安排
- **效率统计** - 任务完成率、平均耗时等关键指标
- **趋势分析** - 长期工作效率变化趋势

### 🔔 智能提醒系统
- **多级提醒** - 基于任务紧急度设置不同提醒频率
- **自适应提醒** - 根据任务完成情况调整提醒策略
- **多渠道通知** - 支持邮件、桌面通知等

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                   用户界面层                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ CLI界面  │  │ Web界面  │  │ API接口  │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
└───────┼──────────────┼──────────────┼────────────┘
        │              │              │
┌───────┼──────────────┼──────────────┼────────────┐
│       │              │              │            │
│  ┌───▼──────────────▼──────────────▼────┐     │
│  │        业务逻辑层 (Core)            │     │
│  │  ┌──────────────────────────────┐   │     │
│  │  │    TaskScheduler           │   │     │
│  │  │  - 任务管理               │   │     │
│  │  │  - 依赖解析               │   │     │
│  │  │  - 冲突解决               │   │     │
│  │  └──────────────────────────────┘   │     │
│  │  ┌──────────────────────────────┐   │     │
│  │  │    Optimizer              │   │     │
│  │  │  - 拓扑排序               │   │     │
│  │  │  - 优先级计算             │   │     │
│  │  │  - 负载均衡               │   │     │
│  │  └──────────────────────────────┘   │     │
│  │  ┌──────────────────────────────┐   │     │
│  │  │    Predictor             │   │     │
│  │  │  - ML预测模型             │   │     │
│  │  │  - 历史数据管理           │   │     │
│  │  └──────────────────────────────┘   │     │
│  └────────────────────────────────────┘     │
│                                          │
│  ┌────────────────────────────────────┐     │
│  │        数据访问层 (DAL)           │     │
│  │  ┌────────────────────────────┐  │     │
│  │  │  JSONPersistence        │  │     │
│  │  │  - 任务序列化/反序列化     │  │     │
│  │  │  - 模型保存/加载         │  │     │
│  │  └────────────────────────────┘  │     │
│  └────────────────────────────────────┘     │
└────────────────────────────────────────────┘
```

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行应用

```bash
# 交互式CLI
python main.py

# 运行测试
python -m pytest test_scheduler.py -v

# 生成甘特图
python examples/gantt_chart_example.py
```

## 📖 详细使用指南

### 1. 任务管理

```python
from scheduler import TaskScheduler
from task import Priority

# 创建调度器
scheduler = TaskScheduler()

# 添加简单任务
task1 = scheduler.add_task(
    name="完成项目文档",
    description="编写项目的技术文档",
    duration=120,  # 120分钟
    priority=Priority.HIGH,
    deadline=datetime(2024, 1, 25, 18, 0),
    tags=["文档", "项目"]
)

# 添加带依赖的任务
task2 = scheduler.add_task(
    name="代码审查",
    description="审查团队成员提交的代码",
    duration=60,
    priority=Priority.MEDIUM,
    dependencies=[task1.id]  # 依赖任务1
)

# 查看任务
print(f"任务ID: {task1.id}")
print(f"任务名称: {task1.name}")
print(f"优先级: {task1.priority.value}")
```

### 2. 智能调度

```python
# 优化任务顺序
scheduled_tasks = scheduler.optimize()

# 查看优化后的时间表
for task in scheduled_tasks:
    print(f"{task.start_time.strftime('%Y-%m-%d %H:%M')} - {task.end_time.strftime('%H:%M')}")
    print(f"  {task.name} ({task.duration}分钟)")
    print(f"  优先级: {task.priority.value}")
    if task.deadline:
        print(f"  截止时间: {task.deadline.strftime('%Y-%m-%d %H:%M')}")
```

### 3. 机器学习预测

```python
from advanced_features import DurationPredictor

# 创建预测器
predictor = DurationPredictor()

# 添加历史数据
predictor.add_history("编写单元测试", 45)
predictor.add_history("编写单元测试", 50)
predictor.add_history("编写单元测试", 55)

# 预测新任务的耗时
predicted_duration = predictor.predict("编写单元测试")
print(f"预测耗时: {predicted_duration} 分钟")

# 保存模型
predictor.save_model("models/duration_predictor.pkl")

# 加载模型
new_predictor = DurationPredictor()
new_predictor.load_model("models/duration_predictor.pkl")
```

### 4. 冲突解决

```python
from advanced_features import ConflictResolver

# 创建冲突解决器
resolver = ConflictResolver()

# 解决任务时间冲突
resolved_tasks = resolver.resolve_conflicts(
    scheduled_tasks,
    work_hours=(9, 18)  # 工作时间 9:00 - 18:00
)

for task in resolved_tasks:
    print(f"{task.start_time} - {task.name}")
```

### 5. 统计分析

```python
# 获取统计信息
stats = scheduler.get_statistics()

print(f"总任务数: {stats['total_tasks']}")
print(f"已完成: {stats['completed_tasks']}")
print(f"进行中: {stats['in_progress_tasks']}")
print(f"待处理: {stats['pending_tasks']}")
print(f"完成率: {stats['completion_rate']:.1f}%")
print(f"平均耗时: {stats['avg_duration']:.1f} 分钟")
print(f"总时长: {stats['total_duration']} 分钟")

# 查看逾期任务
overdue = scheduler.get_overdue_tasks()
print(f"\n逾期任务: {len(overdue)}")
for task in overdue:
    print(f"  - {task.name} (截止: {task.deadline})")

# 查看即将到期的任务
upcoming = scheduler.get_upcoming_tasks(hours=24)
print(f"\n24小时内到期: {len(upcoming)}")
for task in upcoming:
    print(f"  - {task.name} (截止: {task.deadline})")
```

## 🧪 测试

项目包含完整的单元测试，覆盖核心功能：

```bash
# 运行所有测试
python -m pytest test_scheduler.py -v

# 运行特定测试类
python -m pytest test_scheduler.py::TestTaskScheduler -v

# 查看测试覆盖率
python -m pytest test_scheduler.py --cov=. --cov-report=html
```

测试覆盖：
- ✅ 任务管理（添加、更新、删除）
- ✅ 拓扑排序
- ✅ 依赖关系处理
- ✅ 循环依赖检测
- ✅ 冲突解决
- ✅ 统计计算
- ✅ 数据持久化

## 📊 算法详解

### 拓扑排序 (Topological Sort)

用于处理任务依赖关系，确保依赖的任务先执行。

**时间复杂度：** O(V + E)，V是顶点数，E是边数

**实现原理：**
1. 计算每个任务的入度
2. 将入度为0的任务加入队列
3. 从队列中取出任务，减少其依赖任务的入度
4. 重复直到队列为空

```python
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
        raise ValueError("存在循环依赖")
    
    return result
```

### 优先级计算

综合考虑任务优先级、截止时间、依赖关系等因素。

**评分公式：**

```
Score = Priority_Weight + Deadline_Bonus - Dependency_Penalty

其中：
- Priority_Weight: 紧急=1.0, 高=0.8, 中=0.5, 低=0.3
- Deadline_Bonus: <24h=+0.5, <48h=+0.3, <72h=+0.1
- Dependency_Penalty: 每个依赖-0.05
```

## 🎯 实际应用场景

### 1. 学生学习计划

```python
# 创建学习任务
scheduler.add_task("数学作业", duration=60, priority=Priority.HIGH)
scheduler.add_task("英语阅读", duration=45, priority=Priority.MEDIUM)
scheduler.add_task("编程练习", duration=90, priority=Priority.HIGH)

# 生成学习计划
study_plan = scheduler.optimize()

# 导出为甘特图
generate_gantt_chart(study_plan, "study_plan.png")
```

### 2. 软件项目管理

```python
# 项目任务分解
scheduler.add_task("需求分析", duration=240, priority=Priority.URGENT)
scheduler.add_task("设计文档", duration=180, dependencies=["task_0"])
scheduler.add_task("代码实现", duration=480, dependencies=["task_1"])
scheduler.add_task("单元测试", duration=120, dependencies=["task_2"])
scheduler.add_task("集成测试", duration=180, dependencies=["task_3"])
scheduler.add_task("部署上线", duration=60, dependencies=["task_4"])

# 生成项目时间表
project_schedule = scheduler.optimize()

# 分析项目进度
stats = scheduler.get_statistics()
print(f"项目完成率: {stats['completion_rate']}%")
```

### 3. 团队协作

```python
# 团队任务分配
scheduler.add_task("前端开发", duration=480, assignee="张三")
scheduler.add_task("后端开发", duration=480, assignee="李四")
scheduler.add_task("测试", duration=240, dependencies=["task_0", "task_1"])

# 优化团队协作
team_schedule = scheduler.optimize()

# 生成团队甘特图
generate_team_gantt(team_schedule, "team_schedule.png")
```

## 🔧 配置选项

```python
# config.py
class Config:
    # 工作时间设置
    WORK_START_HOUR = 9
    WORK_END_HOUR = 18
    BREAK_DURATION = 60  # 午休时间
    
    # 任务优先级权重
    PRIORITY_WEIGHTS = {
        "urgent": 1.0,
        "high": 0.8,
        "medium": 0.5,
        "low": 0.3
    }
    
    # 提醒设置
    REMINDER_ADVANCE_TIME = 30  # 提前30分钟提醒
    REMINDER_INTERVALS = {
        "urgent": [1440, 60, 30],  # 1天前、1小时前、30分钟前
        "high": [1440, 60],
        "medium": [1440],
        "low": []
    }
    
    # ML模型设置
    USE_ML_PREDICTION = True
    MODEL_PATH = "models/duration_predictor.pkl"
    HISTORY_LENGTH = 10  # 保留最近10条历史记录
    
    # 调度算法设置
    OPTIMIZATION_STRATEGY = "priority"  # priority, deadline, balanced
    LOAD_BALANCING = True
    CONFLICT_RESOLUTION = "auto"  # auto, manual
```

## 📁 项目结构

```
smart-scheduler/
├── core/
│   ├── scheduler.py          # 核心调度逻辑
│   ├── task.py              # 任务类定义
│   ├── optimizer.py         # 优化算法
│   └── predictor.py        # ML预测模型
├── advanced/
│   ├── advanced_features.py  # 高级功能
│   ├── conflict_resolver.py # 冲突解决
│   └── priority_calc.py    # 优先级计算
├── utils/
│   ├── visualization.py    # 可视化工具
│   ├── reminder.py         # 提醒系统
│   └── statistics.py       # 统计分析
├── models/
│   └── duration_predictor.pkl  # 训练好的模型
├── data/
│   └── tasks.json         # 任务数据
├── tests/
│   └── test_scheduler.py  # 单元测试
├── examples/
│   └── gantt_chart_example.py  # 示例代码
├── main.py                 # 主程序入口
├── config.py               # 配置文件
└── requirements.txt         # 依赖列表
```

## 🎓 技术亮点

### 1. 数据结构与算法

- **有向无环图 (DAG)** - 表示任务依赖关系
- **拓扑排序** - 确保任务执行顺序正确
- **优先队列** - 高效管理待处理任务
- **贪心算法** - 优化任务安排

### 2. 机器学习

- **历史数据学习** - 基于过去数据预测未来
- **滑动窗口** - 保留最近N条记录
- **模型持久化** - 保存训练好的模型

### 3. 软件工程

- **SOLID原则** - 单一职责、开闭原则等
- **设计模式** - 策略模式、工厂模式
- **单元测试** - 完整的测试覆盖
- **类型注解** - 提高代码可读性

## 🔮 未来计划

- [ ] Web界面（React + FastAPI）
- [ ] 移动端应用（React Native）
- [ ] 多用户协作
- [ ] 日历同步（Google Calendar、Outlook）
- [ ] 语音输入任务
- [ ] AI任务推荐
- [ ] 更多可视化图表
- [ ] 云端同步
- [ ] 插件系统

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

感谢以下开源项目：
- [Python](https://www.python.org/)
- [Matplotlib](https://matplotlib.org/)
- [NetworkX](https://networkx.org/)

## 📞 联系方式

- 项目主页: https://github.com/yourusername/smart-scheduler
- 问题反馈: https://github.com/yourusername/smart-scheduler/issues
- 邮箱: your.email@example.com

---

⭐ 如果这个项目对你有帮助，请给个Star！
