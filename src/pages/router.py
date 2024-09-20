from fastapi import APIRouter, Request, Form, Depends,File,UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.posts.models import Posts




router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="src/templates")

# Обработчик для получения формы
@router.get("/create_post", response_class=HTMLResponse)
async def get_create_post(request: Request):
    return templates.TemplateResponse('create_post.html', {"request": request})

# Обработчик для создания нового поста
@router.post("/create_post", response_class=HTMLResponse)
async def create_new_post(
    request: Request,
    title: str = Form(...),
    tags: str = Form(...),
    photo: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session)
):
    photo_data = await photo.read()

    new_post = Posts(
        text=title,
        tags=tags.split(','),
        photo=photo_data,
        user_id=1  # Замените на актуальный ID пользователя
    )

    session.add(new_post)
    await session.commit()

    return templates.TemplateResponse('create_post.html', {"request": request, "message": "Post successfully created!"})