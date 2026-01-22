#!/usr/bin/env python3
from scheduler import TaskScheduler
from task import Priority
from datetime import datetime, timedelta
import json

def main():
    print("=" * 60)
    print("🗓️  智能日程管理系统")
    print("=" * 60)
    
    scheduler = TaskScheduler()
    
    while True:
        print("\n" + "=" * 60)
        print("请选择操作:")
        print("1. 添加任务")
        print("2. 查看所有任务")
        print("3. 优化日程")
        print("4. 标记任务完成")
        print("5. 查看统计信息")
        print("6. 导出任务")
        print("7. 导入任务")
        print("8. 退出")
        print("=" * 60)
        
        choice = input("\n请输入选项 (1-8): ").strip()
        
        if choice == "1":
            add_task_menu(scheduler)
        elif choice == "2":
            list_tasks(scheduler)
        elif choice == "3":
            optimize_schedule(scheduler)
        elif choice == "4":
            complete_task_menu(scheduler)
        elif choice == "5":
            show_statistics(scheduler)
        elif choice == "6":
            export_tasks(scheduler)
        elif choice == "7":
            import_tasks(scheduler)
        elif choice == "8":
            print("\n感谢使用智能日程管理系统！")
            break
        else:
            print("\n无效选项，请重新选择")

def add_task_menu(scheduler: TaskScheduler):
    print("\n" + "-" * 60)
    print("添加新任务")
    print("-" * 60)
    
    name = input("任务名称: ").strip()
    if not name:
        print("任务名称不能为空！")
        return
    
    description = input("任务描述 (可选): ").strip()
    
    try:
        duration = int(input("预计耗时 (分钟, 默认60): ").strip() or "60")
    except ValueError:
        duration = 60
        print("使用默认时长: 60分钟")
    
    print("\n优先级:")
    print("1. 紧急 (urgent)")
    print("2. 高 (high)")
    print("3. 中 (medium)")
    print("4. 低 (low)")
    
    priority_map = {
        "1": Priority.URGENT,
        "2": Priority.HIGH,
        "3": Priority.MEDIUM,
        "4": Priority.LOW
    }
    
    priority_choice = input("选择优先级 (默认3): ").strip() or "3"
    priority = priority_map.get(priority_choice, Priority.MEDIUM)
    
    deadline_str = input("截止时间 (格式: YYYY-MM-DD HH:MM, 可选): ").strip()
    deadline = None
    if deadline_str:
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
        except ValueError:
            print("时间格式错误，忽略截止时间")
    
    tags_str = input("标签 (用逗号分隔, 可选): ").strip()
    tags = [tag.strip() for tag in tags_str.split(",")] if tags_str else []
    
    task = scheduler.add_task(
        name=name,
        description=description,
        duration=duration,
        priority=priority,
        deadline=deadline,
        tags=tags
    )
    
    print(f"\n✅ 任务已添加！ID: {task.id}")

def list_tasks(scheduler: TaskScheduler):
    print("\n" + "-" * 60)
    print("任务列表")
    print("-" * 60)
    
    if not scheduler.tasks:
        print("暂无任务")
        return
    
    for task in scheduler.tasks.values():
        status = "✓" if task.completed else "○"
        priority_emoji = {
            Priority.URGENT: "🔴",
            Priority.HIGH: "🟠",
            Priority.MEDIUM: "🟡",
            Priority.LOW: "🟢"
        }
        
        print(f"\n{status} {priority_emoji.get(task.priority, '')} {task.name}")
        print(f"   ID: {task.id}")
        print(f"   时长: {task.duration} 分钟")
        print(f"   优先级: {task.priority.value}")
        
        if task.deadline:
            print(f"   截止: {task.deadline.strftime('%Y-%m-%d %H:%M')}")
        
        if task.tags:
            print(f"   标签: {', '.join(task.tags)}")
        
        if task.dependencies:
            print(f"   依赖: {', '.join(task.dependencies)}")

def optimize_schedule(scheduler: TaskScheduler):
    print("\n" + "-" * 60)
    print("优化日程")
    print("-" * 60)
    
    try:
        scheduled_tasks = scheduler.optimize()
        
        print("\n优化后的日程安排:\n")
        
        current_date = None
        for task in scheduled_tasks:
            if task.start_time.date() != current_date:
                current_date = task.start_time.date()
                print(f"\n📅 {current_date.strftime('%Y年%m月%d日')}")
                print("-" * 40)
            
            start_str = task.start_time.strftime('%H:%M')
            end_str = task.end_time.strftime('%H:%M')
            
            print(f"{start_str} - {end_str} | {task.name} ({task.duration}分钟)")
        
        print("\n✅ 日程优化完成！")
        
    except ValueError as e:
        print(f"\n❌ 优化失败: {e}")

def complete_task_menu(scheduler: TaskScheduler):
    print("\n" + "-" * 60)
    print("标记任务完成")
    print("-" * 60)
    
    task_id = input("请输入任务ID: ").strip()
    
    if task_id in scheduler.tasks:
        scheduler.mark_completed(task_id)
        print(f"\n✅ 任务 {task_id} 已标记为完成")
    else:
        print(f"\n❌ 未找到任务 {task_id}")

def show_statistics(scheduler: TaskScheduler):
    print("\n" + "-" * 60)
    print("统计信息")
    print("-" * 60)
    
    stats = scheduler.get_statistics()
    
    print(f"\n总任务数: {stats['total_tasks']}")
    print(f"已完成: {stats['completed_tasks']}")
    print(f"进行中: {stats['in_progress_tasks']}")
    print(f"待处理: {stats['pending_tasks']}")
    print(f"完成率: {stats['completion_rate']:.1f}%")
    print(f"总时长: {stats['total_duration']} 分钟")
    print(f"已完成时长: {stats['completed_duration']} 分钟")
    print(f"平均时长: {stats['avg_duration']:.1f} 分钟")
    
    overdue = scheduler.get_overdue_tasks()
    if overdue:
        print(f"\n⚠️  逾期任务: {len(overdue)}")
        for task in overdue:
            print(f"   - {task.name} (截止: {task.deadline.strftime('%Y-%m-%d %H:%M')})")

def export_tasks(scheduler: TaskScheduler):
    filepath = input("请输入导出文件路径 (默认: tasks.json): ").strip() or "tasks.json"
    
    try:
        scheduler.export_to_json(filepath)
        print(f"\n✅ 任务已导出到 {filepath}")
    except Exception as e:
        print(f"\n❌ 导出失败: {e}")

def import_tasks(scheduler: TaskScheduler):
    filepath = input("请输入导入文件路径: ").strip()
    
    try:
        scheduler.import_from_json(filepath)
        print(f"\n✅ 任务已从 {filepath} 导入")
        print(f"共导入 {len(scheduler.tasks)} 个任务")
    except FileNotFoundError:
        print(f"\n❌ 文件不存在: {filepath}")
    except Exception as e:
        print(f"\n❌ 导入失败: {e}")

if __name__ == "__main__":
    main()
