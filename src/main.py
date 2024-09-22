from fastapi import FastAPI
import uvicorn
from fastapi.staticfiles import StaticFiles

from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate

from src.posts.router import router as posts_operation
from src.pages.router import router as router_pages


app = FastAPI(
    title="InsaneGram App"
)

app.mount("/static",StaticFiles(directory="src/static"), name="static")

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
app.include_router(router_pages)




if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)