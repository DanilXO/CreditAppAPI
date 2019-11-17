from django.contrib import admin
from django.contrib.auth.models import Group

from apps.users.models import UserWithRole
from project.admin.mixins import ClickModelAdminMixin

admin.site.unregister(Group)


@admin.register(UserWithRole)
class UserAdmin(ClickModelAdminMixin, admin.ModelAdmin):
    fields = ('username', 'email', 'role', 'first_name', 'last_name',
              'last_login', 'date_joined')
    readonly_fields = ('last_login', 'date_joined')
    list_display = ('id', 'username', 'role', 'last_login')
    list_filter = ('last_login', 'date_joined', 'role')
    search_fields = ('username', 'email', 'first_name', 'last_name')

