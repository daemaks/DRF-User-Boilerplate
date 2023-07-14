from django.conf import settings
from rest_framework import authentication, exceptions
import jwt

from . import models

"""
This class is a custom authentication class that uses JWT tokens.

It authenticates users by decoding the JWT token in the request cookies.
"""


class CustomUserAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        """
        This method authenticates the user.

        It gets the JWT token from the request cookies and decodes it.
        If the token is valid, it returns the user object.
        """
        token = request.COOKIES.get("jwt")

        if not token:
            return None

        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET, algorithms=["HS256"]
            )
        except:
            raise exceptions.AuthenticationFailed("Unauthorized")

        user = models.User.objects.filter(id=payload["id"]).first()

        return (user, None)
