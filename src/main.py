

from fastapi import FastAPI, Depends,Request,HTTPException
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi_users.schemas import BaseUser

from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate

from src.posts.router import router as posts_operation
from src.pages.router import router as router_pages, templates
from src.auth.models import User


app = FastAPI(
    title="InsaneGram App"
)

app.mount("/static",StaticFiles(directory="src/static"), name="static")



app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth/jwt",
    tags=["Auth"],
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        return templates.TemplateResponse("error.html", {"request": request, "message": exc.detail}, status_code=401)
    return templates.TemplateResponse("error.html", {"request": request, "message": "An error occurred."}, status_code=exc.status_code)

@app.get("/protected")
async def protected_route(user: User = Depends(fastapi_users.current_user(active=True))):
    return {"message": f"Hello {user.email}, you are authorized!"}

app.include_router(posts_operation)
app.include_router(router_pages)



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)