
from rest_framework import serializers

from apps.credit import models
from apps.credit.mixins import ValidateModelMixin
from apps.credit.permissions import role_is
from apps.users import conf
from apps.users.serializers import UserDetailSerializer


class CustomerProfileSerializer(ValidateModelMixin, serializers.ModelSerializer):
    class Meta:
        model = models.CustomerProfile
        fields = ('id', 'partner', 'first_name', 'last_name', 'phone', 'email', 'passport',
                  'scoring_score', 'created', 'updated')
        read_only_fields = ('id', 'created', 'updated',)


class CustomerProfileDetailSerializer(ValidateModelMixin, serializers.ModelSerializer):
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

    def get_fields(self):
        self.read_only_fields = ('id', 'customer', 'offer', 'sent', 'created')
        return super().get_fields()

    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()
        if role_is(self.context['request'].user, conf.ORGANISATION_ROLE):
            read_only_fields = ('id', 'customer', 'offer', 'sent', 'created')
            for field in read_only_fields:
                extra_kwargs[field] = {'read_only': True}
        return extra_kwargs

    class Meta:
        model = models.LoanOffer
        fields = ('id', 'customer', 'offer', 'status', 'sent', 'created')
        read_only_fields = ('id', 'created')


class LoanRequestDetailSerializer(LoanOfferSerializer):
    customer = CustomerProfileDetailSerializer(read_only=True)
    offer = LoanOfferDetailSerializer(read_only=True)
    status = serializers.SerializerMethodField()

    @staticmethod
    def get_status(obj):
        return {'id': obj.status, 'name': obj.status_name}
