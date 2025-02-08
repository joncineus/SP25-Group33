from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        # Extract username and password from request
        username = request.data.get("username")
        password = request.data.get("password")
        
        if not username or not password:
            return Response({
                "detail": "Username and password are required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Authenticate the user
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Generate JWT token for the authenticated user
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            # Return the tokens as a response
            return Response({
                "refresh": str(refresh),
                "access": str(access_token)
            }, status=status.HTTP_200_OK)
        
        # Return error if authentication fails
        return Response({
            "detail": "Invalid credentials"
        }, status=status.HTTP_401_UNAUTHORIZED)