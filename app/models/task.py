from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.user import User, attach_user_relationships

class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, index=True)
    task = Column(String(255), nullable=False)

    # Use Integer to match user_id type
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    modified_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships back to User
    creator = relationship("User", foreign_keys=[created_by], back_populates="tasks_created")
    modifier = relationship("User", foreign_keys=[modified_by], back_populates="tasks_modified")

# Attach relationships to User after Task is defined
attach_user_relationships(Task)
