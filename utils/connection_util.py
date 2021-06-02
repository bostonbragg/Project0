from psycopg2 import connect, OperationalError
import os


def create_connection():
    try:
        con = connect(
            host=os.environ.get('HOST'),
            database=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USERNAME'),
            password=os.environ.get('DB_PASSWORD'),
            port=os.environ.get('PORT')
            )
        return con
    except OperationalError as e:
        print(e)


connection = create_connection()
