import random
from rest_framework.response import Response
from rest_framework import status
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

def generate_10_digit_id():
    # Generate a random 10-digit number
    return random.randint(10**9, 10**10 - 1)

def validate_email(email):
    """
    Validates the email address.
    
    Args:
        email (str): The email address to validate.
        
    Returns:
        bool: True if the email address is valid, False otherwise.
    """
    try:
        validate_email(email)  # Raises ValidationError if email is invalid
        return True
    except ValidationError:
        return False

def validate_required_fields(data, required_fields):
    """
    Validates that all required fields are present in the data.
    
    Args:
        data (dict): The incoming request data.
        required_fields (list): List of fields that are required.
    
    Returns:
        Response: If any field is missing, returns a 400 Bad Request response.
        None: If all fields are present.
    """
    for field in required_fields:
        if field not in data or not data[field]:
            return Response({'message': f'{field} is required and cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        # if field == 'email':
        #     if not validate_email(data[field]):
        #         return Response({'message': 'Invalid email address'}, status=status.HTTP_400_BAD_REQUEST)
    return None

# Secret key for signing the tokens (keep this secure in production)
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

def create_access_token(payload):
    """
    Creates an access token valid for 1 hour.
    
    Args:
        payload (dict): Data to include in the token (e.g., user ID, roles).
    
    Returns:
        str: The encoded JWT access token.
    """
    # Set the expiration time to 1 hour from now
    expiration = datetime.utcnow() + timedelta(hours=1)
    payload.update({'exp': expiration})  # Add expiration to the payload
    return jwt.encode(payload=payload, key=SECRET_KEY, algorithm='HS256')

def create_refresh_token(payload):
    """
    Creates a refresh token valid for 5 days.
    
    Args:
        payload (dict): Data to include in the token (e.g., user ID).
    
    Returns:
        str: The encoded JWT refresh token.
    """
    # Set the expiration time to 5 days from now
    expiration = datetime.utcnow() + timedelta(days=5)
    payload.update({'exp': expiration})  # Add expiration to the payload
    return jwt.encode(payload=payload, key=SECRET_KEY, algorithm='HS256')

def decode_token(token):
    """
    Decodes and verifies a JWT token.
    
    Args:
        token (str): The JWT token to decode.
    
    Returns:
        dict: The decoded payload if the token is valid.
    
    Raises:
        jwt.ExpiredSignatureError: If the token has expired.
        jwt.InvalidTokenError: If the token is invalid.
    """
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception('Token has expired')
    except jwt.InvalidTokenError:
        raise Exception('Invalid token')