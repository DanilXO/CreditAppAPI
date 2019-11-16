from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.conf import settings


class UserWithRole(models.Model):
    PARTNER_ROLE = 1
    ORGANISATION_ROLE = 2
    SUPERUSER_ROLE = 3
    ROLES = (
        (PARTNER_ROLE, 'Partner'),
        (ORGANISATION_ROLE, 'Organization'),
        (SUPERUSER_ROLE, 'Superuser')
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.PositiveIntegerField(_('role'), choices=ROLES)

    class Meta:
        abstract = True


class Partner(UserWithRole):
    """ Партнеры """
    def save(self, *args, **kwargs):
        self.role = self.PARTNER_ROLE
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('partner')
        verbose_name_plural = _('partners')


class CreditOrganization(UserWithRole):
    """ Кредитная организация """
    def save(self, *args, **kwargs):
        self.role = self.ORGANISATION_ROLE
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('credit organization')
        verbose_name_plural = _('credit organizations')


class CustomerProfile(models.Model):
    """ Анкета клиента """
    partner = models.ForeignKey(Partner, null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(_('first name'), max_length=128)
    last_name = models.CharField(_('last name'), max_length=128)
    phone = models.CharField(_('phone'), max_length=16, unique=True)
    email = models.EmailField(_('email'), max_length=255, blank=True, null=True)
    passport = models.IntegerField(_('passport number'))
    scoring_score = models.PositiveIntegerField(_('scoring score'))

    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    class Meta:
        verbose_name = _('customer profile')
        verbose_name_plural = _('customer profiles')


class LoanOffer(models.Model):
    """ Кредитное предложение """
    CONSUMER_CREDIT_TYPE = 1
    MORTGAGE_TYPE = 2
    CAR_LOAN_TYPE = 3
    LOAN_TYPES = (
        (CONSUMER_CREDIT_TYPE, 'Consumer credit'),
        (MORTGAGE_TYPE, 'Mortgage'),
        (CAR_LOAN_TYPE, 'Car loan')
    )
    organization = models.ForeignKey(CreditOrganization, null=True, on_delete=models.SET_NULL)

    name = models.CharField(_('first name'), max_length=256)
    start_rotation = models.DateTimeField(_('start of rotation'))
    end_rotation = models.DateTimeField(_('end of rotation'))
    min_scoring_score = models.PositiveIntegerField(_('min scoring score'))
    max_scoring_score = models.PositiveIntegerField(_('max scoring score'))
    type = models.PositiveIntegerField(_('type'), choices=LOAN_TYPES)

    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    def clean(self):
        if self.max_scoring_score < self.min_scoring_score:
            raise ValidationError(_('The maximum scoring score should be more than the minimum scoring score'))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('loan offer')
        verbose_name_plural = _('loan offers')


class LoanRequest(models.Model):
    NEW_STATUS = 1
    SENT_STATUS = 2
    RECEIVED_STATUS = 3
    APPROVED_STATUS = 4
    DENIED_STATUS = 5
    ISSUED_STATUS = 6
    STATUS_TYPES = (
        (NEW_STATUS, 'New'),
        (SENT_STATUS, 'Sent'),
        (RECEIVED_STATUS, 'Received'),
        (APPROVED_STATUS, 'Approved'),
        (DENIED_STATUS, 'Denied'),
        (ISSUED_STATUS, 'Issued'),
    )
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    offer = models.ForeignKey(LoanOffer, on_delete=models.CASCADE)
    status = models.PositiveIntegerField(_('status'), choices=STATUS_TYPES)
    send = models.DateTimeField(_('sending date'))
    created = models.DateTimeField(_('created'), auto_now_add=True)
