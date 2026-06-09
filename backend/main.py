from fastapi import FastAPI
from routers import sessions, sets, exercises, users

app = FastAPI()

app.include_router(sessions.router)
app.include_router(sets.router)
app.include_router(exercises.router)
app.include_router(users.router)