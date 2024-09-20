from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="src/templates")

@router.post("/create_post", response_class=HTMLResponse)
async def create_new_post(request: Request):
    return templates.TemplateResponse('create_post.html', {"request": request})

