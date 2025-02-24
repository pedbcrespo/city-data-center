import psycopg2
from config import dev_configuration as db

DB_CONFIG = {
    "dbname": db.database,
    "user": db.user,
    "password": db.password,
    "host": db.host,
    "port": 5432
}

conn = psycopg2.connect(**DB_CONFIG)



    