# tests/test_authentication.py

import pytest
from moschitta_auth.basic_authenticator import BasicAuthenticator

@pytest.fixture
def authenticator():
    return BasicAuthenticator()

def test_authentication_success(authenticator):
    # Simulate successful authentication
    request = {'username': 'example_user', 'password': 'example_password'}  # Valid credentials
    user, credentials = authenticator.authenticate(request)
    assert user is not None

def test_authentication_failure(authenticator):
    # Simulate failed authentication
    request = {'username': 'invalid_user', 'password': 'invalid_password'}  # Invalid credentials
    user, credentials = authenticator.authenticate(request)
    assert user is None
