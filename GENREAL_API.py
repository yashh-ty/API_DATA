from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import cursor  # your existing connection

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- SAFE TABLE MAPPING ---------------- #
ALLOWED_TABLES = {
    "nifty50": "n50",
    "niftynext50": "nn50",
    "midcap": "nm50",
    "smallcap": "ns50"
}

# ---------------- MAIN API ---------------- #

@app.get("/")
def home():
    return {"message": "API is running"}

@app.get("/index-data/{index}")
def get_index_data(index: str):
    table = ALLOWED_TABLES.get(index.lower())

    if not table:
        raise HTTPException(status_code=400, detail="Invalid index name")
    query = f"""
        SELECT 
            b.SYMBOL,
            b.OPEN_PRICE,
            b.HIGH_PRICE,
            b.LOW_PRICE,
            b.CLOSE_PRICE,
            b.TTL_TRD_QNTY,
            b.PCT_CHNG
        FROM stock_streets.bhavcopy AS b
        INNER JOIN stock_streets.{table} AS m
        ON b.SYMBOL = m.symbol
        WHERE b.T_DATE = (
            SELECT MAX(T_DATE)
            FROM stock_streets.bhavcopy
        );
        """

    cursor.execute(query)

    records = cursor.fetchall()

    return  records