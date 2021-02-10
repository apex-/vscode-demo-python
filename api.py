from typing import Optional, List
from collections import OrderedDict
from fastapi import FastAPI, HTTPException
from models import Task, TaskCreateInput, TaskUpdateInput

tasks: OrderedDict = OrderedDict()
app = FastAPI(title="Task List API")

# Create task
@app.post("/tasks", status_code=201)
async def create_task(taskInput: TaskCreateInput):
    current_id = next(reversed(tasks)) + 1 if len(tasks) > 0 else 1
    task = Task(
        id=current_id, 
        title=taskInput.title, 
        description=taskInput.description, 
        done=taskInput.done)
    tasks[task.id] = task
    return task

# List tasks
@app.get("/tasks", response_model=List[Task])
async def list_tasks():
    task_list = list(tasks.values())
    return task_list

# Update task
@app.put("/task/{task_id}", response_model=Task)
async def update_task(task_id: int, taskInput: TaskUpdateInput):
    task = tasks.get(task_id, None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if taskInput.title:
        task.title = taskInput.title
    if taskInput.description:
        task.description = taskInput.description
    if taskInput.done:
        task.done = taskInput.done
    return task

# Delete task
@app.delete("/task/{task_id}", status_code=204)
async def delete_task(task_id: int):
    task = tasks.pop(task_id, None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {}
