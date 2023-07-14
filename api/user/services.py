import dataclasses
import datetime
import jwt
from typing import TYPE_CHECKING
from django.conf import settings

from . import models

if TYPE_CHECKING:
    from .models import User

"""
This data class represents a user.

It contains the user's first name, last name, email, password, and ID.
"""


@dataclasses.dataclass
class UserDataClass:
    first_name: str
    last_name: str
    email: str
    password: str = None
    id: int = None

    @classmethod
    def from_instance(cls, user_model: "User") -> "UserDataClass":
        """
        This method creates a UserDataClass from a User model.

        Args:
            user_model: The User model to create the UserDataClass from.

        Returns:
            The UserDataClass created from the User model.
        """
        return cls(
            first_name=user_model.first_name,
            last_name=user_model.last_name,
            email=user_model.email,
            id=user_model.id,
        )


def create_user(user_dc: "UserDataClass") -> "UserDataClass":
    """
    This function creates a new user.

    Args:
        user_dc: The UserDataClass to create the user from.

    Returns:
        The UserDataClass created from the user_dc.
    """
    instance = models.User(
        first_name=user_dc.first_name,
        last_name=user_dc.last_name,
        email=user_dc.email,
    )

    if user_dc.password is not None:
        instance.set_password(user_dc.password)

    instance.save()

    return UserDataClass.from_instance(instance)


def user_email_selector(email: str) -> "User":
    """
    This function selects a user by email.

    Args:
        email: The email of the user to select.

    Returns:
        The User object selected by email.
    """
    user = models.User.objects.filter(email=email).first()

    return user


def create_token(user_id: int) -> str:
    """
    This function creates a JWT token for a user.

    Args:
        user_id: The ID of the user to create the token for.

    Returns:
        The JWT token created for the user.
    """
    payload = dict(
        id=user_id,
        exp=datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        iat=datetime.datetime.utcnow(),
    )

    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

    return token
