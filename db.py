import pymysql

mydb = pymysql.connect(host='147.93.97.191',
                       user='client',
                       password='StockStreets@2026',
                       database='stock_streets',
                       port=3306)
cursor = mydb.cursor(pymysql.cursors.DictCursor)

