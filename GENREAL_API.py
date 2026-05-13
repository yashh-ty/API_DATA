from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import cursor

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



@app.get("/")
def home():
    return {"message": "API is running"}

# ---------------- USED TO GET THE DATA OFF STOCKS OF BASED ON INDEXES---------------- #
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

#-------It is used to get the OHLC of any of the stock--------------#

@app.get("/stock/{symbol}")
def get_stock_ohlc(symbol: str):

    query = """
        SELECT 
            T_DATE,
            SYMBOL,
            OPEN_PRICE,
            HIGH_PRICE,
            LOW_PRICE,
            CLOSE_PRICE,
            TTL_TRD_QNTY,
            PCT_CHNG,
            DELIV_PER
        FROM bhavcopy
        WHERE symbol = %s
        ORDER BY T_DATE DESC
        LIMIT 1
    """

    cursor.execute(query, (symbol.upper(),))

    row = cursor.fetchone()

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Stock not found"
        )

    return {
        "DATE":row['T_DATE'],
        "SYMBOL": row['SYMBOL'],
        "OPEN": row['OPEN_PRICE'],
        "HIGH": row['HIGH_PRICE'],
        "LOW": row['LOW_PRICE'],
        "CLOSE": row['CLOSE_PRICE'],
        "VOLUME":row['TTL_TRD_QNTY'],
        "DELIV_PCT":row['PCT_CHNG']

    }

#-------------------USED TO SUGGEST THE STOCKS BASED ON THE INPUT---------#
@app.get("/search-stock")
def search_stock(q: str):
    try:

        sql = '''SELECT DISTINCT SYMBOL
        FROM stock_streets.bhavcopy
        WHERE SYMBOL LIKE %s
        AND T_DATE = (
        SELECT MAX(T_DATE)
        FROM stock_streets.bhavcopy
        )
        LIMIT 10;'''

        cursor.execute(sql, (f"{q.upper()}%",))

        results = cursor.fetchall()
        stocks = []
        for row in results:
            stocks.append(row["SYMBOL"])
        return stocks

    except Exception as e:
        return {"error": str(e)}