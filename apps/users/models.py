from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.users import conf


class UserWithRoleManager(UserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('role', conf.SUPERUSER_ROLE)
        super().create_superuser(username, email, password, **extra_fields)


class UserWithRole(AbstractUser):
    objects = UserWithRoleManager()
    role = models.PositiveIntegerField(_('role'), choices=conf.ROLES)
    email = models.EmailField(_('email address'), unique=True)

    @property
    def role_name(self):
        return [_ for _ in conf.ROLES if _[0] == self.role][0][1]
