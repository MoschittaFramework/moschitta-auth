import argparse
import os
import sqlite3

def create_database(database_type: str = 'sqlite', database_path: str = 'auth.db'):
    """
    Create a database based on the specified type.

    Args:
        database_type (str, optional): Type of the database. Defaults to 'sqlite'.
        database_path (str, optional): Path to the database. Defaults to 'auth.db'.

    Raises:
        ValueError: If an unsupported database type is provided.
    """
    # Initialize conn variable
    conn = None

    try:
        if database_type == 'sqlite':
            # Code to create SQLite database
            project_root = os.path.dirname(os.path.abspath(__file__))
            db_file_path = os.path.join(project_root, database_path)
            conn = sqlite3.connect(db_file_path)
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS users
                        (username text PRIMARY KEY, hashed_password text)''')
            c.execute('''CREATE TABLE IF NOT EXISTS sessions
                        (session_id text PRIMARY KEY)''')
            conn.commit()
            conn.close()
            print(f"SQLite database created at {db_file_path}")

        elif database_type == 'postgres':
            raise NotImplementedError("PostgreSQL database creation is not yet implemented.")

        elif database_type == 'mysql':
            raise NotImplementedError("MySQL database creation is not yet implemented.")

        else:
            raise ValueError(f"Unsupported database type: {database_type}")

    except Exception as e:
        print(f"Error creating database: {e}")

    finally:
        if conn is not None:
            conn.close()

def main():
    """
    Parse command-line arguments and create the database accordingly.
    """
    parser = argparse.ArgumentParser(description="Create a database.")
    parser.add_argument("--database-type", default='sqlite', choices=['sqlite', 'postgres', 'mysql'], help="Type of the database (default: sqlite)")
    parser.add_argument("--database-path", default='auth.db', help="Path to the database (default: auth.db)")
    parser.add_argument("--test", action="store_true", help="Create a test database")
    args = parser.parse_args()

    if args.test and args.database_type == 'sqlite':
        database_path = 'test_auth.db'
        database_type = 'sqlite'
        create_database(database_type, database_path)
        print(f"Test SQLite database created at {database_path}")

    elif args.test:
        raise ValueError("The --test flag is only supported for SQLite databases.")

    else:
        database_path = args.database_path
        create_database(args.database_type, database_path)

if __name__ == "__main__":
    main()
