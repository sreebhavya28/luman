def get_connection():
    import mysql.connector as sql
    connect=sql.connect(host="localhost",
                user="public",
                passwd="Password#123",
                database="lumen")
    return connect
my_connection = get_connection()
my_cursor = my_connection.cursor()