from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(50), unique=True, index=True, nullable=False)
    role = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)

    # Relationships will be attached later to avoid circular imports
def attach_user_relationships(Task):
    User.tasks_created = relationship(
        "Task",
        foreign_keys=[Task.created_by],
        back_populates="creator"
    )
    User.tasks_modified = relationship(
        "Task",
        foreign_keys=[Task.modified_by],
        back_populates="modifier"
    )
