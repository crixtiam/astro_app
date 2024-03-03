import uvicorn
from src.read_document import read_csv
from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated, List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database.database import SessionLocal, engine
import models.model
from fastapi.middleware.cors import CORSMiddleware

origins = [
    'http://localhost:3000'    
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

#declare model pydantic
class TransactionBase(BaseModel):
    amount:float
    category:str
    description:str
    is_income:bool
    date:str


class TransactionModel(TransactionBase):
    id:int
    
    class Config:
        orm_mode = True
        
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependecy = Annotated[Session,Depends(get_db)]

models.model.Base.metadata.create_all(bind = engine)

url = "./data/search_data_raw.csv"

@app.get("/")
def welcome_page():
    return {"saludo":"welcome"}

@app.get("/astro_app")
def astro_app():
    data = read_csv(url)
    return {"data":list(data.Planet_Name)}


@app.post('/transactions/',response_model=TransactionModel)
async def create_transaction(transaction:TransactionBase,db:db_dependecy):
    db_transaction = models.model.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    
    return db_transaction


@app.get('/transactions/',response_model=List[TransactionModel])
async def read_transactions(db:db_dependecy,skip: int=0,limit: int = 100):
    transactions = db.query(models.model.Transaction).offset(skip).limit(limit).all()
    return transactions


if __name__ == "__main__":
    uvicorn.run(app=app,host="localhost",port=8000)