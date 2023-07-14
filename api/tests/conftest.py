import pytest
from rest_framework.test import APIClient
from user import services as user_services


@pytest.fixture
def user():
    """
    Fixture that creates a user for testing purposes.

    Returns:
        User: The created user object.
    """
    user_dc = user_services.UserDataClass(
        first_name="Jesse",
        last_name="Pinkman",
        email="jessepinkman@gmail.com",
        password="superstrongpassword",
    )

    user = user_services.create_user(user_dc=user_dc)

    return user


@pytest.fixture
def client():
    """
    Fixture that provides an instance of the APIClient for testing.

    Returns:
        APIClient: An instance of the APIClient.
    """
    return APIClient()


@pytest.fixture
def auth_client(user, client):
    """
    Fixture that provides an authenticated APIClient for testing.

    Args:
        user (User): The user object created by the 'user' fixture.
        client (APIClient): The APIClient instance created by the 'client' fixture.

    Returns:
        APIClient: An authenticated instance of the APIClient.
    """
    client.post(
        "/api/users/login/",
        dict(email=user.email, password="superstrongpassword"),
    )

    return client
