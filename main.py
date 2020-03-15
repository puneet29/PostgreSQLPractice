import psycopg2
from settings import Config

config = Config()

conn = psycopg2.connect(database="test", user=config.user, password=config.password, host='127.0.0.1', port=5432)

print(conn)
