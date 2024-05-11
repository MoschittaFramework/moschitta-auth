# delete_database.py

import os
import sys

def delete_database(database_file):
    try:
        if os.path.exists(database_file):
            os.remove(database_file)
            print(f"Database file '{database_file}' deleted successfully.")
        else:
            print(f"Database file '{database_file}' does not exist.")
    except Exception as e:
        print(f"Error deleting database file '{database_file}': {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python delete_database.py <database_file>")
        sys.exit(1)
    
    database_file = sys.argv[1]
    delete_database(database_file)
