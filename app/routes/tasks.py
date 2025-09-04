from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.task import Task
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# ---------------------------
# Pydantic Models
# ---------------------------
class TaskRequest(BaseModel):
    task: str = Field(..., min_length=1, max_length=500)
    user_id: int  # Who is performing the action

class TaskResponse(BaseModel):
    task_id: int
    task: str
    created_by: str
    modified_by: str = None
    created_at: datetime
    modified_at: datetime = None

# ---------------------------
# Helper Functions
# ---------------------------
def get_user(user_id: int, db: Session):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

def get_task(task_id: int, db: Session):
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

# ---------------------------
# Routes
# ---------------------------

# Create Task (Admin only)
@router.post("/", response_model=TaskResponse)
def create_task(request: TaskRequest, db: Session = Depends(get_db)):
    user = get_user(request.user_id, db)
    if user.role.lower() != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin can create tasks")
    # return {"message": "Only admin can create tasks"}

    new_task = Task(
        task=request.task,
        created_by=user.user_id,
        modified_by=user.user_id,
        created_at=datetime.utcnow(),
        modified_at=datetime.utcnow()
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return TaskResponse(
        task_id=new_task.task_id,
        task=new_task.task,
        created_by=new_task.creator.user_name,
        modified_by=new_task.modifier.user_name,
        created_at=new_task.created_at,
        modified_at=new_task.modified_at
    )

# Update Task (any logged-in user)
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, request: TaskRequest, db: Session = Depends(get_db)):
    print("Request Data:", request)
    task = get_task(task_id, db)
    user = get_user(request.user_id, db)

    task.task = request.task
    task.modified_by = user.user_id
    task.modified_at = datetime.utcnow()
    db.commit()
    db.refresh(task)

    return TaskResponse(
        task_id=task.task_id,
        task=task.task,
        created_by=task.creator.user_name,
        modified_by=task.modifier.user_name,
        created_at=task.created_at,
        modified_at=task.modified_at
    )

# Delete Task (Admin only)
@router.delete("/{task_id}")
def delete_task(task_id: int, user_id: int, db: Session = Depends(get_db)):
    user = get_user(user_id, db)
    if user.role.lower() != "admin":
        return {"message": "Only admin can delete tasks"}

    task = get_task(task_id, db)
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}

# Get All Tasks
@router.get("/", response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    response = [
        TaskResponse(
            task_id=t.task_id,
            task=t.task,
            created_by=t.creator.user_name,
            modified_by=t.modifier.user_name if t.modifier else None,
            created_at=t.created_at,
            modified_at=t.modified_at
        ) for t in tasks
    ]
    return response
