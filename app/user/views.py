from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer
from user.serializers import AuthTokenSerializer


class CreateUserApiView(generics.CreateAPIView):
    """Creates a new user in the system"""
    serializer_class = UserSerializer


class CreateUserTokenApiView(ObtainAuthToken):
    """Create a new user token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
