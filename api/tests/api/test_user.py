import pytest


@pytest.mark.django_db
def test_register_user(client):
    """
    Test the registration of a user.

    Args:
        client (APIClient): The APIClient instance.
    """
    payload = dict(
        first_name="Jesse",
        last_name="Pinkman",
        email="jessepinkman@gmail.com",
        password="superstrongpassword",
    )

    response = client.post("/api/users/register/", payload)

    data = response.data

    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
    assert data["email"] == payload["email"]
    assert "password" not in data


@pytest.mark.django_db
def test_login_user(user, client):
    """
    Test the login of a user.

    Args:
        user (User): The user object created by the 'user' fixture.
        client (APIClient): The APIClient instance.
    """
    response = client.post(
        "/api/users/login/",
        dict(email="jessepinkman@gmail.com", password="superstrongpassword"),
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_login_user_fail(client):
    """
    Test a failed login attempt.

    Args:
        client (APIClient): The APIClient instance.
    """
    response = client.post(
        "/api/users/login/",
        dict(email="jessepinkman@gmail.com", password="superstrongpassword"),
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_get_user(user, auth_client):
    """
    Test retrieving user information.

    Args:
        user (User): The user object created by the 'user' fixture.
        auth_client (APIClient): The authenticated APIClient instance.
    """
    response = auth_client.get("/api/users/me/")

    data = response.data

    assert response.status_code == 200
    assert data["id"] == user.id
    assert data["email"] == user.email
    assert data["first_name"] == user.first_name
    assert data["last_name"] == user.last_name
    assert user.password not in data


@pytest.mark.django_db
def test_logout_user(user, auth_client):
    """
    Test the logout of a user.

    Args:
        user (User): The user object created by the 'user' fixture.
        auth_client (APIClient): The authenticated APIClient instance.
    """
    response = auth_client.post("/api/users/logout/")

    assert response.status_code == 200
    assert response.data["message"] == "Logout complete"
