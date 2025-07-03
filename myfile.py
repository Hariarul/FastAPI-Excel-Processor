from fastapi import FastAPI, UploadFile, File, Query, HTTPException
import pandas as pd
from typing import Dict
import uvicorn
from uuid import uuid4

app = FastAPI()


# Define target sheets
sheets = [
    'investment measures',
    'growth rates',
    'working capital',
    'discount rate',
    'cashflow details',
    'initial investment',
    'book value & depreciation',
    'operating cashflows'
]

# In-memory data store: file_id → data
data_store: Dict[str, Dict[str, pd.DataFrame]] = {}

def load_file(file_obj) -> Dict[str, pd.DataFrame]:
    df_dict = pd.read_excel(file_obj, sheet_name=sheets)
    for sheet_name, df in df_dict.items():
        if 'Column1' in df.columns:
            df.drop('Column1', axis=1, inplace=True)
    return df_dict

def normalize_table_name(table_name: str, data: Dict[str, pd.DataFrame]) -> str:
    lower_map = {name.lower(): name for name in data.keys()}
    key = table_name.strip().lower()
    if key not in lower_map:
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found.")
    return lower_map[key]

#Upload once and store in memory
@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    data = load_file(file.file)
    file_id = str(uuid4())
    data_store[file_id] = data
    return {
        "file_id": file_id,
        "tables": list(data.keys())
    }

@app.get("/list_tables")
async def list_tables(file_id: str = Query(...)):
    if file_id not in data_store:
        raise HTTPException(status_code=404, detail="Invalid file_id.")
    return {"tables": list(data_store[file_id].keys())}

@app.get("/get_rows")
async def get_rows(
    file_id: str = Query(...),
    table_name: str = Query(...)
):
    if file_id not in data_store:
        raise HTTPException(status_code=404, detail="Invalid file_id.")

    data = data_store[file_id]
    table = normalize_table_name(table_name, data)
    df = data[table]

    column_name = table_name.upper()
    if column_name not in df.columns:
        raise HTTPException(status_code=400, detail=f"Column '{column_name}' not found in table '{table}'.")

    row_names = df[column_name].dropna().astype(str).tolist()
    return {
        "table_name": table,
        "row_names": row_names
    }

@app.get("/row_sum")
async def row_sum(
    file_id: str = Query(...),
    table_name: str = Query(...),
    row_name: str = Query(...)
):
    if file_id not in data_store:
        raise HTTPException(status_code=404, detail="Invalid file_id.")

    data = data_store[file_id]
    table = normalize_table_name(table_name, data)
    sheet = data[table]

    for _, row in sheet.iterrows():
        key = str(row.iloc[0]).strip()
        if key == row_name.strip():
            # Select only numeric values across the row (excluding first column)
            numeric_values = pd.to_numeric(row.iloc[1:], errors='coerce')
            numeric_sum = numeric_values[numeric_values.notna()].sum()

            return {
                "table": table,
                "row": key,
                "sum": numeric_sum
            }

    raise HTTPException(status_code=404, detail=f"Row '{row_name}' not found in table '{table}'.")


# Run with: uvicorn myfile:app --reload
if __name__ == "__main__":
    uvicorn.run("myfile:app", host="localhost", port=9090, reload=True)
