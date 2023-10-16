from fastapi import FastAPI
from app.routers import accounts, messages


# CREATES CONNECTION TO FAST API AND DESIGNES IT
app = FastAPI(
    title="Guestbook API",
    version="0.1.0",
    description="A place to leave your suggestions..."
)

app.include_router(accounts.router)
app.include_router(messages.router)