from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base
from pydantic import BaseModel
from typing import Optional

class ExpenseDB(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(String, nullable=True)
    descripcion = Column(String, nullable=True)
    monto = Column(Float, nullable=True)
    categoria = Column(String, nullable=True)

class Expense(BaseModel):
    fecha: Optional[str]
    descripcion: Optional[str]
    monto: Optional[float]
    categoria: Optional[str]

    class Config:
        orm_mode = True

class CategorySummary(BaseModel):
    category: str
    amount: float
    percentage: float