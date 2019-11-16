# from rest_framework import permissions
# from django.utils.translation import gettext as _
# from rest_framework.exceptions import PermissionDenied, NotAuthenticated
#
#
# def role_is(user, role_name):
#     """
#     Принимает пользователя и имя role и возвращает `True`, если пользователь находится в этой группе.
#     """
#     try:
#         return Role.objects.get(name=role_name) == user.role
#     except (AttributeError, Role.DoesNotExist):
#         return None
#
#
# class HasRolePermission(permissions.BasePermission):
#     """
#     Убедитесь, что пользователь находится в необходимых группах.
#     """
#
#     def has_permission(self, request, view):
#         # if not request.user.is_superuser:
#         #     try:
#         #         if not request.user.company.subscription_is_active:
#         #             raise PermissionDenied(detail="Sorry, the subscription for your company is not active.")
#         #     except AttributeError:
#         #         raise NotAuthenticated()
#
#         # Получить отображение методов -> требуемая группа.
#         required_roles_mapping = getattr(view, "required_roles", {})
#
#         # Определите необходимые группы для этого конкретного метода запроса.
#         required_roles = required_roles_mapping.get(request.method, [])
#
#         # Вернуть True, если у пользователя есть хотя бы одна необходимая группа
#         return any([role_is(request.user, group_name) if group_name != "__all__" else True for group_name in
#                     required_roles]) or (request.user and request.user.is_staff)
#         # Если в будущем понадобится набор групп,
#         # можно сделать проверку на наличие всех указанных, заменив any на all