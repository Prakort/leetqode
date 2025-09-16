from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from google.auth.transport import requests
from google.oauth2 import id_token
from .serializers import UserSerializer

User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """Get current user profile."""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])  # No authentication required
@csrf_exempt
def google_auth(request):
    """Handle Google OAuth2 authentication with JWT token."""
    try:
        credential = request.data.get('credential')
        if not credential:
            return Response({'error': 'No credential provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verify the Google ID token
        from django.conf import settings
        CLIENT_ID = getattr(settings, 'GOOGLE_OAUTH2_CLIENT_ID', '283307083033-qh48bj9liq495l3ge5s843s4uhm7q07j.apps.googleusercontent.com')
        
        try:
            idinfo = id_token.verify_oauth2_token(credential, requests.Request(), CLIENT_ID)
        except ValueError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Extract user information
        email = idinfo.get('email')
        name = idinfo.get('name', '')
        picture = idinfo.get('picture', '')
        google_id = idinfo.get('sub')
        
        if not email:
            return Response({'error': 'No email in token'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get or create user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email,
                'first_name': name.split(' ')[0] if name else '',
                'last_name': ' '.join(name.split(' ')[1:]) if name and len(name.split(' ')) > 1 else '',
                'avatar': picture,
                'google_id': google_id,
            }
        )
        
        # Update user info if not created
        if not created:
            user.first_name = name.split(' ')[0] if name else user.first_name
            user.last_name = ' '.join(name.split(' ')[1:]) if name and len(name.split(' ')) > 1 else user.last_name
            user.avatar = picture or user.avatar
            user.google_id = google_id or user.google_id
            user.save()
        
        # Log the user in with the default backend
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        # Ensure session is saved
        request.session.save()
        
        return Response({
            'success': True,
            'user': UserSerializer(user).data,
            'message': 'Authentication successful'
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def auth_status(request):
    """Check authentication status."""
    if request.user.is_authenticated:
        return Response({
            'authenticated': True,
            'user': UserSerializer(request.user).data
        })
    else:
        return Response({
            'authenticated': False,
            'user': None
        })


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])  # No authentication required
@csrf_exempt
def logout(request):
    """Logout user."""
    from django.contrib.auth import logout as django_logout
    django_logout(request)
    return Response({
        'success': True,
        'message': 'Logged out successfully'
    })
