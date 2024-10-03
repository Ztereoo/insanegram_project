import base64
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select, insert, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.posts.models import Posts
from src.auth.models import User
from src.auth.base_config import fastapi_users
from src.database import get_async_session
from src.posts.schemas import PostCreate, PostUpdate

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/by_id")
async def get_posts_by_user_id(
        set_id: int = Query(...),
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(fastapi_users.current_user(active=True))):

    query = select(Posts).where(Posts.user_id == set_id)
    result = await session.execute(query)
    posts = result.scalars().all()


    if not posts:
        raise HTTPException(status_code=404, detail=f"No posts found for user_id {set_id}")


    post_list = []
    for post in posts:
        photo_base64 = None
        if post.photo:
            photo_base64 = base64.b64encode(post.photo).decode('utf-8')

        post_list.append({
            "id": post.id,
            "text": post.text,
            "tags": post.tags,
            "photo": photo_base64,
        })

    return post_list


@router.get("/by_name")
async def get_post_by_name(
        get_name: str = Query(...),
        session: AsyncSession = Depends(get_async_session)):

    get_name = get_name.lower()

    query = select(Posts).where(func.lower(Posts.text).contains(get_name))
    result = await session.execute(query)
    posts = result.scalars().all()


    if not posts:
        raise HTTPException(status_code=404, detail=f"No posts match with the word '{get_name}'")

    post_list = []
    for post in posts:
        photo_base64 = None
        if post.photo:
            photo_base64 = base64.b64encode(post.photo).decode('utf-8')

        post_list.append({
            "id": post.id,
            "text": post.text,
            "tags": post.tags,
            "photo": photo_base64,
        })

    return post_list


@router.get('/by_tag')
async def get_post_by_tag(
        get_tag: str = Query(...),
        session: AsyncSession = Depends(get_async_session)):
    get_tag = get_tag.lower()
    query = select(Posts).where(func.lower(Posts.tags).contains(get_tag))
    result = await session.execute(query)
    posts = result.scalars().all()

    if not posts:
        raise HTTPException(status_code=404, detail=f"No tags match with {get_tag}")

    post_list = []
    for post in posts:
        photo_base64 = None
        if post.photo:
            photo_base64 = base64.b64encode(post.photo).decode('utf-8')

        post_list.append({
            "id": post.id,
            "text": post.text,
            "tags": post.tags,
            "photo": photo_base64,
        })

    return post_list

@router.post("/create")
async def add_specific_operations(
        new_post: PostCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(fastapi_users.current_user(active=True))):
    stmt = insert(Posts).values(**new_post.dict())
    await session.execute(stmt)
    await session.commit()

    return f"post successfully added"


@router.patch("/update/")
async def update_post(
        post_id: int = Query(...),
        post_data: PostUpdate = Depends(),
        session=Depends(get_async_session),
        user: User = Depends(fastapi_users.current_user(active=True))):
    query = select(Posts).where(Posts.id == post_id)
    result = await session.execute(query)
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail='Post not found')

    if post_data.text is not None:
        post.text = post_data.text
    if post_data.tags is not None:
        post.tags = post_data.tags
    if post_data.photo is not None:
        post.photo = post_data.photo

    await session.commit()

    return f'Post changed successfully'


@router.get("/delete")
async def delete_post_by_id(
        set_id: int = Query(...),
        session=Depends(get_async_session),
        user: User = Depends(fastapi_users.current_user(superuser=True))):
    query = select(Posts).where(Posts.id == set_id)
    result = await session.execute(query)
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail='No such post in db')

    await session.delete(post)
    await session.commit()
    return f"Post Successfully deleted"
