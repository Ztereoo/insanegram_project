from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select, insert, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.posts.models import Posts
from src.database import get_async_session

from src.posts.schemas import OperationCreate

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/by_id")
async def get_posts_by_id(
        set_id: int = Query(...),
        session: AsyncSession = Depends(get_async_session)):
    query = select(Posts).where(Posts.user_id == set_id)
    result = await session.execute(query)
    posts = result.scalars().all()

    if not posts:
        raise HTTPException(status_code=404, detail=f"No user with {set_id} id found")
    return posts


@router.get("/by_name")
async def get_post_by_name(
        get_name: str = Query(...),
        session: AsyncSession = Depends(get_async_session)):
    get_name = get_name.lower()
    query = select(Posts).where(func.lower(Posts.text).contains(get_name))
    result = await session.execute(query)
    posts = result.scalars().all()

    if not posts:
        raise HTTPException(status_code=404, detail=f"No posts matches with word {get_name}")
    return posts


@router.get('/by_tag')
async def get_post_by_tag(
        get_tag: str = Query(...),
        session: AsyncSession = Depends(get_async_session)):
    get_tag = get_tag.lower()
    query = select(Posts).where(func.lower(Posts.tags).contains(get_tag))
    result = await session.execute(query)
    posts = result.scalars().all()

    if not posts:
        raise HTTPException(status_code=404, detail=f"No tags matches with {get_tag}")

    return posts


@router.post("/")
async def add_specific_operations():
    pass
