from rest_framework import views, response, permissions
from rest_framework import status as rest_status
from . import serializer as status_serializer
from . import services
from user import authentication


"""
This class defines the `/api/status/create/` and `/api/status/` endpoints.

It allows users to create and list their statuses.
"""


class StatusCreateListApi(views.APIView):
    authentication_classes = (authentication.CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        """
        This method handles POST requests to the endpoint.

        It validates the request data and creates a new status.
        """
        serializer = status_serializer.StatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        serializer.instance = services.create_status(
            user=request.user, status_dc=data
        )

        return response.Response(
            data=serializer.data, status=rest_status.HTTP_201_CREATED
        )

    def get(self, request):
        """
        This method handles GET requests to the endpoint.

        It returns the user's statuses.
        """
        status_collection = services.get_user_status(user=request.user)
        serializer = status_serializer.StatusSerializer(
            status_collection, many=True
        )

        return response.Response(data=serializer.data)


"""
This class defines the `/api/status/<status_id>/` endpoint.

It allows users to retrieve, update, and delete their statuses.
"""


class StatusRetrieveUpdateDelete(views.APIView):
    authentication_classes = (authentication.CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, status_id):
        """
        This method handles GET requests to the endpoint.

        It returns the details of a specific status.
        """
        status = services.get_user_status_details(status_id=status_id)
        serializer = status_serializer.StatusSerializer(status)

        return response.Response(data=serializer.data)

    def delete(self, request, status_id):
        """
        This method handles DELETE requests to the endpoint.

        It deletes a specific status.
        """
        services.delete_user_status(user=request.user, status_id=status_id)

        return response.Response(status=rest_status.HTTP_204_NO_CONTENT)

    def put(self, request, status_id):
        """
        This method handles PUT requests to the endpoint.

        It updates a specific status.
        """
        serializer = status_serializer.StatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status = serializer.validated_data
        serializer.instance = services.update_user_status(
            user=request.user, status_id=status_id, status_data=status
        )

        return response.Response(data=serializer.data)
