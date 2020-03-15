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
    print("Database connection closed")

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

    print_color("Running commands...", "WARNING")

    # Run commands one by one
    for command in commands:
        cur.execute(command)

    print_color("Commands ran successfully!", "OKGREEN")

    # Close communication with tht PostgreSQL database server
    cur.close()

    # Commit the changes
    conn.commit()

def parse_commands(conn, pairings):
    """ Parse commands """
    cmd = []
    for pairing in pairings:
        if pairing["type"] == "create_table":
            temp = f"CREATE TABLE {pairing['table_name']}("
            for i, column in enumerate(pairing["columns"]):
                temp += f"{column['name']} {column['type']}"
                for constraint in column["constraints"]:
                    temp += f" {constraint}"
                if i != len(pairing["columns"]) - 1:
                    temp += ","
                else:
                    temp += ")"
            cmd.append(temp)
        elif pairing["type"] == "drop_table":
            temp = f"DROP TABLE"
            if pairing["if_exists"]:
                temp += " IF EXISTS"
            temp += f" {pairing['table_name']}"
            cmd.append(temp)
    return cmd


if __name__ == "__main__":
    try:
        conn = connect()
        
        if conn is None:
            raise Exception("Configuration for the database is invalid.")
        
        print("Database connected opened")
        
        # To print the version of database
        # print_version(conn)
        
        # ------------------- COMMAND USAGE --------------------
        drop_commands = [
                """
                DROP TABLE IF EXISTS cars
                """
                ]

        create_commands = [
                """
                CREATE TABLE cars(
                    id BIGSERIAL PRIMARY KEY,
                    make VARCHAR(50) NOT NULL,
                    model VARCHAR(50) NOT NULL,
                    year INTERVAL YEAR NOT NULL
                )
                """
                ]

        run_commands(conn, drop_commands)
        run_commands(conn, create_commands)
        # ------------------------------------------------------

        print("Running dict commands...")

        # -------------------- DICT USAGE ----------------------
        drop_pairings = [{'type': 'drop_table', 'table_name': 'cars', 'if_exists': True},
                {'type': 'drop_table', 'table_name': 'bikes', 'if_exists': True}
                ]
        
        create_pairings = [
                            {
                                'type': 'create_table',
                                'table_name': 'cars', 
                                'columns': [
                                    {
                                        'name': 'id', 
                                        'type': 'BIGSERIAL',
                                        'constraints': [
                                                'PRIMARY KEY'
                                            ]
                                        },
                                    {
                                        'name': 'make',
                                        'type': 'VARCHAR(50)',
                                        'constraints': [
                                                'NOT NULL'
                                            ]
                                        },
                                    {
                                        'name': 'model',
                                        'type': 'VARCHAR(50)',
                                        'constraints': [
                                                'NOT NULL'
                                            ]
                                        },
                                    {
                                        'name': 'year',
                                        'type': 'INTERVAL YEAR',
                                        'constraints': [
                                                'NOT NULL'
                                            ]
                                        }
                                ]
                            }
                        ]

        drop_cmds = parse_commands(conn, drop_pairings)
        create_cmds = parse_commands(conn, create_pairings)
        
        run_commands(conn, drop_cmds)
        run_commands(conn, create_cmds)
        # ------------------------------------------------------

        disconnect(conn)
    except (Exception, psycopg2.DatabaseError) as error:
        print_color(error, "FAIL")

