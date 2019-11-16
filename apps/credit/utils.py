from rest_framework import generics


class PermissionAPIMixin(generics.GenericAPIView):
    """ Mixin добавляющий default ограничения на все методы """
    permission_classes = [IsAuthenticated, IsSubscriptionPermission, HasRolePermission]
    required_roles = {
        # роли, которые имеют доступ к запросам
        'GET': [ADMIN, OWNER],
        'POST': [ADMIN, OWNER],
        'PUT': [ADMIN, OWNER],
        'DELETE': [ADMIN, OWNER],
        'PATCH': [ADMIN, OWNER],
        'HEAD': [ADMIN, OWNER],
        'OPTIONS': [ADMIN, OWNER],
        # 'POST': ['__all__'],
    }