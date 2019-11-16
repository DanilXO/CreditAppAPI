from django.urls import path

from apps.users import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='sign-up'),
]
