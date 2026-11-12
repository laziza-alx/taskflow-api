from fastapi import FastAPI
from app.routers.users import router as users_router

print(">>> USERS ROUTER IMPORTED <<<")

app = FastAPI(
    title= "TaskFlow API"
)

app.include_router(users_router)

@app.get("/")
def root():
    return {"message": "TaskFlow API 12345"}


