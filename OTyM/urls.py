"""
URL configuration for OTyM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from solicitudes import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('primera_etapa/', views.primera_etapa_view, name='primera_etapa'),
    path('segunda_etapa/', views.segunda_etapa_view, name='segunda_etapa'),
    path('tercera_etapa/', views.tercera_etapa_view, name='tercera_etapa'),
    path('prorroga/', views.prorroga_view, name='prorroga'),
    path('agrimensor/', views.agrimensor_view, name='agrimensor'),
    path('cliente/', views.cliente_view, name='cliente'),
    path('notario/', views.notario_view, name='notario'),
    path('departamento/', views.departamento_view, name='departamento'),
    path('sector/', views.sector_view, name='sector'),
    path('usuario/', views.usuario_view, name='usuario'),
    path('solicitud_autorizacion/', views.solicitud_autorizacion_view, name='solicitud_autorizacion'),
    path('primera_etapa_detallada/', views.primera_etapa_detallada_view, name='primera_etapa_detallada'),
    path('segunda_etapa_detallada/', views.segunda_etapa_detallada_view, name='segunda_etapa_detallada'),
    path('tercera_etapa_detallada/', views.tercera_etapa_detallada_view, name='tercera_etapa_detallada'),
    path('form_segunda_etapa/', views.form_segunda_etapa_view, name='form_segunda_etapa'),
    path('form_tercera_etapa/', views.form_tercera_etapa_view, name='form_tercera_etapa'),
    path('procesar_formulario_solicitudes/', views.procesar_formulario_solicitudes, name='procesar_formulario_solicitudes'),
    path('procesar_formulario_segunda_etapa/', views.procesar_formulario_segunda_etapa, name='procesar_formulario_segunda_etapa'),
    path('procesar_formulario_tercera_etapa/', views.procesar_formulario_tercera_etapa, name='procesar_formulario_tercera_etapa'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)