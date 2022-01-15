from django import urls
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from adviser.views import adviserviewset,registerview, loginapiview,adviserbookingapi, bookingslistapi, ChangePasswordView, \
    firstpage
app_name = "leads"


urlpatterns = [
    path('', firstpage, name='firstpage'),
    path('api/register/',registerview.as_view(),name='register'),
    path('api/user/login/',loginapiview.as_view(),name='login'),
    path('api/password/change/', ChangePasswordView.as_view(), name='change-password'),
]

