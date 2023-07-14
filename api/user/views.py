from rest_framework import views, response, exceptions, permissions

from . import serializer as user_serialzier
from . import services, authentication


"""
This class defines the `/api/register` endpoint.

It allows users to register for the application.
"""


class RegisterApi(views.APIView):
    def post(self, request):
        """
        This method handles POST requests to the endpoint.

        It validates the request data and creates a new user account.
        """
        serializer = user_serialzier.UserSerialzier(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        serializer.instance = services.create_user(user_dc=data)

        return response.Response(data=serializer.data)


"""
This class defines the `/api/login` endpoint.

It allows users to login to the application.
"""


class LoginApi(views.APIView):
    def post(self, request):
        """
        This method handles POST requests to the endpoint.

        It validates the request data and logs the user in, saved the jwt token in a cookies.
        """
        email = request.data["email"]
        password = request.data["password"]

        user = services.user_email_selector(email=email)

        if user is None:
            raise exceptions.AuthenticationFailed("Invalid Credentials")

        if not user.check_password(raw_password=password):
            raise exceptions.AuthenticationFailed("Invalid Credentials")

        token = services.create_token(user_id=user.id)

        resp = response.Response()

        resp.set_cookie(key="jwt", value=token, httponly=True)

        return resp


"""
This class defines the `/api/user` endpoint.

This endpoint can only be used if the user is authenticated.
"""


class UserApi(views.APIView):
    authentication_classes = (authentication.CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """
        This method handles GET requests to the endpoint.

        It returns the user's account information.
        """
        user = request.user
        serializer = user_serialzier.UserSerialzier(user)

        return response.Response(data=serializer.data)


"""
This class defines the `/api/logout` endpoint.

This endpoint can only be used if the user is authenticated.
"""


class LogoutApi(views.APIView):
    authentication_classes = (authentication.CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        """
        This method handles POST requests to the endpoint.

        It logs the user out and deletes the jwt cookie.
        """
        resp = response.Response()
        resp.delete_cookie("jwt")
        resp.data = {"message": "Logout complete"}

        return resp
