from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from apps.users import conf

User = settings.AUTH_USER_MODEL


class CustomerProfile(models.Model):
    """ Анкета клиента """
    partner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(_('first name'), max_length=128)
    last_name = models.CharField(_('last name'), max_length=128)
    phone = models.CharField(_('phone'), max_length=16, unique=True)
    email = models.EmailField(_('email'), max_length=255, blank=True, null=True)
    passport = models.IntegerField(_('passport number'))
    scoring_score = models.PositiveIntegerField(_('scoring score'))

    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    def clean(self):
        if self.partner.role not in (conf.PARTNER_ROLE, conf.SUPERUSER_ROLE):
            raise ValidationError({'organization':
                                       _('Only user with partner role can do it.')})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

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
    organization = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    name = models.CharField(_('first name'), max_length=256)
    start_rotation = models.DateTimeField(_('start of rotation'))
    end_rotation = models.DateTimeField(_('end of rotation'))
    min_scoring_score = models.PositiveIntegerField(_('min scoring score'))
    max_scoring_score = models.PositiveIntegerField(_('max scoring score'))
    type = models.PositiveIntegerField(_('type'), choices=LOAN_TYPES)

    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    @property
    def type_name(self):
        return [_ for _ in self.LOAN_TYPES if _[0] == self.type][0][1]

    def clean(self):
        if self.organization.role not in (conf.ORGANISATION_ROLE, conf.SUPERUSER_ROLE):
            raise ValidationError({'organization':
                                       _('Only user with organization role can do it.')})
        if self.max_scoring_score < self.min_scoring_score:
            raise ValidationError({'max_scoring_score':
                                       _('The maximum scoring score should be more than the minimum scoring score.')})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('loan offer')
        verbose_name_plural = _('loan offers')


class LoanRequest(models.Model):
    """ Кредитная заявка """
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
    sent = models.DateTimeField(_('sending date'))
    created = models.DateTimeField(_('created'), auto_now_add=True)

    @property
    def type_name(self):
        return [_ for _ in self.STATUS_TYPES if _[0] == self.status][0][1]

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('loan request')
        verbose_name_plural = _('loan request')
