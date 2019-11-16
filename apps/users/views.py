from rest_framework import generics

from apps.users import models, serializers


class SignUp(generics.CreateAPIView):
    queryset = models.UserWithRole.objects.all()
    serializer_class = serializers.UserSerializer
