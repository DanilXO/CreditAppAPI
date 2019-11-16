from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.credit import models, serializers
from apps.credit.mixins import CustomMethodsAPIMixin
from apps.credit.permissions import role_is
from apps.users import conf


class ApiRoot(APIView):
    """ Возвращающает список всех конечных точек. """
    @staticmethod
    def get(request, format=None):
        if request.user.is_authenticated:
            response_data = {
                'customer-profiles': reverse('credit:customer-profiles-list', request=request, format=format),
                'loan-offers': reverse('credit:loan-offers-list', request=request, format=format),
                'loan-requests': reverse('credit:loan-requests-list', request=request, format=format),
                'logout': reverse('rest_framework:logout', request=request, format=format),
            }
        else:
            response_data = {
                'sign-up': reverse('users:sign-up', request=request, format=format),
                'login': reverse('rest_framework:login', request=request, format=format),
            }
        return Response(response_data)


class CustomerProfileViewSet(CustomMethodsAPIMixin, ModelViewSet):
    """ ViewSet для CustomerProfile """
    queryset = models.CustomerProfile.objects.all()
    serializer_class = serializers.CustomerProfileSerializer
    detail_serializer_class = serializers.CustomerProfileDetailSerializer

    required_roles = {
        # Роли, которые имеют доступ к запросам
        'GET': [conf.SUPERUSER_ROLE, conf.PARTNER_ROLE],
        'POST': [conf.SUPERUSER_ROLE, conf.PARTNER_ROLE],
        'PUT': [conf.SUPERUSER_ROLE],
        'DELETE': [conf.SUPERUSER_ROLE],
        'PATCH': [conf.SUPERUSER_ROLE],
        'HEAD': [conf.SUPERUSER_ROLE, conf.PARTNER_ROLE],
        'OPTIONS': [conf.SUPERUSER_ROLE, conf.PARTNER_ROLE],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if role_is(self.request.user, conf.PARTNER_ROLE):
            return queryset.filter(partner=self.request.user)
        return queryset


class LoanOfferViewSet(CustomMethodsAPIMixin, ModelViewSet):
    """ ViewSet для LoanOffer """
    required_roles = {
        # Роли, которые имеют доступ к запросам
        'GET': [conf.SUPERUSER_ROLE, conf.PARTNER_ROLE, conf.ORGANISATION_ROLE],
        'POST': [conf.SUPERUSER_ROLE, conf.ORGANISATION_ROLE],
        'PUT': [conf.SUPERUSER_ROLE],
        'DELETE': [conf.SUPERUSER_ROLE],
        'PATCH': [conf.SUPERUSER_ROLE],
        'HEAD': [conf.SUPERUSER_ROLE, conf.PARTNER_ROLE, conf.ORGANISATION_ROLE],
        'OPTIONS': [conf.SUPERUSER_ROLE, conf.PARTNER_ROLE, conf.ORGANISATION_ROLE],
    }

    queryset = models.LoanOffer.objects.all()
    serializer_class = serializers.LoanOfferSerializer
    detail_serializer_class = serializers.LoanOfferDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if role_is(self.request.user, conf.ORGANISATION_ROLE):
            return queryset.filter(organization=self.request.user)
        return queryset


class LoanRequestViewSet(CustomMethodsAPIMixin, ModelViewSet):
    """ ViewSet для LoanRequest """
    required_roles = {
        # Роли, которые имеют доступ к запросам
        'GET': [conf.SUPERUSER_ROLE, conf.PARTNER_ROLE, conf.ORGANISATION_ROLE],
        'POST': [conf.SUPERUSER_ROLE, conf.PARTNER_ROLE],
        'PUT': [conf.SUPERUSER_ROLE],
        'DELETE': [conf.SUPERUSER_ROLE],
        'PATCH': [conf.SUPERUSER_ROLE, conf.ORGANISATION_ROLE],
        'HEAD': [conf.SUPERUSER_ROLE, conf.PARTNER_ROLE, conf.ORGANISATION_ROLE],
        'OPTIONS': [conf.SUPERUSER_ROLE, conf.PARTNER_ROLE, conf.ORGANISATION_ROLE],
    }

    queryset = models.LoanRequest.objects.all()
    serializer_class = serializers.LoanRequestSerializer
    detail_serializer_class = serializers.LoanRequestDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if role_is(self.request.user, conf.ORGANISATION_ROLE):
            return queryset.filter(offer__organization=self.request.user)
        elif role_is(self.request.user, conf.PARTNER_ROLE):
            return queryset.filter(customer__partner=self.request.user)
        return queryset
