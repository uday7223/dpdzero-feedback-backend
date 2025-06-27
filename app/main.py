from fastapi import FastAPI
from app.routers import users, feedback, dashboard
from app.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="DPDZero Feedback API")

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] for all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include routers
app.include_router(users.router)
app.include_router(feedback.router)
app.include_router(dashboard.router)

# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the DPDZero Feedback System API"}
