# Task Manager Backend

This is the backend for the **Task Manager** application built using **FastAPI** and **MySQL**. It provides RESTful APIs for user authentication, task management, and other related operations.

---

## Features

- User registration and login with **JWT authentication**   //Not in use for now
- CRUD operations for tasks
- Role-based access (Admin/User)
- Connected to a **MySQL database** (hosted)
- CORS enabled for frontend integration

---

## Tech Stack

- **Backend Framework:** FastAPI  
- **Database:** MySQL (hosted on Railway)  
- **ORM:** SQLAlchemy  
- **Authentication:** JWT via `python-jose`  //Not in use for now
- **Password Hashing:** Bcrypt & Passlib  
- **Environment Management:** Python `venv` & `.env`  
- **Server:** Uvicorn  

---

## Getting Started

### Prerequisites

- Python 3.11+
- MySQL database (or Railway hosted)
- Git
