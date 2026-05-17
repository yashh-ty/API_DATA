from fastapi import FastAPI, HTTPException,Body
from fastapi.middleware.cors import CORSMiddleware
from db import connection_sql1
import bcrypt
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
    connection = connection_sql1()

    cursor = connection.cursor()
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

    connection = connection_sql1()

    cursor = connection.cursor()

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

        connection = connection_sql1()

        cursor = connection.cursor()

        cursor.execute(sql, (f"{q.upper()}%",))

        results = cursor.fetchall()
        stocks = []
        for row in results:
            stocks.append(row["SYMBOL"])
        return stocks

    except Exception as e:
        return {"error": str(e)}



#It is used to submit the response of the data of the calls

@app.post("/submit_call")
def submit_call(data: dict):

    try:

        # -----------------------------
        # FETCH DATA
        # -----------------------------

        doa = data.get("call_date")

        student_name = data.get("student_name")

        symbol = data.get("symbol")

        call_type = data.get("call_type")

        entry_price = float(data.get("entry_price"))

        target1 = float(data.get("target1"))

        target2 = float(data.get("target2"))

        stoploss = float(data.get("stoploss"))

        # -----------------------------
        # RISK REWARD CALCULATION
        # -----------------------------

        risk = abs(entry_price - stoploss)

        reward = abs(target2 - entry_price)

        # -----------------------------
        # INSERT QUERY
        # -----------------------------

        insert_query = """

            INSERT INTO trade_calls (

                doa,
                student_name,
                symbol,
                call_type,
                entry_price,
                target1,
                target2,
                stoploss,
                risk,
                reward

            )

            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

        """

        values = (

            doa,
            student_name,
            symbol,
            call_type,
            entry_price,
            target1,
            target2,
            stoploss,
            risk,
            reward

        )
        connection = connection_sql1()

        cursor = connection.cursor()

        cursor.execute(insert_query, values)


        return {

            "message": "Trade Call Added Successfully"

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.post("/login")
def login(data: dict = Body(...)):

    try:

        mobilenumber = data.get("mobileNumber")

        pin = data.get("pin")

        # -----------------------------
        # CHECK USER IN DATABASE
        # -----------------------------

        query = """

            SELECT id, full_name, pin_hash
            FROM users_call
            WHERE mobile_number=%s

        """
        connection = connection_sql1()


        cursor = connection.cursor()
        cursor.execute(query)

        user = cursor.fetchone()

        # -----------------------------
        # INVALID LOGIN
        # -----------------------------

        if not user:

            raise HTTPException(
                status_code=401,
                detail="Invalid Mobilenumber or Pin"
            )

        stored_hash = user[2]

        # -----------------------------
        # VERIFY PIN
        # -----------------------------

        if not bcrypt.checkpw(

            pin.encode("utf-8"),
            stored_hash.encode("utf-8")

        ):

            raise HTTPException(
                status_code=401,
                detail="Invalid Mobilenumber or Pin"
            )

        # -----------------------------
        # SUCCESS LOGIN
        # -----------------------------

        return {

            "success": True,

            "message": "Login Successful",

            "user": {

                "id": user[0],

                "full_name": user[1]

            }

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/signup")
def signup(data: dict = Body(...)):

    try:

        # -----------------------------------
        # FETCH DATA
        # -----------------------------------

        full_name = data.get("fullName")

        mobile_number = data.get("mobileNumber")

        dob = data.get("DOB")

        pin_code = data.get("pinCode")

        city = data.get("city")

        email = data.get("email")

        pin = data.get("pin")

        # -----------------------------------

        # -----------------------------------

        check_query = """

            SELECT id
            FROM users_call
            WHERE email=%s
            OR mobile_number=%s

        """
        connection = connection_sql1()

        cursor = connection.cursor()
        cursor.execute(
            check_query,
            (email, mobile_number)
        )

        existing_user = cursor.fetchone()

        if existing_user:

            raise HTTPException(
                status_code=400,
                detail="User already exists"
            )

        # -----------------------------------
        # HASH PIN
        # -----------------------------------

        hashed_pin = bcrypt.hashpw(
            pin.encode("utf-8"),
            bcrypt.gensalt()
        )

        # -----------------------------------
        # INSERT QUERY
        # -----------------------------------

        insert_query = """

            INSERT INTO users_call (

                full_name,
                mobile_number,
                dob,
                pin_code,
                city,
                email,
                pin_hash

            )

            VALUES (%s,%s,%s,%s,%s,%s,%s)

        """

        values = (

            full_name,
            mobile_number,
            dob,
            pin_code,
            city,
            email,
            hashed_pin.decode("utf-8")

        )

        cursor.execute(insert_query, values)


        return {

            "success": True,
            "message": "Signup Successful"

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
@app.get("/new")
def home():
    return {"message": "LATEST VERSION WORKING"}