from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions
from rest_framework.authtoken.models import Token

class BearerTokenAuthentication(BaseAuthentication):

    """
    Custom authentication class for handling Bearer Token authentication.

    This class authenticates incoming requests that include a Bearer token
    in the `Authorization` header.

    Methods:
        - authenticate(request): Parses and validates the Bearer token.
        - authenticate_credentials(key): Verifies the provided token and its associated user.
        - authenticate_header(request): Returns the authentication scheme for the response.

    How it works:
        - The `Authorization` header should be in the format: "Bearer <token>".
        - If valid, the associated user and token are returned.
        - If invalid or missing, an authentication error is raised.

    Raises:
        - AuthenticationFailed: For invalid, missing, or improperly formatted tokens.
        - UnicodeError: If the token contains invalid characters.

    Example:
        Authorization: Bearer <your_token_here>

    Attributes:
        - keyword (str): The expected prefix for the token in the header (default: 'Bearer').
    """
    keyword = 'Bearer'

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed('Invalid token header. No credentials provided.')
        elif len(auth) > 2:
            raise exceptions.AuthenticationFailed('Invalid token header. Token string should not contain spaces.')

        try:
            token = auth[1].decode()
        except UnicodeError:
            raise exceptions.AuthenticationFailed('Invalid token header. Token string should not contain invalid characters.')

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.select_related('user').get(key=key)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token.')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')

        return (token.user, token)

    def authenticate_header(self, request):
        return f'{self.keyword}'
