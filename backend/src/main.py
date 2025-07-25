from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .config import ORIGINS
from .services import parse_uploaded_file
from .models import Expense, CategorySummary, ExpenseDB
from .database import SessionLocal, engine, Base
import shutil
import pandas as pd
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Save file temporarily
    temp_path = f"./temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Parse and insert into DB
    df = parse_uploaded_file(temp_path)
    for _, row in df.iterrows():
        expense = ExpenseDB(
            fecha=row.get("Fecha"),
            descripcion=row.get("Descripción"),
            monto=row.get("Monto"),
            categoria=row.get("Categoria"),
        )
        db.add(expense)
    db.commit()
    # Remove temp file
    import os
    os.remove(temp_path)
    return {
        "filename": file.filename,
        "rows_inserted": len(df),
    }

@app.get("/expenses/", response_model=List[Expense])
def get_expenses(db: Session = Depends(get_db)):
    expenses = db.query(ExpenseDB).all()
    return expenses

@app.get("/expenses/categories-summary", response_model=List[CategorySummary])
def get_expenses_categories_summary(db: Session = Depends(get_db)):
    expenses = db.query(ExpenseDB).all()
    if not expenses:
        return []
    df = pd.DataFrame([{
        "Categoria": e.categoria,
        "Monto": e.monto
    } for e in expenses])
    grouped = df.groupby("Categoria", dropna=False)["Monto"].sum().reset_index()
    total = grouped["Monto"].sum()
    grouped["percentage"] = grouped["Monto"] / total * 100 if total else 0
    result = [
        {
            "category": row["Categoria"] if pd.notnull(row["Categoria"]) else "Sin categoría",
            "amount": row["Monto"],
            "percentage": round(row["percentage"], 2)
        }
        for _, row in grouped.iterrows()
    ]
    return result

@app.get("/")
def read_root():
    return {"Hello": "World"}