# tests/test_authentication.py

import os
import subprocess

import pytest

# Import the create_database and delete_database functions from the scripts
from create_database import create_database
from delete_database import delete_database

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


from moschitta_auth.basic_authenticator import BasicAuthenticator


@pytest.fixture
def authenticator():
    """Fixture to create a BasicAuthenticator instance for testing."""
    db_path = "test_auth.db"  # Use a temporary test database for testing
    return BasicAuthenticator(db_path=db_path)

def test_authentication_success(authenticator):
    """Test successful authentication."""
    authenticator.register_user("example_user", "example_password")
    assert authenticator.authenticate("example_user", "example_password") is not None

def test_authentication_failure(authenticator):
    """Test authentication failure with wrong password."""
    assert authenticator.authenticate("example_user", "wrong_password") is None

def test_authentication_failure_no_user(authenticator):
    """Test authentication failure with non-existent user."""
    assert authenticator.authenticate("nonexistent_user", "example_password") is None
