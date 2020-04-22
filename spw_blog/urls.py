"""spw_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from users import views as user_views

from django_otp.admin import OTPAdminSite
admin.site.__class__ = OTPAdminSite
admin.site.site_header = 'SPW Administration Page'
admin.site.site_title = 'SPW Admin'

class OTPAdmin(OTPAdminSite):
    pass

from django.contrib.auth.models import User
from django_otp.plugins.otp_totp.models import TOTPDevice
from blog.models import Post
admin_site = OTPAdmin(name='OTPAdmin')
admin_site.register(User)
admin_site.register(TOTPDevice)
admin_site.register(Post)
#admin_site.register(user_views.profile)

urlpatterns = [
    path('spwprojectadminsite/', admin.site.urls),
    path('admin/', admin_site.urls),
    path('register/', user_views.register, name ='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', user_views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-cimpelete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),

    path('', include('blog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
