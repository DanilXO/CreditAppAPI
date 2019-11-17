from django.contrib import admin

from apps.credit import models
from project.admin.mixins import ClickModelAdminMixin


@admin.register(models.CustomerProfile)
class CustomerProfileAdmin(ClickModelAdminMixin, admin.ModelAdmin):
    fields = ('partner', 'first_name', 'last_name', 'phone', 'email',
              'passport', 'scoring_score', 'created', 'updated')
    readonly_fields = ('created', 'updated')
    list_display = ('id', 'partner_name', 'first_name', 'last_name', 'created', 'updated')
    list_filter = ('created', 'updated', 'scoring_score')
    search_fields = ('partner__username', 'first_name', 'last_name', 'phone', 'email', 'passport')


@admin.register(models.LoanOffer)
class LoanOfferAdmin(ClickModelAdminMixin, admin.ModelAdmin):
    fields = ('organization', 'name', 'start_rotation', 'end_rotation', 'min_scoring_score',
              'max_scoring_score', 'type', 'created', 'updated')
    readonly_fields = ('created', 'updated')
    list_display = ('id', 'organization_name', 'name', 'start_rotation', 'end_rotation',
                    'created', 'updated')
    list_filter = ('created', 'updated', 'start_rotation', 'end_rotation',
                   'min_scoring_score', 'max_scoring_score')
    search_fields = ('organization__username', 'name', )


@admin.register(models.LoanRequest)
class LoanRequestAdmin(ClickModelAdminMixin, admin.ModelAdmin):
    fields = ('customer', 'offer', 'status', 'sent', 'created')
    readonly_fields = ('created', )
    list_display = ('id', 'customer_name', 'offer_name', 'status', 'created')
    list_filter = ('customer', 'offer', 'status', 'created')
    search_fields = ('customer__partner__username', 'customer__partner__first_name', 'customer__partner__last_name',
                     'customer__partner__phone', 'customer__partner__email',
                     'offer__organization__username', 'offer__name')
