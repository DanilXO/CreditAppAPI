from django.urls import path
from rest_framework.routers import SimpleRouter

from apps.credit import views

app_name = 'credit'
router = SimpleRouter()
router.register(r'customer-profiles', views.CustomerProfileViewSet, basename='customer-profiles')
router.register(r'loan-offers', views.LoanOfferViewSet, basename='loan-offers')
router.register(r'loan-requests', views.LoanRequestViewSet, basename='loan-requests')

urlpatterns = [
    path('', views.ApiRoot.as_view(), name='api-root'),
]

urlpatterns += router.urls
