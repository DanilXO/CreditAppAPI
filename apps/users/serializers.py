from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError as RestValidationError
from apps.users import conf, models


class UserSerializer(serializers.ModelSerializer):
    ROLES = (
        (conf.PARTNER_ROLE, 'Partner'),
        (conf.ORGANISATION_ROLE, 'Organization'),
    )
    role = serializers.ChoiceField(choices=ROLES)

    def create(self, validated_data):
        try:
            user = super().create(validated_data)
            user.set_password(validated_data.get('password'))
            user.save()
            return user
        except ValidationError as ex:
            raise RestValidationError(ex.message_dict)

    class Meta:
        model = models.UserWithRole
        fields = ('id', 'username', 'email', 'role', 'password')
        write_only_fields = ('password', )


class UserDetailSerializer(UserSerializer):
    role = serializers.SerializerMethodField()

    @staticmethod
    def get_role(obj):
        return {'id': obj.role, 'name': obj.role_name}
