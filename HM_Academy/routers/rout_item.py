
from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from backend.db import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from models.models import Item
from schemas import CreateItem, UpdateItem
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/item", tags=["item"])

#from fastapi_pagination import Page, add_pagination, paginate
#add_pagination(router)  # Добавляем пагинацию в приложение


@router.get("/")
def all_items(db: Annotated[Session, Depends(get_db)], request: Request) -> HTMLResponse:
    items = db.scalars(select(Item)).all()
    header = "Статьи расходов на содержание и управление общим имуществом МКД"

#    return items
    return templates.TemplateResponse("items.html", {"request":request, "header": header, "items": items} )


@router.get("/item_id")
async def item_by_id(db: Annotated[Session, Depends(get_db)], item_id: int):
    item = db.scalar(select(Item).where(Item.id == item_id))
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item was not found!')
    return item


@router.post("/create")
async def create_item(db: Annotated[Session, Depends(get_db)]
                      , create_item: CreateItem):
    db.execute(insert(Item).values(
        title=create_item.title,
        content=create_item.content,
        sort_num= create_item.sort_num,
        slug=slugify(create_item.title)))

    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}


@router.put("/update")
async def update_item(db: Annotated[Session, Depends(get_db)], item_id: int
                      , update_item: UpdateItem):
    item = db.scalar(select(Item).where(Item.id == item_id))
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item was not found!')

    db.execute(update(Item).where(Item.id == item_id).values(
        title=update_item.title,
        content=update_item.content,
        priority=update_item.priority,
        user_id=update_item.user,
        slug=slugify(update_item.title)))
    db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Item update is successful!'
    }


@router.delete("/delete")
async def delete_item(db: Annotated[Session, Depends(get_db)], item_id: int):
    item = db.scalar(select(Item).where(Item.id == item_id))
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item was not found!')

    db.execute(delete(Item).where(Item.id == item_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Item delete is successful'
    }

