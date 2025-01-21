from pydantic import BaseModel


class CreateBuilding(BaseModel):
    title: str
    number_of_floors: int
    number_of_entrances: int
    number_of_elevators: int
    number_of_chutes: int
    number_of_residents: int
    cleaning_area: float
    residential_area: float


class UpdateBuilding(BaseModel):
    title: str
    number_of_floors: int
    number_of_entrances: int
    number_of_elevators: int
    number_of_chutes: int
    number_of_residents: int
    cleaning_area: float
    residential_area: float


class CreateItem(BaseModel):
    title: str
    content: str
    sort_num: int


class UpdateItem(BaseModel):
    title: str
    content: str
    sort_num: int


class CreateExpenses(BaseModel):
    summ: float
    type: str
    building: int
    item: int

class UpdateExpenses(BaseModel):
    summ: float
    type: str
