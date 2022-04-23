# ===================================================={ all imports }============================================================

from fastapi import FastAPI

from .database import engine
from . import models as models
from .routes import users, token, exercise, course, task, attempt, results
from fastapi.middleware.cors import CORSMiddleware


# ==================================================={ global objects }==========================================================

app = FastAPI()  # FastAPI object

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(bind=engine)  # creating database

# ==================================================={ All the routes }==========================================================

app.include_router(attempt.router, prefix="/attempt", tags=["Attempt"])
app.include_router(course.router, prefix="/course", tags=["Course"])
app.include_router(exercise.router, prefix="/exercise", tags=["Exercise"])
app.include_router(task.router, prefix="/task", tags=["Task"])
app.include_router(token.router, prefix="/token", tags=["Token"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(results.router, prefix="/results", tags=["results"])

# ==================================================={ code ends here }==========================================================
