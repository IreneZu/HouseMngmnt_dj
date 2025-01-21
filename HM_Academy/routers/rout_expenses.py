from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from backend.db import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from models.models import Expenses, Building, Item
from schemas import CreateItem, CreateExpenses, UpdateExpenses, UpdateItem, UpdateExpenses
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get("/")
def all_expenses(db: Annotated[Session, Depends(get_db)]):
    expenses = db.scalars(select(Expenses)).all()

    return expenses


@router.get("/build_id/item_id")
def expenses_by_build_item_id(db: Annotated[Session, Depends(get_db)], build_id: int, item_id: int):
    expenses = db.scalar(select(Expenses).where(Expenses.building_id == build_id and Expenses.item_id == item_id))
    if expenses is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Expenses was not found!')
    return expenses

@router.get("/build_id")
def expenses_by_build_id(db: Annotated[Session, Depends(get_db)], request: Request, build_id: int):
    building = db.scalar(select(Building).where(Building.id == build_id))
    header = f'Плановые расходы по дому {building.title}'

    subq = select(Expenses).filter(Expenses.building_id==build_id).subquery()

    exp_query = select(Item).outerjoin(subq, subq.c.item_id==Item.id).add_columns(subq.c.summ, subq.c.type)
    #.filter(building_id==build_id or Expenses is None))

    expenses = db.execute(exp_query).all()
    #print('expenses = \n' , expenses)
    exp_list = []
    exp_sum = 0
    for exp in expenses:
        a = {}
        a['item_id']    = exp[0].id
        a['title']      = exp[0].title
        a['summ']    = 0.0 if exp[1] is None else exp[1]
        a['type']    = 'месяц' if exp[2] is None else exp[2]
        exp_list.append(a)
        exp_sum += a['summ']
#    print('exp_list = \n', exp_list)
#    print('exp_sum = ', exp_sum)

    if expenses is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Expenses was not found!')

#    return exp_list
    return templates.TemplateResponse("exps_view.html", {"request": request, "header": header, "summa": exp_sum, "expenses": exp_list})


@router.post("/create")
def create_expenses(db: Annotated[Session, Depends(get_db)]
                      , create_expenses: CreateExpenses):
    building = db.scalar(select(Building).where(Building.id == create_expenses.building))
    if building is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Building was not found!')
    item = db.scalar(select(Item).where(Item.id == create_expenses.item))
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item was not found!')
    exp_found = db.scalars(select(Expenses).where(Expenses.building_id == create_expenses.building and Expenses.item_id == create_expenses.item)).all()
    if exp_found:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail='Use update function instead!')
    db.execute(insert(Expenses).values(
        summ=create_expenses.summ,
        type=create_expenses.type,
        building_id=create_expenses.building,
        item_id=create_expenses.item))

    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}


@router.put("/update")
def update_expenses(db: Annotated[Session, Depends(get_db)], build_id: int, item_id: int
                      , update_expenses: UpdateExpenses):
    expenses = db.scalar(select(Expenses).where(Expenses.building_id == build_id
                                                  and Expenses.item_id == item_id))
    if expenses is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Expenses was not found!')

    db.execute(update(Expenses).where(Expenses.building_id == build_id
                                                  and Expenses.item_id == item_id).values(
        summ=update_expenses.summ,
        type=update_expenses.type))
    db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Expenses update is successful!'
    }


@router.delete("/delete")
def delete_expenses(db: Annotated[Session, Depends(get_db)], expenses_id: int):
    expenses = db.scalar(select(Expenses).where(Expenses.id == expenses_id))
    if expenses is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Expenses was not found!')

    db.execute(delete(Expenses).where(Expenses.id == expenses_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Expenses delete is successful'
    }

import datetime
@router.get("/test")
def test(db: Annotated[Session, Depends(get_db)]):
    t1 = datetime.datetime.now()
    tsum = 0
    for i in range(1,501):
        expenses = db.scalar(select(Expenses).where(Expenses.id == i))
        tsum += expenses.summ

    t2 = datetime.datetime.now()

    res = (f'get object : SQLAlchemy req/seq: {500 / (t2 - t1).total_seconds()}, '
           f'req time (ms): {(t2 - t1).total_seconds() * 1000 / 500}')
    print(f'tsum = {tsum}')
    print(res)
    return res

# Response body
# echo=True
# "get object : SQLAlchemy req/seq: 1707.5044821992658, req time (ms): 0.58565"
# echo=False -
# "get object : SQLAlchemy req/seq: 2552.7526331643408, req time (ms): 0.391734"
