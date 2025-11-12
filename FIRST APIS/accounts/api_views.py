from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer, ChangePasswordSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            
            return Response({
                'message': 'User registered successfully!',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'tokens': tokens
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({
                'error': 'Please provide both username and password'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                tokens = get_tokens_for_user(user)
                
                return Response({
                    'message': 'Login successful!',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                    },
                    'tokens': tokens
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Account is disabled'
                }, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            
            if not refresh_token:
                return Response({
                    'error': 'Refresh token is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({
                'message': 'Logout successful!'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({
            'user': serializer.data
        }, status=status.HTTP_200_OK)


class UpdateUserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully!',
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            user = request.user
            
            if not user.check_password(serializer.validated_data.get('old_password')):
                return Response({
                    'error': 'Old password is incorrect'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data.get('new_password'))
            user.save()
            
            return Response({
                'message': 'Password changed successfully!'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProtectedDataAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({
            'message': 'This is protected data!',
            'user': request.user.username,
            'user_id': request.user.id,
            'email': request.user.email,
            'data': {
                'info': 'Only authenticated users can see this',
            }
        }, status=status.HTTP_200_OK)
