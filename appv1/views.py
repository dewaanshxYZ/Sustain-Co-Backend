from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User, Contact
from .serializers import UserSerializer
from django.contrib.auth.hashers import make_password, check_password
from .utils import validate_required_fields, create_access_token, create_refresh_token
from datetime import datetime
from .mapbox import update_figure
import plotly.io as pio
from .permissions import HasRequiredPermission

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        data = request.data

        required_fields = ['name', 'email', 'password']
        validation_error = validate_required_fields(data, required_fields)

        if validation_error:
            return validation_error
        
        # Check if user already exists
        try:
            exist_user = User.objects.get(email=data['email'])
            return Response({'message': 'User already exists', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass

        # Create User
        try:
            user = User.objects.create(
                name=data['name'],
                email=data['email'],
                password=make_password(data['password']),
                phone = data.get('phone', None)
            )
            user.save()
            return Response({'message': 'User created Succesfully!', 'success': True}, status=status.HTTP_201_CREATED)
        except:
            return Response({'message': 'Internal Server Error', 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GetAllUsersView(APIView):
    def get(self, request):
        users = User.objects.all()
        user_serializer = UserSerializer(users, many=True)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    
class UserDetailView(APIView):
    def get(self, request, user_id):
        user = User.objects.get(user_id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LoginView(APIView):
    def post(self, request):
        data = request.data

        required_fields = ['email', 'password']
        
        validation_error = validate_required_fields(data, required_fields)

        if validation_error:
            return validation_error
        
        # Check if user exists
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            return Response({'message': 'User does not exist please login!', 'success': False}, status==status.HTTP_400_BAD_REQUEST)
        
        # Check if password is correct
        if not check_password(data['password'], user.password):
            return Response({'message': 'Invalid Password', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
        
        user.last_login = datetime.now()
        user.save()
        
        user_serializer = UserSerializer(user)
        # Create tokens and a session
        access_token = create_access_token(user_serializer.data)
        refresh_token = create_refresh_token(user_serializer.data)

        return Response({'message': 'Login Succesfull!', 'access_token': access_token, 'refresh_token': refresh_token, 'user_id': user.user_id, 'success': True}, status=status.HTTP_200_OK)

class GraphDataView(APIView):
    permission_classes = [HasRequiredPermission]
    required_permission = 'authenticated'
    def get(self, request):
        # Generate the Plotly figure
        graph_data = update_figure(None, 1984, None, None, 0)
        
        # Convert the Plotly figure to a JSON string
        graph_json = pio.to_json(graph_data)
        
        # Return the JSON string in the API response
        return Response(graph_json, status=status.HTTP_200_OK)
    
class RefetchGraphDataView(APIView):
    permission_classes=[HasRequiredPermission]
    required_permission = 'authenticated'
    def post(self, request):
        data = request.data

        print(data)

        graph_data = update_figure(data['value'], data['year'], None, None, 0)
        
        # Convert the Plotly figure to a JSON string
        graph_json = pio.to_json(graph_data)
        
        # Return the JSON string in the API response
        return Response(graph_json, status=status.HTTP_200_OK)
    
class ContactView(APIView):
    def post(self, request):
        data = request.data

        required_fields = ['name', 'email', 'subject', 'message']
        validation_error = validate_required_fields(data, required_fields)

        if validation_error:
            return validation_error
        
        # Check if user already exists
        try:
            exist_user = Contact.objects.get(email=data['email'])
            return Response({'message': 'We have already received your response', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass

        # Create User
        try:
            user = Contact.objects.create(
                name=data['name'],
                email=data['email'],
                subject=data['subject'],
                message=data['message']
            )
            user.save()
            return Response({'message': 'Thank You! We will contact you soon', 'success': True}, status=status.HTTP_201_CREATED)
        except:
            return Response({'message': 'Internal Server Error', 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)