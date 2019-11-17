from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from apps.credit import models
from apps.credit.mixins import ValidateModelMixin
from apps.credit.permissions import role_is
from apps.users import conf
from apps.users.serializers import UserDetailSerializer


class CustomerProfileSerializer(ValidateModelMixin, serializers.ModelSerializer):
    def get_fields(self, *args, **kwargs):
        """ Динамически убираем поле выбора partner """
        fields = super(CustomerProfileSerializer, self).get_fields()
        request = self.context.get('request', None)
        if role_is(request.user, conf.PARTNER_ROLE):
            fields.pop('partner')
        return fields

    def validate(self, validated_data):
        """ Валидация данных с автомотической подменой partner на текущего user """
        request = self.context.get('request', None)
        if role_is(request.user, conf.PARTNER_ROLE) and validated_data.get('partner') is None:
            validated_data['partner'] = request.user
        return validated_data

    class Meta:
        model = models.CustomerProfile
        fields = ('id', 'partner', 'first_name', 'last_name', 'phone', 'email', 'passport',
                  'scoring_score', 'created', 'updated')
        read_only_fields = ('id', 'created', 'updated',)


class CustomerProfileDetailSerializer(CustomerProfileSerializer):
    partner = UserDetailSerializer(read_only=True)


class LoanOfferSerializer(ValidateModelMixin, serializers.ModelSerializer):
    class Meta:
        model = models.LoanOffer
        fields = ('id', 'organization', 'name', 'start_rotation', 'end_rotation', 'min_scoring_score',
                  'max_scoring_score', 'type', 'created', 'updated')
        read_only_fields = ('id', 'created', 'updated',)


class LoanOfferDetailSerializer(LoanOfferSerializer):
    organization = UserDetailSerializer(read_only=True)
    type = serializers.SerializerMethodField()

    @staticmethod
    def get_type(obj):
        return {'id': obj.type, 'name': obj.type_name}


class LoanRequestSerializer(ValidateModelMixin, serializers.ModelSerializer):

    def validate(self, attrs):
        request = self.context.get('request', None)
        if request and role_is(request.user, conf.ORGANISATION_ROLE) and \
                not(len(attrs) == 1 and attrs.get('status')):
            raise PermissionDenied('You do not have permission to perform this action. '
                                   'You can only change the status of the Loan request.')
        return attrs

    class Meta:
        model = models.LoanRequest
        fields = ('id', 'customer', 'offer', 'status', 'sent', 'created')
        read_only_fields = ('id', 'created')


class LoanRequestDetailSerializer(LoanRequestSerializer):
    customer = CustomerProfileDetailSerializer(read_only=True)
    offer = LoanOfferDetailSerializer(read_only=True)
    status = serializers.SerializerMethodField()

    @staticmethod
    def get_status(obj):
        return {'id': obj.status, 'name': obj.status_name}
