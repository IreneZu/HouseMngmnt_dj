import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///db_academy.db')

df = pd.read_csv('files/expenses.csv', encoding="cp1251", sep=";")

df.to_sql('specifications_expenses', engine, index=False, if_exists='replace')

with engine.connect() as connection:
    query = text("SELECT * FROM specifications_expenses")
    result = connection.execute(query).fetchall()
    print(result)
