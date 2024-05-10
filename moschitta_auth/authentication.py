# authentication.py

import pytest

from moschitta_auth.basic_authenticator import BasicAuthenticator


@pytest.fixture
def authenticator():
    return BasicAuthenticator()


def test_authentication_success(authenticator):
    # Simulate successful authentication
    request = {}  # Mock request object
    user, credentials = authenticator.authenticate(request)
    assert user is not None


def test_authentication_failure(authenticator):
    # Simulate failed authentication
    request = {}  # Mock request object
    user, credentials = authenticator.authenticate(request)
    assert user is None
