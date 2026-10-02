from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import auth, users, schedules, shifts, leaves, holidays, messages, visitors

app = FastAPI(title="Shift Schedule Management API")

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]
if settings.FRONTEND_URL and settings.FRONTEND_URL not in origins:
    origins.append(settings.FRONTEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers already have their own prefix defined
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(schedules.router)
app.include_router(shifts.router)
app.include_router(leaves.router)
app.include_router(holidays.router)
app.include_router(messages.router)
app.include_router(visitors.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
