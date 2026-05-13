from fastapi import FastAPI
from db import cursor
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------- NIFTY 50 API ---------------- #

@app.get("/nifty50")
def get_nifty50_data():

    query = """
    SELECT 
        b.SYMBOL,
        b.OPEN_PRICE,
        b.HIGH_PRICE,
        b.LOW_PRICE,
        b.CLOSE_PRICE,
        b.TTL_TRD_QNTY,
        b.PCT_CHNG
    FROM stock_streets.bhavcopy AS b
    INNER JOIN stock_streets.n50 AS m
    ON b.SYMBOL = m.SYMBOL
    WHERE b.T_DATE = (
        SELECT MAX(T_DATE)
        FROM stock_streets.bhavcopy
    );
    """

    cursor.execute(query)

    records = cursor.fetchall()

    return {
        "status": "success",
        "count": len(records),
        "data": records
    }


