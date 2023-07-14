import pytest

from status import models


@pytest.mark.django_db
def test_create_status(user, auth_client):
    """
    Test the creation of a status.

    Args:
        user (User): The user object created by the 'user' fixture.
        auth_client (APIClient): The authenticated APIClient instance.
    """
    payload = dict(content="Lorem ipsum dolor sit amet")

    response = auth_client.post("/api/status/", payload)

    status_from_db = models.Status.objects.all().first()

    assert response.status_code == 201
    assert response.data["content"] == status_from_db.content
    assert response.data["id"] == status_from_db.id
    assert response.data["user"]["id"] == user.id


@pytest.mark.django_db
def test_get_status(user, auth_client):
    """
    Test retrieving statuses.

    Args:
        user (User): The user object created by the 'user' fixture.
        auth_client (APIClient): The authenticated APIClient instance.
    """
    models.Status.objects.bulk_create(
        [
            models.Status(
                user_id=user.id, content="Lorem ipsum dolor sit amet"
            ),
            models.Status(
                user_id=user.id, content="risus in hendrerit gravida rutrum"
            ),
        ]
    )

    response = auth_client.get("/api/status/")

    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_retrieve_status(user, auth_client):
    """
    Test retrieving a specific status.

    Args:
        user (User): The user object created by the 'user' fixture.
        auth_client (APIClient): The authenticated APIClient instance.
    """
    models.Status.objects.create(
        user_id=user.id, content="Lorem ipsum dolor sit amet"
    )

    response = auth_client.get("/api/status/1/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_retrieve_status_404(auth_client):
    """
    Test retrieving a status that does not exist.

    Args:
        auth_client (APIClient): The authenticated APIClient instance.
    """
    response = auth_client.get("/api/status/1/")

    assert response.status_code == 404


@pytest.mark.django_db
def test_update_status(user, auth_client):
    """
    Test updating a status.

    Args:
        user (User): The user object created by the 'user' fixture.
        auth_client (APIClient): The authenticated APIClient instance.
    """
    status = models.Status.objects.create(
        user_id=user.id, content="Lorem ipsum dolor sit amet"
    )

    payload = dict(content="risus in hendrerit gravida rutrum")

    response = auth_client.put(f"/api/status/{status.id}/", payload)

    status.refresh_from_db()

    assert response.data["id"] == status.id
    assert response.data["user"]["id"] == user.id
    assert status.content == payload["content"]


@pytest.mark.django_db
def test_delete_status(user, auth_client):
    """
    Test deleting a status.

    Args:
        user (User): The user object created by the 'user' fixture.
        auth_client (APIClient): The authenticated APIClient instance.
    """
    status = models.Status.objects.create(
        user_id=user.id, content="Lorem ipsum dolor sit amet"
    )

    response = auth_client.delete(f"/api/status/{status.id}/")

    assert response.status_code == 204

    with pytest.raises(models.Status.DoesNotExist):
        status.refresh_from_db()
