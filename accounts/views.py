from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import logging

from .models import CustomUser

logger = logging.getLogger(__name__)


@csrf_exempt
@api_view(['POST'])
def register_user(request):
    try:
        data = request.data

        first_name = data.get('first_name', '').strip()
        last_name  = data.get('last_name',  '').strip()
        email      = data.get('email',      '').strip().lower()
        password   = data.get('password',   '')
        phone      = data.get('phone',      '').strip()
        role       = data.get('role',       'tenant')

        if not first_name or not last_name or not email or not password:
            return Response(
                {'error': 'First name, last name, email and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if CustomUser.objects.filter(email=email).exists():
            return Response(
                {'error': 'An account with this email already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = CustomUser.objects.create_user(
            username   = email,
            email      = email,
            password   = password,
            first_name = first_name,
            last_name  = last_name,
            phone      = phone,
            role       = role
        )

        logger.info(f"New user registered: {email} as {role}")

        return Response({
            'message': 'Registration successful',
            'user': {
                'id':         user.id,
                'first_name': user.first_name,
                'last_name':  user.last_name,
                'email':      user.email,
                'phone':      user.phone,
                'role':       user.role
            }
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return Response(
            {'error': f'Registration failed: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@csrf_exempt
@api_view(['POST'])
def login_user(request):
    try:
        data     = request.data
        email    = data.get('email',    '').strip().lower()
        password = data.get('password', '')

        if not email or not password:
            return Response(
                {'error': 'Email and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=email, password=password)

        if user is None:
            return Response(
                {'error': 'Invalid email or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        logger.info(f"User logged in: {email}")

        return Response({
            'message': 'Login successful',
            'user': {
                'id':         user.id,
                'first_name': user.first_name,
                'last_name':  user.last_name,
                'email':      user.email,
                'phone':      user.phone,
                'role':       user.role
            }
        }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return Response(
            {'error': f'Login failed: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@csrf_exempt
@api_view(['GET', 'PUT'])
def user_profile(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        return Response({
            'user': {
                'id':          user.id,
                'first_name':  user.first_name,
                'last_name':   user.last_name,
                'email':       user.email,
                'phone':       user.phone,
                'role':        user.role,
                'date_joined': user.date_joined
            }
        })

    elif request.method == 'PUT':
        data = request.data

        user.first_name = data.get('first_name', user.first_name)
        user.last_name  = data.get('last_name',  user.last_name)
        user.phone      = data.get('phone',      user.phone)
        user.save()

        logger.info(f"Profile updated for user: {user.email}")

        return Response({'message': 'Profile updated successfully'})