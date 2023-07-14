import dataclasses
import datetime

from typing import TYPE_CHECKING

from rest_framework import exceptions
from django.shortcuts import get_object_or_404

from user import services as user_services
from . import models as status_models

if TYPE_CHECKING:
    from .models import Status
    from user.models import User

"""
This data class represents a status.

It contains the status's content, date published, user, and ID.
"""


@dataclasses.dataclass
class StatusDataClass:
    content: str
    date_published: datetime.datetime = None
    user: user_services.UserDataClass = None
    id: int = None

    @classmethod
    def from_instance(cls, status_model: "Status") -> "StatusDataClass":
        """
        This method creates a StatusDataClass from a Status model.

        Args:
            status_model: The Status model to create the StatusDataClass from.

        Returns:
            The StatusDataClass created from the Status model.
        """

        return cls(
            content=status_model.content,
            date_published=status_model.date_published,
            id=status_model.id,
            user=status_model.user,
        )


def create_status(user, status_dc: "StatusDataClass") -> "StatusDataClass":
    """
    This function creates a new status.

    Args:
        user: The user who created the status.
        status_dc: The StatusDataClass to create the status from.

    Returns:
        The StatusDataClass created from the status_dc.
    """
    status_create = status_models.Status.objects.create(
        content=status_dc.content,
        user=user,
    )

    return StatusDataClass.from_instance(status_model=status_create)


def get_user_status(user: "User") -> list["StatusDataClass"]:
    """
    This function gets the statuses for a user.

    Args:
        user: The user to get the statuses for.

    Returns:
        A list of StatusDataClass objects for the user.
    """
    user_status = status_models.Status.objects.filter(user=user)

    return [
        StatusDataClass.from_instance(single_status)
        for single_status in user_status
    ]


def get_user_status_details(status_id: int) -> "StatusDataClass":
    """
    This function gets the details of a status.

    Args:
        status_id: The ID of the status to get the details for.

    Returns:
        The StatusDataClass for the status.
    """
    status = get_object_or_404(status_models.Status, pk=status_id)

    return StatusDataClass.from_instance(status_model=status)


def delete_user_status(user: "User", status_id: int) -> "StatusDataClass":
    """
    This function deletes a status.

    Args:
        user: The user who owns the status.
        status_id: The ID of the status to delete.

    Returns:
        The StatusDataClass for the deleted status.
    """
    status = get_object_or_404(status_models.Status, pk=status_id)

    if status.user.id != user.id:
        raise exceptions.PermissionDenied("Forbidden")

    # It is not recommended to delete objects from the database because it can affect its performance in the future
    status.delete()


def update_user_status(
    user: "User", status_id: int, status_data: "StatusDataClass"
):
    """
    This function updates a status.

    Args:
        user: The user who owns the status.
        status_id: The ID of the status to update.
        status_data: The updated status data.

    Returns:
        The StatusDataClass for the updated status.
    """
    status = get_object_or_404(status_models.Status, pk=status_id)

    if status.user.id != user.id:
        raise exceptions.PermissionDenied("Forbidden")

    status.content = status_data.content
    status.save()

    return StatusDataClass.from_instance(status_model=status)
