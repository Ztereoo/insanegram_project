from fastapi import APIRouter, Depends,Query
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.posts.models import Posts
from src.database import get_async_session

from src.posts.schemas import OperationCreate

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/")
async def get_specific_posts(
        set_id: int = Query(...),
        session: AsyncSession = Depends(get_async_session)):
    query = select(Posts).where(Posts.user_id == set_id)
    result = await session.execute(query)
    posts= result.scalars().all()
    return [post for post in posts]


@router.post("/")
async def add_specific_operations():
    pass
