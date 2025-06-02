"""
URL configuration for Cert2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [
    path('', views.home, name="home" ),
    path('admin/', admin.site.urls),
    path('base', views.home),
    path('metricas', views.metricas, name='metricas'),
    path('informacion', views.informacion, name='informacion'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('registro/', views.registro, name='registro'),
    path('solicitudes/nueva/', views.nueva_solicitud, name='nueva_solicitud'),
    path('solicitudes/', views.mis_solicitudes, name='mis_solicitudes'),


]
