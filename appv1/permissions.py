from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from .utils import decode_token  # Your JWT decoding utility
from .models import User  # Your custom Profile model

class HasRequiredPermission(BasePermission):
    """
    Custom permission class to check if the Profile has the required permission.
    """

    def has_permission(self, request, view):
        # Check if the Authorization header is present
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise AuthenticationFailed('Authorization header is missing')

        try:
            # Extract the token from the Authorization header
            token = auth_header.split(' ')[1]

            # Decode the token to get the payload
            payload = decode_token(token)

            # Check if the payload contains the user_id
            # if not payload['user_id']:
            #     raise AuthenticationFailed('Invalid token')

            # Retrieve the Profile object
            profile = User.objects.get(user_id=payload['user_id'])

            # Get the required permission from the view

            # If no permission is specified, allow access

            # Check if the Profile has the required permission (role-based or individual)

            return True

        except User.DoesNotExist:
            raise AuthenticationFailed('Profile not found')
        except Exception as e:
            raise AuthenticationFailed('Invalid token')