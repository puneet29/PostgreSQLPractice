import psycopg2
from config import config

def connect():
    """ Connect to the PostgreSQL database server"""
    conn = None
    try:
        # Read connection parameters
        params = config()

        # Connect to the PostgreSQL server
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**params)

        # Create a cursor
        cur = conn.cursor()

        # Execute a statement
        print("PostgreSQL database version:")
        cur.execute("Select version()")

        # Display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # Close the communication with the PostgreSQL
        cur.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")


if __name__ == "__main__":
    connect()

