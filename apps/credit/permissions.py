from rest_framework import permissions


def role_is(user, role_id):
    """
    Принимает пользователя и имя role и возвращает `True`, если пользователь находится в этой группе.
    """
    return user.role == role_id


class HasRolePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        required_roles_mapping = getattr(view, "required_roles", {})
        required_roles = required_roles_mapping.get(request.method, [])

        # Вернуть True, если у пользователя есть хотя бы одна необходимая группа
        return any([role_is(request.user, group_name) if group_name != "__all__" else True for group_name in
                    required_roles]) or (request.user and request.user.is_staff)
