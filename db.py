import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def connection_sql1():
    mydb=pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT")),
        cursorclass=pymysql.cursors.DictCursor,

        autocommit=True
    )
    return mydb


def connection_sql2():
    mydb=pymysql.connect(
        host=os.getenv("DB_HOST1"),
        user=os.getenv("DB_USER1"),
        password=os.getenv("DB_PASSWORD1"),
        database=os.getenv("DB_NAME1"),
        port=int(os.getenv("DB_PORT1")),
        cursorclass=pymysql.cursors.DictCursor,

        autocommit=True
    )
    return mydb

