"""FaceDetection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from faceapp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns =[
    path('', views.user_login, name='user_login'),
    path('admin/', admin.site.urls),
    #user
    path("user-login/", views.user_login, name="user_login"),
    path("user-signup/", views.user_signup, name="user_signup"),
    path("user-logout", views.user_logout, name="user_logout"),
    path("index", views.index, name="index"),
    path("download-report", views.download_report, name="download_report"),
    path("otp", views.otp, name="otp"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) is attached for media folder