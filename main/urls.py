from django.urls import path, include
from django.conf import settings
from django.views.static import serve
from .views import *


urlpatterns = [
    path('', index_view, name='home'),
    path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('contacts', contacts_view, name='contacts'),
    path('login', login_view, name='login'),
    path('login/2fa', login_2fa_view, name='login_2fa'),
    path('logout', logout_view, name='logout'),
    path('registration', registration_view, name='registration'),
    path('polygon', polygon_view, name='polygon'),
    path('polygon2', polygon2_view, name='polygon2'),
    path('otp-settings', otp_settings_view, name='otp-settings'),
]