import sys
import uvicorn
from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

from routers import rout_item, rout_building, rout_expenses
from backend.db import engine, Base

app = FastAPI()

#print(sys.path())

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def welcome(request: Request):
    header = "Welcome to HouseManager"
    cont1 = 'Управляющая организация ООО "Ромашка"'
    cont2 = 'По всем вопросам просьба обращаться по адресу г. Москва, 3-я ул.Строителей, д.1'
    return templates.TemplateResponse("main.html", {"request":request, "header": header, "cont":cont1, "cont2":cont2} )

app.include_router(rout_item.router)
app.include_router(rout_building.router)
app.include_router(rout_expenses.router)

Base.metadata.create_all(engine)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
