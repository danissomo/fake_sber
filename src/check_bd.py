from mysql.connector import connect, Error
try:
    db_sql =  connect(
        host="127.0.0.1",
        user="root",
        password="sql_password",
        port = 3306,
        database = "mysql",
        connection_timeout  = 10
    )
except Exception as e:
    print(e)

cursor = db_sql.cursor()
cursor.execute("SELECT * FROM customers")
result = cursor.fetchall()
print(result)