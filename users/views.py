from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationView(APIView):

    """
    API View for user registration.

    Allows new users to register by providing their details.
    Upon successful registration, a token is created and returned
    along with the user's information.

    Permissions:
        - Accessible to anyone (no authentication required).

    Methods:
        POST: Registers a new user.

    Request Payload:
        {
            "username": "string",
            "password": "string",
            "email": "string"
        }

    Response:
        - On success (status 201):
            {
                "user": {
                    "id": 1,
                    "username": "username",
                    "email": "user@example.com"
                },
                "token": "generated_auth_token"
            }
        - On validation error (status 400):
            {
                "error_field": ["error_message"]
            }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Create a token for the user
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': serializer.data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):

    """
    API View for user login.

    Authenticates users with their username and password. If valid,
    returns an authentication token, user ID, and username.

    Permissions:
        - Accessible to anyone (no authentication required).

    Methods:
        POST: Logs in a user.

    Request Payload:
        {
            "username": "string",
            "password": "string"
        }

    Response:
        - On success (status 200):
            {
                "token": "auth_token",
                "user_id": 1,
                "username": "username"
            }
        - On authentication failure (status 401):
            {
                "error": "Invalid Credentials"
            }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            # Get or create token for the user
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username
            })

        return Response({
            'error': 'Invalid Credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)