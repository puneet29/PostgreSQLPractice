from config import config
from utils import print_color

import psycopg2

def connect():
    """ Connect to the PostgreSQL database server"""
    conn = None

    # Read connection parameters
    params = config()

    # Connect to the PostgreSQL server
    print_color("Connecting to the PostgreSQL database...", "HEADER")
    try:
        conn = psycopg2.connect(**params)
    finally:
        return conn

def disconnect(conn):
    """ Disconnect PostgreSQL database server """
    if conn is None:
        return

    conn.close()
    print_color("Database connection closed", "OKGREEN")

def print_version(conn):
    """ Print the version of PostgreSQL running """
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

def run_commands(conn, commands):
    """ Running SQL commands in PostgreSQL database """
    # Create a cursor
    cur = conn.cursor()

    print("Running commands...")

    # Run commands one by one
    for command in commands:
        cur.execute(command)

    print("Commands ran successfully!")

    # Close communication with tht PostgreSQL database server
    cur.close()

    # Commit the changes
    conn.commit()

    
if __name__ == "__main__":
    try:
        conn = connect()
        
        if conn is None:
            raise Exception("Configuration for the database is invalid.")
        
        print_color("Database connected opened", "OKGREEN")
        
        # To print the version of database
        # print_version(conn)
        
        # To drop tables
        drop_commands = [
                """
                DROP TABLE cars
                """
                ]

        # To create tables
        create_commands = [
                """
                CREATE TABLE cars(
                    id BIGSERIAL PRIMARY KEY,
                    make VARCHAR(50) NOT NULL,
                    model VARCHAR(50) NOT NULL,
                    year DATE NOT NULL
                )
                """
                ]

        run_commands(conn, drop_commands)
        run_commands(conn, create_commands)

        disconnect(conn)
    except (Exception, psycopg2.DatabaseError) as error:
        print_color(error, "FAIL")

