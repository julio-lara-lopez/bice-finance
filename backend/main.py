from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import shutil
import os
from typing import List

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Diccionario de categorías
diccionario_categorias_tc = {
    "SUPERMERCADO": ["unimarc", "lider", "jumbo", "tottus"],
    "INTERES": ["impuesto", "intereses", "comision" ],
    "INTERNACIONAL": ["traspaso"],
    "INTERNET": ["movistar"],
    "PASAJES": ["latam", "despegar", "jetsmart", "sky"],
    "SALIDAS": ["uber eats", "floreria", "low free"],
    "CONSUMISMO": ["merpago venta", "zara", "paris"],
    "GYM": ["biogym", "sportlife", "budas"],
    "TRANSPORTE": ["uber trip", "cabify", "bip", "copec"],  
    "SALUD": ["matfemaco", "salcrobrand", "cryz verde"],
    "SUSCRIPCION": ["prime video", "unicef", "disney", "hbo max"],
    "OTROS": []  # Puedes dejar esta como categoría por defecto
}

diccionario_categorias_cc = {
    "SUPERMERCADO": ["unimarc", "lider", "jumbo", "tottus"],
    "INTERES": ["impuesto", "intereses", "comision" ],
    "INTERNACIONAL": ["traspaso"],
    "INTERNET": ["movistar"],
    "PASAJES": ["latam", "despegar", "jetsmart", "sky"],
    "SALIDAS": ["uber eats", "floreria", "low free"],
    "CONSUMISMO": ["merpago venta", "zara", "paris"],
    "GYM": ["biogym", "sportlife", "budas"],
    "TRANSPORTE": ["uber trip", "cabify", "bip", "copec"],  
    "SALUD": ["matfemaco", "salcrobrand", "cryz verde"],
    "OTROS": []  # Puedes dejar esta como categoría por defecto
}

def asignar_categoria_tc(descripcion):
    descripcion = str(descripcion).lower()
    for categoria, keywords in diccionario_categorias_tc.items():
        for keyword in keywords:
            if keyword in descripcion:
                return categoria
    return "OTROS"

def asignar_categoria_cc(descripcion):
    descripcion = str(descripcion).lower()
    for categoria, keywords in diccionario_categorias_cc.items():
        for keyword in keywords:
            if keyword in descripcion:
                return categoria
    return "OTROS"

def process_tc_file(file_path):
    df_raw = pd.read_excel(file_path)
    header_row_idx = df_raw[df_raw.apply(lambda row: row.astype(str).str.contains("Detalle", case=False).any(), axis=1)].index[0]
    df = pd.read_excel(file_path, skiprows=header_row_idx + 1)
    df.columns = df_raw.iloc[header_row_idx]
    if "Detalle" not in df.columns or "Monto $" not in df.columns:
        return pd.DataFrame()
    df = df.dropna(subset=["Detalle", "Monto $"])
    df["Monto $"] = df["Monto $"].astype(str).str.replace(",", "", regex=False)
    df["Monto $"] = pd.to_numeric(df["Monto $"], errors="coerce")
    df['Categoria'] = df['Detalle'].apply(asignar_categoria_tc)
    return df

def process_cc_file(file_path):
    df = pd.read_excel(file_path, sheet_name="Cartola", skiprows=17)
    columnas_esperadas = ["Fecha", "Categoría", "Nº operación", "Descripción", "Monto"]
    if not all(col in df.columns for col in columnas_esperadas):
        return pd.DataFrame()
    df["Monto"] = (
        df["Monto"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", "", regex=False)
    )
    df["Monto"] = pd.to_numeric(df["Monto"], errors="coerce")
    df_filtrado = df[df["Categoría"].isin(["Abonos", "Cargos"])].copy()  # Use .copy() to avoid SettingWithCopyWarning
    df_filtrado['Categoria'] = df_filtrado['Descripción'].apply(asignar_categoria_cc)
    return df_filtrado

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    os.makedirs(DATA_DIR, exist_ok=True)
    file_path = os.path.join(DATA_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "file_path": file_path}

@app.get("/expenses/")
def get_expenses():
    all_expenses = []
    if not os.path.exists(DATA_DIR):
        return []
    for filename in os.listdir(DATA_DIR):
        file_path = os.path.join(DATA_DIR, filename)
        if filename.startswith("Movimientos Nacionales de Tarjeta de Crédito"):
            df = process_tc_file(file_path)
            df = df.rename(columns={"Detalle": "Descripción", "Monto $": "Monto"})
        elif filename.startswith("Cartola"):
            df = process_cc_file(file_path)
        else:
            continue
        # Only append non-empty DataFrames
        if not df.empty:
            all_expenses.append(df)
    if not all_expenses:
        return []
    # Define the unified set of columns
    unified_columns = ["Fecha", "Descripción", "Monto", "Categoria"]
    # Align all DataFrames to the unified columns
    aligned_expenses = []
    for df in all_expenses:
        # Remove duplicate columns
        df = df.loc[:, ~df.columns.duplicated()]
        # Add missing columns
        for col in unified_columns:
            if col not in df.columns:
                df[col] = None
        # Reorder columns
        df = df[unified_columns]
        aligned_expenses.append(df)
    consolidated_df = pd.concat(aligned_expenses, ignore_index=True)
    return consolidated_df.to_dict(orient="records")

@app.get("/")
def read_root():
    return {"Hello": "World"}
