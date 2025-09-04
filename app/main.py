from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.tasks import router as tasks_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Allow all origins, methods, and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all domains
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(auth_router)
app.include_router(tasks_router)


@app.get("/")
def root():
    return {"message": "FastAPI Task Manager API is running"}
