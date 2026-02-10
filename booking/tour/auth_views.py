from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate

@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    """
    Login endpoint for API clients
    POST /api/login/ with email and password
    Returns authentication token
    """
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response(
            {'error': 'Email and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Find user by email
    from django.contrib.auth.models import User
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {'error': 'Invalid email or password'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Authenticate using username
    user_auth = authenticate(username=user.username, password=password)
    
    if user_auth is None:
        return Response(
            {'error': 'Invalid email or password'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Get or create token
    token, created = Token.objects.get_or_create(user=user_auth)
    
    return Response({
        'token': token.key,
        'user_id': user_auth.id,
        'email': user_auth.email,
        'username': user_auth.username,
        'message': 'Login successful'
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def api_logout(request):
    """
    Logout endpoint - deletes token
    """
    if request.user:
        Token.objects.filter(user=request.user).delete()
        return Response(
            {'message': 'Logout successful'},
            status=status.HTTP_200_OK
        )
    return Response(
        {'error': 'Not authenticated'},
        status=status.HTTP_400_BAD_REQUEST
    )
