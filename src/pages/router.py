import base64
from fastapi import APIRouter, Request, Form, Depends, File, UploadFile, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from PIL import Image
from io import BytesIO

from src.auth.base_config import fastapi_users
from src.auth.models import User
from src.database import get_async_session
from src.posts.models import Posts
from src.posts.router import get_post_by_tag

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="src/templates")


def b64encode(value: bytes) -> str:
    return base64.b64encode(value).decode('utf-8')


templates.env.filters['b64encode'] = b64encode


def resize_image(image_data: bytes, max_width=600) -> bytes:
    image = Image.open(BytesIO(image_data))

    format = image.format
    if format is None:
        format = "JPG"

    width, height = image.size

    if width > height:
        new_width = max_width
        new_height = int((new_width / width) * height)
    else:
        new_height = max_width
        new_width = int((new_height / height) * width)

    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    output = BytesIO()
    image.save(output, format=format)
    return output.getvalue()


@router.get("/create_post", response_class=HTMLResponse)
async def get_create_post(request: Request):
    return templates.TemplateResponse('create_post.html', {"request": request})


@router.post("/create_post", response_class=HTMLResponse)
async def create_new_post(
        request: Request,
        title: str = Form(...),
        tags: str = Form(...),
        photo: UploadFile = File(...),
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(fastapi_users.current_user(active=True))
):
    photo_data = await photo.read()
    resized_photo = resize_image(photo_data)

    new_post = Posts(
        text=title,
        tags=tags.split(','),
        photo=resized_photo,
        user_id= user.id
    )

    session.add(new_post)
    await session.commit()

    return templates.TemplateResponse('create_post.html', {"request": request, "message": "Post successfully created!"})

@router.get("/show_posts", response_class=HTMLResponse)
async def show_posts(
        request: Request,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(fastapi_users.current_user(active=True))):
    if user is None:
        raise HTTPException(status_code=401, detail="You need to log in to see the page")

    query = select(Posts)
    result = await session.execute(query)
    posts = result.scalars().all()
    return templates.TemplateResponse('show_posts.html', {"request": request, "posts": posts,})

@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse('login.html', {"request": request})


@router.post("/auth/jwt/login", response_class=HTMLResponse)
async def login(
        request: Request,
        user: User = Depends(fastapi_users.current_user(active=True))):
    if user:
        return RedirectResponse(url="/show_posts", status_code=303)
    else:
        return templates.TemplateResponse('error.html', {"request": request, "message": "Invalid credentials"})

@router.post("/search", response_class=HTMLResponse)
async def return_search(request: Request, tag: str = Form(...), session: AsyncSession = Depends(get_async_session)):
    posts = await get_post_by_tag(tag, session)
    if posts:
        return templates.TemplateResponse('search.html', {"request": request, "posts": posts})
    else:
        message = "No posts found for the given tag."
        return templates.TemplateResponse('search.html', {"request": request, "posts": [], "message": message})

