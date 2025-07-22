import pandas as pd
from .categories import diccionario_categorias_tc, diccionario_categorias_cc, asignar_categoria

def parse_uploaded_file(file_path: str) -> pd.DataFrame:
    # Try both TC and CC parsing, return whichever is not empty
    from os.path import basename
    if "Tarjeta de Crédito" in basename(file_path):
        df = process_tc_file(file_path)
        df = df.rename(columns={"Detalle": "Descripción", "Monto $": "Monto"})
    elif "Cartola" in basename(file_path):
        df = process_cc_file(file_path)
    else:
        df = pd.DataFrame()
    if not df.empty:
        unified_columns = ["Fecha", "Descripción", "Monto", "Categoria"]
        for col in unified_columns:
            if col not in df.columns:
                df[col] = None
        df = df[unified_columns]
        # Filter out rows where Descripción is 'MONTO CANCELADO' or 'MONTO CANCELADO PAGO NORMAL' (case-insensitive)
        df = df[~df["Descripción"].astype(str).str.strip().str.upper().isin(["MONTO CANCELADO", "MONTO CANCELADO PAGO NORMAL"])]
    return df

def process_tc_file(file_path: str) -> pd.DataFrame:
    df_raw = pd.read_excel(file_path)
    header_row_idx = df_raw[df_raw.apply(lambda row: row.astype(str).str.contains("Detalle", case=False).any(), axis=1)].index[0]
    df = pd.read_excel(file_path, skiprows=header_row_idx + 1)
    df.columns = df_raw.iloc[header_row_idx]
    if "Detalle" not in df.columns or "Monto $" not in df.columns:
        return pd.DataFrame()
    df = df.dropna(subset=["Detalle", "Monto $"])
    df["Monto $"] = df["Monto $"].astype(str).str.replace(",", "", regex=False)
    df["Monto $"] = pd.to_numeric(df["Monto $"], errors="coerce")
    df['Categoria'] = df['Detalle'].apply(lambda x: asignar_categoria(x, diccionario_categorias_tc))
    return df

def process_cc_file(file_path: str) -> pd.DataFrame:
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
    df_filtrado = df[df["Categoría"].isin(["Abonos", "Cargos"])].copy()
    df_filtrado['Categoria'] = df_filtrado['Descripción'].apply(lambda x: asignar_categoria(x, diccionario_categorias_cc))
    return df_filtrado

def consolidate_expenses(data_dir: str) -> pd.DataFrame:
    import os
    all_expenses = []
    if not os.path.exists(data_dir):
        return pd.DataFrame()
    for filename in os.listdir(data_dir):
        file_path = os.path.join(data_dir, filename)
        if filename.startswith("Movimientos Nacionales de Tarjeta de Crédito"):
            df = process_tc_file(file_path)
            df = df.rename(columns={"Detalle": "Descripción", "Monto $": "Monto"})
        elif filename.startswith("Cartola"):
            df = process_cc_file(file_path)
        else:
            continue
        if not df.empty:
            all_expenses.append(df)
    if not all_expenses:
        return pd.DataFrame()
    unified_columns = ["Fecha", "Descripción", "Monto", "Categoria"]
    aligned_expenses = []
    for df in all_expenses:
        df = df.loc[:, ~df.columns.duplicated()]
        for col in unified_columns:
            if col not in df.columns:
                df[col] = None
        df = df[unified_columns]
        aligned_expenses.append(df)
    consolidated_df = pd.concat(aligned_expenses, ignore_index=True)
    return consolidated_df