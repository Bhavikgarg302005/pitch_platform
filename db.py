import pymysql

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Bhavikgarg@30',
        database='SharkTank6',
        cursorclass=pymysql.cursors.Cursor  # This will return results as a list of lists
    )