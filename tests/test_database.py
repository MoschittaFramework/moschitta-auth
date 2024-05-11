# tests/test_database.py
"""
Module: test_database.py

This module contains unit tests for the database-related functionality of the Moschitta Framework.

The tests cover the creation of database tables, database connections, table existence, table structure,
data integrity, and database operations.

These tests ensure that the database functionality works as expected and maintains the integrity of the data.

Author: Skyler

Date: May 11, 2024

"""

import os
import sqlite3
import subprocess

import pytest

# Import the create_database and delete_database functions from the scripts
from create_database import create_database
from delete_database import delete_database
from moschitta_auth.basic_authenticator import BasicAuthenticator

# Default test database path
DEFAULT_TEST_DB_PATH = "test_auth.db"


@pytest.fixture(scope="session", autouse=True)
def setup_teardown():
    # Determine the command based on whether the '--test' flag should be used
    command = ["python", "create_database.py", "--test"]
    # Execute the command to create the database
    subprocess.run(command, check=True)

    # Yield to run the tests
    yield

    # Delete the test database after all tests have been executed
    # TODO Refactor the delete_database script to handle the other database types also.
    delete_database(DEFAULT_TEST_DB_PATH)


@pytest.fixture
def test_db_path_fixture():
    """Fixture to provide the path to the temporary test database for testing."""
    yield DEFAULT_TEST_DB_PATH


def test_create_user_table(test_db_path_fixture):
    """
    Test the creation of the user table in the database.

    Args:
        test_db_path (str): The path to the temporary test database.

    Returns:
        None
    """
    authenticator = BasicAuthenticator(db_path=test_db_path_fixture)
    authenticator._create_user_table()
    # Add assertions to verify that the table is created correctly


def test_database_connection(test_db_path_fixture):
    """
    Test the database connection.

    Args:
        test_db_path (str): The path to the temporary test database.

    Returns:
        None
    """
    try:
        conn = sqlite3.connect(test_db_path_fixture)
        conn.close()
        assert True
    except Exception as e:
        assert False, f"Database connection test failed: {e}"


def test_table_existence(test_db_path_fixture):
    """
    Test the existence of tables in the database.

    This test checks whether tables exist in the database by querying the database schema.
    It verifies that at least one table is present in the database.

    Args:
        test_db_path (str): The path to the temporary test database.

    Returns:
        None
    """
    try:
        conn = sqlite3.connect(test_db_path_fixture)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        assert len(tables) > 0, "No tables found in the database"
    except Exception as e:
        assert False, f"Table existence test failed: {e}"
    finally:
        conn.close()


def test_table_structure(test_db_path_fixture):
    """
    Test the structure of tables in the database.

    This test verifies the structure of the 'users' table in the database.
    It checks if the table contains the expected columns.

    Args:
        test_db_path (str): The path to the temporary test database.

    Returns:
        None
    """
    expected_columns = ["username", "hashed_password"]  # Define expected columns
    try:
        conn = sqlite3.connect(test_db_path_fixture)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(users);")
        columns = cursor.fetchall()
        actual_columns = [column[1] for column in columns]
        assert (
            actual_columns == expected_columns
        ), f"Unexpected table structure: {actual_columns}"
    except Exception as e:
        assert False, f"Table structure test failed: {e}"
    finally:
        conn.close()


# Additional test functions can be added for other database tests
def test_data_integrity(test_db_path_fixture):
    """
    Test the integrity of data in the database.

    This test inserts data into the 'users' table, retrieves it, and verifies its integrity.
    It checks if the inserted data matches the expected values.

    Args:
        test_db_path (str): The path to the temporary test database.

    Returns:
        None
    """
    try:
        conn = sqlite3.connect(test_db_path_fixture)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, hashed_password) VALUES (?, ?)",
            ("test_user", "hashed_password"),
        )
        conn.commit()
        cursor.execute("SELECT * FROM users WHERE username=?", ("test_user",))
        user = cursor.fetchone()
        assert user is not None, "Failed to retrieve inserted data"
        assert user[0] == "test_user", "Incorrect username retrieved"
        assert user[1] == "hashed_password", "Incorrect password retrieved"
    except Exception as e:
        assert False, f"Data integrity test failed: {e}"
    finally:
        conn.close()


def test_database_operations(test_db_path_fixture):
    """
    Test various database operations.

    This test performs various database operations such as insertion, updating, and deletion of records.
    It verifies the correctness of these operations and ensures data consistency in the database.

    Args:
        test_db_path (str): The path to the temporary test database.

    Returns:
        None
    """
    try:
        # Connect to the test database
        conn = sqlite3.connect(test_db_path_fixture)
        cursor = conn.cursor()

        # Check if the test user already exists in the database
        cursor.execute("SELECT * FROM users WHERE username=?", ("test_user",))
        existing_user = cursor.fetchone()
        if existing_user:
            # If the test user exists, delete it to ensure a clean test environment
            cursor.execute("DELETE FROM users WHERE username=?", ("test_user",))
            conn.commit()

        # Insert a test user into the 'users' table
        cursor.execute(
            "INSERT INTO users (username, hashed_password) VALUES (?, ?)",
            ("test_user", "hashed_password"),
        )
        conn.commit()

        # Update the password for the test user
        cursor.execute(
            "UPDATE users SET hashed_password=? WHERE username=?",
            ("new_hashed_password", "test_user"),
        )
        conn.commit()

        # Retrieve the updated password for verification
        cursor.execute(
            "SELECT hashed_password FROM users WHERE username=?", ("test_user",)
        )
        updated_password = cursor.fetchone()[0]
        assert updated_password == "new_hashed_password", "Record update failed"

        # Delete the test user from the 'users' table
        cursor.execute("DELETE FROM users WHERE username=?", ("test_user",))
        conn.commit()

        # Verify that the test user has been deleted
        cursor.execute("SELECT * FROM users WHERE username=?", ("test_user",))
        deleted_record = cursor.fetchone()
        assert deleted_record is None, "Record deletion failed"
    except Exception as e:
        assert False, f"Database operations test failed: {e}"
    finally:
        # Close the database connection
        conn.close()
