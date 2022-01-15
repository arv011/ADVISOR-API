"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import urls
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from adviser.views import adviserviewset,registerview, loginapiview,adviserbookingapi, bookingslistapi
from rest_framework import routers, urls
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from django.conf import settings
from django.conf.urls.static import static
# router1 = DefaultRouter()
# router2 = DefaultRouter()

# router1.register('admin/advisors',adviserviewset, basename='adviser')
# router2.register('',adviserviewset, basename='advisor-list')

# router.register('user/register/',registerviewset, basename='adviser')


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',include(router1.urls)),
    path('',include('adviser.urls', namespace='leads')),
    path('auth',include('rest_framework.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    # path('user/register/',registerview.as_view(),name='register'),
    # path('user/login/',loginapiview.as_view(),name='login'),
    # path('user/<int:pk>/advisors',include(router2.urls)),
    # path('user/<int:pk>/advisors/<int:pk2>/',adviserbookingapi.as_view(),name='advisor-book'),
    # path('user/<int:pk>/advisors/booking/',bookingslistapi.as_view(), name = 'bookings-list')
    
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

