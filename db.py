import pymysql
import os
from dotenv import load_dotenv

load_dotenv()
mydb = pymysql.connect(host='147.93.97.191',
                       user='client',
                       password='StockStreets@2026',
                       database='stock_streets',
                       port=3306)
mydb=pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=int(os.getenv("DB_PORT"))
)

cursor = mydb.cursor(pymysql.cursors.DictCursor)

