from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import  Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import CustomUserModel, UserProfileModel, UserVideoModel
from .serializers import CustomUserSerializer, UserProfileSerializer, UserVideoSerializer
from .utils import get_tokens_for_user


class RegisterView(APIView):

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self, request):
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Please provide your email and/or password.'}, status=status.HTTP_400_BAD_REQUEST)
        
        email = request.data['email']
        password = request.data['password']
        user = authenticate(request, email = email, password = password)
        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            return Response({'msg': 'You have successfully logged in.', **auth_data}, status=status.HTTP_200_OK)
        
        return Response({'msg': 'Invalid email and password combinations.'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):

    def post(self, request):
        logout(request)
        return Response({'msg': 'You have successfully logged out.'}, status=status.HTTP_200_OK)
    

class UserProfileView(APIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        profile = UserProfileModel.objects.get(user=request.user.id)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user = self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        profile = UserProfileModel.objects.get(user=request.user.id)
        serializer = UserProfileSerializer(profile, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        profile = UserProfileModel.objects.get(user=request.user.id)
        serializer = UserProfileSerializer(profile, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserVideoView(APIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        videos = UserVideoModel.objects.filter(user=request.user.id)
        serializer = UserVideoSerializer(videos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserVideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user = self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        return Response({'method': 'put'})

    def patch(self, request):
        return Response({'method': 'patch'})

