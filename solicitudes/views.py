from django.shortcuts import render, redirect
from django.http import JsonResponse


from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
from docx import Document
import requests
import json

from num2words import num2words

from .reemplazos_docs.procesar_formulario_primera_etapa import procesar_formulario_solicitudes
from .reemplazos_docs.procesar_formulario_segunda_etapa import procesar_formulario_segunda_etapa
from .reemplazos_docs.procesar_formulario_tercera_etapa import procesar_formulario_tercera_etapa

def login_view(request):
    return render(request, 'LOGIN.html')


def primera_etapa_view(request):
    return render(request, 'PRIMERA_ETAPA.html')

def segunda_etapa_view(request):
    return render(request, 'SEGUNDA_ETAPA.html')

def tercera_etapa_view(request):
    return render(request, 'TERCERA_ETAPA.html')

def prorroga_view(request):
    return render(request, 'PRORROGA.html')

def agrimensor_view(request):
    return render(request, 'AGRIMENSOR.html')

def cliente_view(request):
    return render(request, 'CLIENTE.html')

def notario_view(request):
    return render(request, 'NOTARIO.html')

def departamento_view(request):
    return render(request, 'DEPARTAMENTO.html')

def sector_view(request):
    return render(request, 'SECTOR.html')

def usuario_view(request):
    return render(request, 'USUARIO.html')

def solicitud_autorizacion_view(request):
    return render(request, 'SOLICITUD_AUTORIZACIÓN.html')

def primera_etapa_detallada_view(request):
    return render(request, 'PRIMERA_ETAPA_DETALLADA.html')

def segunda_etapa_detallada_view(request):
    return render(request, 'SEGUNDA_ETAPA_DETALLADA.html')

def tercera_etapa_detallada_view(request):
    return render(request, 'TERCERA_ETAPA_DETALLADA.html')

def form_segunda_etapa_view(request):
    return render(request, 'FORM_SEGUNDA_ETAPA.html')

def form_tercera_etapa_view(request):
    return render(request, 'FORM_TERCERA_ETAPA.html')
