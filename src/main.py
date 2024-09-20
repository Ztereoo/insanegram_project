from fastapi import FastAPI
import uvicorn

from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate

from src.posts.router import router as posts_operation


app = FastAPI(
    title="InsaneGram App"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(posts_operation)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)