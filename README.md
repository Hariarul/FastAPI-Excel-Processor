## FastAPI Excel Processor

This project is a FastAPI-based web service that processes a specially structured Excel file and provides useful endpoints to interact with the data.

### Project Background

The raw Excel file originally contained many tiny tables scattered across sheets, making it difficult to process using pandas directly. So, as a preprocessing step, the data has been manually cleaned and reorganized into separate sheets — each representing a clean, structured table.

Each sheet is treated as a separate table and is handled independently through API endpoints.

### Features

- Upload an Excel file and store it temporarily in memory
- List all available table (sheet) names
- View all row names from a selected table
- Sum all numeric values horizontally from a selected row in a table
- A Jupyter Notebook (`logic workbook pre workout.ipynb`) is included to show the logic development and how the functionalities were built step by step

## API Endpoints

### 1. `POST /upload_file`

Upload a structured Excel file. Returns a `file_id` which will be used in all further requests.

- **Input**: `.xlsx` file (multi-sheet Excel)
- **Response**: `{ "file_id": "abc123", "tables": ["sheet1", "sheet2", ...] }`

### Example output `file id `

```
 "file_id": "4e146551-9246-4d28-9ec9-5e91d8225fdb"
```

---

### 2. `GET /list_tables?file_id=...`

Returns the list of table names (sheet names) in the uploaded Excel file.

### Example output

```
{
  "tables": [
    "investment measures",
    "growth rates",
    "working capital",
    "discount rate",
    "cashflow details",
    "initial investment",
    "book value & depreciation",
    "operating cashflows"
  ]
}
```
---
### 3. `GET /get_rows?file_id=...&table_name=...`

Returns all row names from the first column of the selected sheet.

### Example output

```
{
  "table_name": "operating cashflows",
  "row_names": [
    "Lifetime Index",
    "Revenues",
    " -Var. Expenses",
    " - Fixed Expenses",
    "EBITDA",
    " - Depreciation",
    "EBIT",
    " -Tax",
    "EBIT(1-t)",
    " + Depreciation",
    " - ∂ Work. Cap",
    "NATCF",
    "Discount Factor",
    "Discounted CF"
  ]
}
```
---

### 4. `GET /row_sum?file_id=...&table_name=...&row_name=...`

Returns the **horizontal sum of numeric values** from a specific row across all columns (excluding the row name column). Non-numeric or string values are ignored during summing.

### Example output

```
{
  "table": "operating cashflows",
  "row": "Revenues",
  "sum": 537024.0000000001
}

```

---

## Project Structure

your-project/

├── main.py # FastAPI application code

├── requirements.txt # Required Python packages

├── README.md # You're reading it now

└── Workbook.ipynb # Jupyter notebook showing logic development


---

## Setup Instructions

Follow the steps below to run the project on your system:

### 1. Clone the repository

git clone https://github.com/Hariarul/FastAPI-Excel-Processor.git
cd your-repo-name

### 2.Install required packages

pip install -r requirements.txt

### 3.Run the application

uvicorn myfile:app --reload --port 9090 or python myfile.py

### 4.localhost swagger UI

http://localhost:9090/docs

### Logic Workbook

The file Workbook.ipynb contains the Jupyter notebook where all the logic (Excel parsing, table detection, row sum handling, etc.) has been worked out before converting it into API code.




