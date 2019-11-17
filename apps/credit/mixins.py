from django.core.exceptions import ValidationError
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.credit.permissions import HasRolePermission
from rest_framework.exceptions import ValidationError as RestValidationError


class PermissionAPIMixin(generics.GenericAPIView):
    """ Mixin добавляющий default ограничения на все методы """
    permission_classes = [IsAuthenticated, HasRolePermission]
    required_roles = {
        # роли, которые имеют доступ к запросам
        'GET': ['__all__'],
        'POST': ['__all__'],
        'PUT': ['__all__'],
        'DELETE': ['__all__'],
        'PATCH': ['__all__'],
        'HEAD': ['__all__'],
        'OPTIONS': ['__all__'],
    }


class CustomMethodsAPIMixin(PermissionAPIMixin, generics.GenericAPIView):
    """
    Персонализированный mixin класс с общими пользовательскими методами
    и настройками для views
    """
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.request.method == 'GET' and self.detail_serializer_class:
            return self.detail_serializer_class
        return self.serializer_class


class ValidateModelMixin:
    """ Миксин для обработки django.admin.exceptions.ValidationError
    и пробрасывания rest_framework.exceptions.ValidationError
    """
    def update(self, *args, **kwargs):
        try:
            return super().update(*args, **kwargs)
        except ValidationError as ex:
            raise RestValidationError(ex.message_dict)

    def create(self, *args, **kwargs):
        try:
            return super().create(*args, **kwargs)
        except ValidationError as ex:
            raise RestValidationError(ex.message_dict)
