import os
import mysql.connector
from dotenv import load_dotenv
load_dotenv()


def establish_connection():
    USER = os.getenv("db_user")
    PASSWORD = os.getenv("PASSWORD")

    cnx = mysql.connector.connect(
        user=USER,
        password=PASSWORD,
        host='127.0.0.1',
        port=3306,
        database='brain'
    )
    return [cnx, cnx.cursor()]
