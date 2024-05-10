# tests/test_authentication.py

import pytest
from moschitta_auth.basic_authenticator import BasicAuthenticator

@pytest.fixture
def authenticator():
    return BasicAuthenticator()

def test_authentication_success(authenticator):
    # Register a user with a password
    authenticator.register_user('example_user', 'example_password')

    # Simulate successful authentication
    request = {'username': 'example_user', 'password': 'example_password'}
    user, credentials = authenticator.authenticate(request)
    assert user is not None

def test_authentication_failure(authenticator):
    # Register a user with a password
    authenticator.register_user('example_user', 'example_password')

    # Simulate failed authentication with invalid password
    request = {'username': 'example_user', 'password': 'invalid_password'}
    user, credentials = authenticator.authenticate(request)
    assert user is None

def test_authentication_failure_no_user(authenticator):
    # Simulate failed authentication with non-existing user
    request = {'username': 'non_existing_user', 'password': 'invalid_password'}
    user, credentials = authenticator.authenticate(request)
    assert user is None
