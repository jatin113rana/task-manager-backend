from app.database import engine, Base
from app.models.user import User, attach_user_relationships
from app.models.task import Task

# Make sure relationships are attached
attach_user_relationships(Task)

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
