from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from backend.db import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from models.models import Building
from schemas import CreateBuilding, UpdateBuilding
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/building", tags=["building"])


@router.get("/")
def all_buildings(db: Annotated[Session, Depends(get_db)], request: Request):
    buildings = db.scalars(select(Building)).all()
#    print(buildings)
    header = 'Многоквартирные дома в управлении ООО "Ромашка"'
    return templates.TemplateResponse("buildings.html", {"request": request, "header": header, "buildings": buildings})
#    return buildings



@router.get("/building_id", response_class=HTMLResponse)
def building_by_id(db: Annotated[Session, Depends(get_db)], request: Request, building_id: int):
    building = db.scalar(select(Building).where(Building.id == building_id))
    if building is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Building was not found!')
    header = f'Характеристики МКД:  {building.title}'
    return templates.TemplateResponse("building_spec.html", {"request": request, "header": header, "building": building})


@router.post("/create")
async def create_building(db: Annotated[Session, Depends(get_db)]
                      , create_building: CreateBuilding):
    db.execute(insert(Building).values(
        title=create_building.title,
        number_of_floors=create_building.number_of_floors,
        number_of_entrances=create_building.number_of_entrances,
        number_of_elevators=create_building.number_of_elevators,
        number_of_chutes=create_building.number_of_chutes,
        number_of_residents=create_building.number_of_residents,
        cleaning_area=create_building.cleaning_area,
        residential_area=create_building.residential_area
        #        slug=slugify(update_building.title)
    ))

    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}


@router.put("/update")
async def update_building(db: Annotated[Session, Depends(get_db)], building_id: int
                      , update_building: UpdateBuilding):
    building = db.scalar(select(Building).where(Building.id == building_id))
    if building is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Building was not found!')

    db.execute(update(Building).where(Building.id == building_id).values(
        title=update_building.title,
        number_of_floors=update_building.number_of_floors,
        number_of_entrances=update_building.number_of_entrances,
        number_of_elevators=update_building.number_of_elevators,
        number_of_chutes=update_building.number_of_chutes,
        number_of_residents=update_building.number_of_residents,
        cleaning_area=update_building.cleaning_area,
        residential_area=update_building.residential_area
        #        slug=slugify(update_building.title)
        ))
    db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Building update is successful!'
    }


@router.delete("/delete")
async def delete_building(db: Annotated[Session, Depends(get_db)], building_id: int):
    building = db.scalar(select(Building).where(Building.id == building_id))
    if building is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Building was not found!')

    db.execute(delete(Building).where(Building.id == building_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Building delete is successful'
    }


