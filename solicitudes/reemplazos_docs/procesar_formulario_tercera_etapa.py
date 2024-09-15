from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
from docx import Document
import requests
import json
import urllib.parse
from django.http import HttpResponseRedirect

from num2words import num2words
from .Conjuncion_Persona import Conjuncion, Persona
from docxtpl import DocxTemplate

from django.conf import settings
import openpyxl

from openpyxl.drawing.image import Image

API_URL = settings.API_URL

def replace_text_in_docx(doc_template, context):
    doc_template.render(context)


@csrf_exempt
def procesar_formulario_tercera_etapa(request):
    if request.method == 'POST':
        # Recibir los datos del formulario

        data = json.loads(request.body)

        idInformeTecnico = data.get('IdInformeTecnico')
        print(idInformeTecnico)
        api_url = f"{API_URL}/informe_tecnico/{idInformeTecnico}"
        api_response = requests.get(api_url)
        
        if api_response.status_code == 200:
            
            api_data = api_response.json()
            print(api_data)
            
            # Variables para "AreaDiferencia"
            area_diferencia = api_data.get('AreaDiferencia', {}).get('AreaDiferencia')
            estatus_area_diferencia = api_data.get('AreaDiferencia', {}).get('Estatus')
            id_area_diferencia = api_data.get('AreaDiferencia', {}).get('IdAreaDiferencia')

            # Variables para "AreaDiferenciada" y "AreaTotal"
            area_diferenciada = api_data.get('AreaDiferenciada')
            area_total = api_data.get('AreaTotal')

            # Variables para "DeclaracionPosesion"
            # CartaConformidad > AvisoColindantes > AvisoMensura
            enlace_aviso_mensura = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('AvisoMensura', {}).get('Enlace')
            estatus_aviso_mensura = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('AvisoMensura', {}).get('Estatus')
            fecha_autorizacion_aviso_mensura = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('AvisoMensura', {}).get('FechaAutorizacion')
            fecha_hora_mensura = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('AvisoMensura', {}).get('FechaHoraMensura')
            id_aviso_mensura = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('AvisoMensura', {}).get('IdAvisoMensura')
            id_departamento_oficina_mensura = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('AvisoMensura', {}).get('IdDepartamentoOficina')
            id_solicitud_mensura = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('AvisoMensura', {}).get('IdSolicitud')

            # CartaConformidad > AvisoColindantes > AvisoPeriodico
            enlace_aviso_periodico = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('AvisoPeriodico', {}).get('Enlace')
            estatus_aviso_periodico = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('AvisoPeriodico', {}).get('Estatus')
            id_aviso_periodico = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('AvisoPeriodico', {}).get('IdAvisoPeriodico')
            id_aviso_mensura_periodico = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('AvisoPeriodico', {}).get('IdAvisoMensura')

            # CartaConformidad > AvisoColindantes > DepartamentoOficina
            departamento_oficina = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('DepartamentoOficina', {}).get('DepartamentoOficina')
            encargado_departamento = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('DepartamentoOficina', {}).get('Encargado')
            estatus_departamento = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('DepartamentoOficina', {}).get('Estatus')
            id_departamento_oficina = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('DepartamentoOficina', {}).get('IdDepartamentoOficina')
            id_sector_departamento = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('DepartamentoOficina', {}).get('IdSector')

            # CartaConformidad > AvisoColindantes > DepartamentoOficina > Sector
            estatus_sector = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('DepartamentoOficina', {}).get('sector', {}).get('Estatus')
            id_sector = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('DepartamentoOficina', {}).get('sector', {}).get('IdSector')
            municipio_sector = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('DepartamentoOficina', {}).get('sector', {}).get('Municipio')
            pais_sector = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('DepartamentoOficina', {}).get('sector', {}).get('Pais')
            provincia_sector = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('DepartamentoOficina', {}).get('sector', {}).get('Provincia')
            sector_sector = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('DepartamentoOficina', {}).get('sector', {}).get('Sector')

            # Variables para "SolicitudAutorizacion"
            actuacion_tecnica = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('ActuacionTecnica')
            area_solicitud = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Area')
            calle_solicitud = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Calle')
            coord_latitud = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('CoordLatitud')
            coord_longitud = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('CoordLongitud')
            coord_x = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('CoordX')
            coord_y = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('CoordY')
            distrito_catastral = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('DistritoCatrastal')
            enlace_solicitud_autorizacion = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Enlace')
            estatus_solicitud_autorizacion = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Estatus')
            fecha_autorizacion_solicitud = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('FechaAutorizacion')
            fecha_contrato_venta = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('FechaContratoVenta')
            id_agrimensor_solicitud = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('IdAgrimensor')
            id_cliente01_solicitud = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('IdCliente01')
            id_cliente02_solicitud = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('IdCliente02')
            id_departamento_oficina_solicitud = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('IdDepartamentoOficina')
            id_derecho_sustentado_solicitud = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('IdDerechoSustentado')
            id_notario_solicitud = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('IdNotario')
            id_sector_solicitud = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('IdSector')
            id_solicitud_solicitud = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('IdSolicitud')
            nro_expediente = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('NroExpediente')
            parcela = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Parcela')

            # Variables para los datos en la clave "Agrimensor" dentro de "SolicitudAutorizacion"
            nombre_agrimensor = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('Nombre')
            apellido_agrimensor = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('Apellido')
            codia_agrimensor = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('CODIA')
            calle_agrimensor = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('Calle')
            cedula_agrimensor = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('Cedula')
            celular_agrimensor = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('Celular')
            correo_agrimensor = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('Correo')
            estado_civil_agrimensor = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('EstadoCivil')
            estatus_agrimensor = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('Estatus')
            id_agrimensor = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('IdAgrimensor')
            id_sector_agrimensor = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('IdSector')
            nacionalidad_agrimensor = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('Nacionalidad')
            profesion_agrimensor = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('Profesion')
            sexo_agrimensor = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('Sexo')

            # Variables para los datos en la clave "Cliente01" dentro de "SolicitudAutorizacion"
            nombre_cliente01 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('Nombre')
            apellido_cliente01 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('Apellido')
            calle_cliente01 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('Calle')
            cedula_pasaporte_cliente01 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('CedulaPasaporte')
            celular_cliente01 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('Celular')
            correo_cliente01 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('Correo')
            estado_civil_cliente01 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('EstadoCivil')
            estatus_cliente01 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('Estatus')
            id_cliente01 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('IdCliente')
            id_sector_cliente01 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('IdSector')
            nacionalidad_cliente01 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('Nacionalidad')
            ocupacion_cliente01 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('Ocupacion')
            sexo_cliente01 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('Sexo')

            sector_cliente01 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('Sector', {}).get('Sector')
            municipio_cliente01 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('Sector', {}).get('Municipio')
            provincia_cliente01 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('Sector', {}).get('Provincia')
            pais_cliente01 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('Sector', {}).get('Pais')
            
            sector_cliente02 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('Sector', {}).get('Sector')
            municipio_cliente02 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('Sector', {}).get('Municipio')
            provincia_cliente02 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('Sector', {}).get('Provincia')
            pais_cliente02 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('Sector', {}).get('Pais')

            sector_agrimensor = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('Sector', {}).get('Sector')
            municipio_agrimensor = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('Sector', {}).get('Municipio')
            provincia_agrimensor = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('Sector', {}).get('Provincia')
            pais_agrimensor = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('Sector', {}).get('Pais')

            # Variables para los datos en la clave "Cliente02" dentro de "SolicitudAutorizacion"
            nombre_cliente02 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('Nombre')
            apellido_cliente02 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('Apellido')
            calle_cliente02 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('Calle')
            cedula_pasaporte_cliente02 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('CedulaPasaporte')
            celular_cliente02 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('Celular')
            correo_cliente02 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('Correo')
            estado_civil_cliente02 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('EstadoCivil')
            estatus_cliente02 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('Estatus')
            id_cliente02 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('IdCliente')
            id_sector_cliente02 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('IdSector')
            nacionalidad_cliente02 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('Nacionalidad')
            ocupacion_cliente02 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('Ocupacion')
            sexo_cliente02 = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('Sexo')

            # Variables para "Notario" dentro de "SolicitudAutorizacion"
            nombre_notario = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Notario', {}).get('Nombre')
            apellido_notario = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Notario', {}).get('Apellido')
            estatus_notario = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Notario', {}).get('Estatus')
            id_notario = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Notario', {}).get('IdNotario')
            id_sector_notario = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Notario', {}).get('IdSector')
            nro_colegiatura_notario = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Notario', {}).get('NroColegiatura')
            sexo_notario = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Notario', {}).get('Sexo')

            # Variables para "Sector" dentro de "SolicitudAutorizacion"
            estatus_sector_solicitud = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Sector', {}).get('Estatus')
            id_sector_solicitud = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Sector', {}).get('IdSector')
            municipio_sector_solicitud = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Sector', {}).get('Municipio')
            pais_sector_solicitud = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Sector', {}).get('Pais')
            provincia_sector_solicitud = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Sector', {}).get('Provincia')
            sector_solicitud = api_data.get('DeclaracionPosesion', {}).get('CartaConformidad', {}).get('AvisoColindantes', {}).get('SolicitudAutorizacion', {}).get('Sector', {}).get('Sector')

            # Variables adicionales en "DeclaracionPosesion"
            derecho_sustentado = api_data.get('DeclaracionPosesion', {}).get('DerechoSustentado', {}).get('DerechoSustentado')
            estatus_derecho_sustentado = api_data.get('DeclaracionPosesion', {}).get('DerechoSustentado', {}).get('Estatus')
            id_derecho_sustentado = api_data.get('DeclaracionPosesion', {}).get('DerechoSustentado', {}).get('IdDerechoSustentado')
            fecha_documento_derecho_posesion = api_data.get('DeclaracionPosesion', {}).get('FechaDocumentoDerecho')
            id_conformidad_posesion = api_data.get('DeclaracionPosesion', {}).get('IdConformidad')
            id_declaracion_posesion = api_data.get('DeclaracionPosesion', {}).get('IdDeclaracionPosesion')

            # Variables generales
            delimitacion_este = api_data.get('DelimitacionEste')
            delimitacion_norte = api_data.get('DelimitacionNorte')
            delimitacion_oeste = api_data.get('DelimitacionOeste')
            delimitacion_sur = api_data.get('DelimitacionSur')
            enlace_general = api_data.get('Enlace')
            estatus_general = api_data.get('Estatus')
            fecha_documento_derecho = api_data.get('FechaDocumentoDerecho')
            fecha_hora_inicio_mensura = api_data.get('FechaHoraInicioMensura')
            hora_fin_mensura = api_data.get('HoraFinMesura')
            id_area_diferencia_general = api_data.get('IdAreaDiferencia')
            id_informe_tecnico = api_data.get('IdInformeTecnico')


            modelo_equipo = api_data.get('ModeloEquipo')
            nombre_equipo = api_data.get('NombreEquipo')
            ubicacion_inmueble = api_data.get('UbicacionInmueble')
            descripcion_inmueble = api_data.get('DescripcionInmueble')



            if(int(id_cliente02) == 1):
                un_cliente = True
            else:
                un_cliente = False

            

            archivo_template_carta_conformidad = os.path.join(settings.MEDIA_ROOT, 'documentos_templates', 'plantilla_carta_conformidad.docx')
            archivo_template_declaracion_escrita = os.path.join(settings.MEDIA_ROOT, 'documentos_templates', 'plantilla_declaracion_escrita.docx')
            archivo_template_informe_tecnico = os.path.join(settings.MEDIA_ROOT, 'documentos_templates', 'plantilla_informe_tecnico.docx')
            #archivo_template_prorroga = os.path.join(settings.MEDIA_ROOT, 'documentos_templates', 'plantilla_prorroga.docx')
            archivo_template_acta_hitos = os.path.join(settings.MEDIA_ROOT, 'documentos_templates', 'plantilla_acta_de_hitos.xlsx')

            documento_template_carta_conformidad = DocxTemplate(archivo_template_carta_conformidad)
            documento_template_declaracion_escrita = DocxTemplate(archivo_template_declaracion_escrita)
            documento_template_informe_tecnico = DocxTemplate(archivo_template_informe_tecnico)
            #documento_template_prorroga = DocxTemplate( archivo_template_prorroga)
            documento_template_acta_hitos = openpyxl.load_workbook(archivo_template_acta_hitos)
            hoja_doc_acta_hitos = documento_template_acta_hitos['ACTA DE HITOS Y MENSURA']
            
            dia_fecha_autorizacion = fecha_autorizacion_solicitud.split('-')[2]
            mes_fecha_autorizacion = fecha_autorizacion_solicitud.split('-')[1]
            anio_fecha_autorizacion = fecha_autorizacion_solicitud.split('-')[0]
            
            
            #2024-08-08T22:03:00
            fecha_mensura = fecha_hora_mensura.split('T')[0]
            anio_mensura = fecha_mensura.split('-')[0]
            mes_mensura = fecha_mensura.split('-')[1]
            dia_mensura = fecha_mensura.split('-')[2]


            anio_derecho = fecha_documento_derecho_posesion.split('-')[0]
            mes_derecho = fecha_documento_derecho_posesion.split('-')[1]
            dia_derecho = fecha_documento_derecho_posesion.split('-')[2]

            def hora_completa_24_a_12_horas_y_minutos(hora24): #21:00:00 - 9:00 PM
                lista_3_tiempos = hora24.split(':')
                horas = int(lista_3_tiempos[0])
                if(horas > 12):
                    r_horas = horas - 12
                    meridiano = "PM"
                else:
                    r_horas = horas
                    meridiano = "AM"

                return f"{str(r_horas)}:{lista_3_tiempos[1]} {meridiano}"

            hora_mensura = fecha_hora_mensura.split('T')[1]

            p_cliente_01 = Persona(nombre_cliente01,apellido_cliente01,sexo_cliente01,cedula_pasaporte_cliente01)
            p_cliente_02 = Persona('E','A','M','11111')
            p_agrimensor = Persona(nombre_agrimensor,apellido_agrimensor,sexo_agrimensor,cedula_agrimensor)

            c = Conjuncion(p_cliente_01,p_cliente_02,un_cliente)

            meses = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
            print()
            print("LLEGANDO ACÁ")
            print()
            reemplazos = {  
                'ACTUACION_TECNICA': str(actuacion_tecnica.upper() or ""),
                'Actuacion_Tecnica': str(actuacion_tecnica.title() or ""),
                'NUMERO_EXPEDIENTE': str(str(nro_expediente).upper() or ""),
                'dia_mes_texto_anio_hora_convencion_fechahora_mensura': f"el día {dia_mensura} de {meses[int(mes_mensura)-1]} del año {anio_mensura} a las {hora_completa_24_a_12_horas_y_minutos(hora_mensura)}",
                'dia_mes_texto_anio_convencion_fechaautorizacion_mensura': f"{dia_fecha_autorizacion} de {meses[int(mes_fecha_autorizacion)-1]} del {anio_fecha_autorizacion}",
                
                'dia_mes_texto_anio_derecho_sustentado': f"{dia_fecha_autorizacion} de {meses[int(mes_fecha_autorizacion)-1]} del {anio_fecha_autorizacion}",
                'nacionalidad_cliente_01': str(nacionalidad_cliente01 or ""),
                'estado_civil_cliente_01': str(estado_civil_cliente01 or ""),
                'ocupacion_cliente_01': str(ocupacion_cliente01 or ""),

                'domiciliado_a_y_residente_cliente_01': str(parcela or ""),
                'ciudad_cliente_01': str(municipio_cliente01 or ""),
                'provincia_cliente_01': str(provincia_cliente01 or ""),
                'nacionalidad_Agrimensor': str(nacionalidad_agrimensor or ""),
                'estado_civil_Agrimensor': str(estado_civil_agrimensor or ""),
                'cedula_pasaporte_Agrimensor': str(cedula_agrimensor or ""),
                'DERECHO_SUSTENTADO': str(derecho_sustentado or ""),
             
                'AREA_DIFERENCIA_FINAL': str(float(area_total) + float(area_diferenciada) or ""),
                'AREA_TOTAL': str(area_total or ""),
                'AREA_DIFERENCIA': str(area_diferenciada or ""),
                'exceso_defecto': str(area_diferencia or ""),
                'dia_mes_texto_anio_hora_fecha_documento_derecho' : f"el día {dia_derecho} de {meses[int(mes_derecho)-1]} del año {anio_derecho}", 
                'hora_fin_mensura' : str(hora_completa_24_a_12_horas_y_minutos(hora_fin_mensura) or ""),


                'Parcela_Solicitud': str(parcela or ""),
                'Distrito_Catastral': str(distrito_catastral.upper() or ""),
                'Calle_Solicitud': str(calle_solicitud or ""),
                'Sector_Solicitud': str(sector_solicitud.upper() or ""),
                'Municipio_Solicitud': str(municipio_sector_solicitud or ""),
                'Provincia_Solicitud': str(provincia_sector_solicitud or ""),
                'AREA_SOLICITUD': str(area_solicitud or ""),
                'DEPARTAMENTO_SOLICITUD': str(departamento_oficina or ""),
                'COORDENADAS_LATITUD': str(coord_latitud or ""),
                'COORDENADAS_LONGITUD': str(coord_longitud or ""),
                'COORDENADAS_X': str(coord_x or ""),
                'COORDENADAS_Y': str(coord_y or ""),

            
                'DELIMITACION_SUR': str(delimitacion_sur or ""),
                'DELIMITACION_NORTE': str(delimitacion_norte or ""),
                'DELIMITACION_ESTE': str(delimitacion_este or ""),
                'DELIMITACION_OESTE': str(delimitacion_oeste or ""),

                'NOMBRE_COMPLETO_AGRIMENSOR': str(nombre_agrimensor.upper() or "") + " " + str(apellido_agrimensor.upper() or ""),
                'NUMERO_CODIA_AGRIMENSOR': str(codia_agrimensor or ""),
                'CELULAR_AGRIMENSOR': str(celular_agrimensor or ""),
                'correo_agrimensor': str(correo_agrimensor or ""),
                'calle_Agrimensor': str(calle_agrimensor or ""),
                'Sector_Agrimensor': str(sector_agrimensor or ""),
                'Ciudad_Agrimensor': str(municipio_agrimensor or ""),
                'Provincia_Agrimensor': str(provincia_agrimensor or ""),

                
                


                'Provincia_cliente_01': str(provincia_cliente01 or ""),
                'el_SR_la_SRA_NOMBRE_COMPLETO_CLIENTE_01': str(c.el_SR_la_SRA_CLIENTE_01()),
                'SR_SRA_NOMBRE_COMPLETO_CLIENTE_01': str(c.SR_SRA_CLIENTE_01()),


                'portador_cedula_o_pasaporte_cliente_01': str(c.portador_cliente_01()) + " " + str(c.del_pasaporte_de_la_cedula_cliente_01()),
                'Propietario_cliente_01': str(p_cliente_01.Propietario_a()),

                'el_la_agrimensor_a': str(p_agrimensor.el_la()) + ' ' + str(p_agrimensor.agrimensor_a()),
                'Agrimensor_a': str(p_agrimensor.agrimensor_a()).title(),
                'AGRIMENSOR_A': str(p_agrimensor.agrimensor_a()).upper(),

                'Modelo_Equipo': str(modelo_equipo),
                'Nombre_Equipo': str(nombre_equipo),
                'Ubicacion_Inmueble': str(ubicacion_inmueble),
                'Descripcion_Inmueble': str(descripcion_inmueble)
            }




            print(archivo_template_carta_conformidad)
            print()
                # Reemplazar el texto en el documento
            replace_text_in_docx(documento_template_carta_conformidad, reemplazos)

            replace_text_in_docx(documento_template_declaracion_escrita, reemplazos)

            replace_text_in_docx(documento_template_informe_tecnico, reemplazos)

            #replace_text_in_docx(documento_template_prorroga, reemplazos)


            var = " " * 154

            variables = {
                'D7': reemplazos['ACTUACION_TECNICA'],  #ACTUACION_TECNICA
                'D8': reemplazos['NOMBRE_COMPLETO_AGRIMENSOR'], #NOMBRE_COMPLETO_AGRIMENSOR
                'P7': "---", #Fecha
                'P8': reemplazos['NUMERO_CODIA_AGRIMENSOR'], #CODIA
                'D11': reemplazos['Provincia_Solicitud'], #PROVINCIA
                'L11': reemplazos['Municipio_Solicitud'], #MUNICIPIO
                'L12': reemplazos['Sector_Solicitud'], #SECTOR
                'D13': reemplazos['Parcela_Solicitud'], #PARCELA
                'C15': reemplazos['Distrito_Catastral'], #DISTRITO CATASTRAL
                'G15': reemplazos['Calle_Solicitud'], #CALLE
                'K26': reemplazos['DELIMITACION_NORTE'], #DESCRIPCION NORTE
                'K27': reemplazos['DELIMITACION_ESTE'], #DESCRIPCION ESTE
                'K28': reemplazos['DELIMITACION_SUR'], #DESCRIPCION SUR
                'K29': reemplazos['DELIMITACION_OESTE'], #DESCRIPCION OESTE
                'D39': reemplazos['NUMERO_EXPEDIENTE'] + "_1_1", #EXPEDIENTE_1_1
                'P39': reemplazos['Distrito_Catastral'], #DISTRITO CATASTRAL

                'C45': str(dia_mensura), #DIA FECHA INICIO
                'D45': str(meses[int(mes_mensura)-1]).upper(), #MES TEXTO FECHA INICIO
                'F45': str(anio_mensura), #AÑO FECHA INICIO
                'C46': str(hora_completa_24_a_12_horas_y_minutos(hora_mensura)), #HORAFECHA INICIO

                'J45': str(dia_mensura), #DIA FECHA FIN
                'K45': str(meses[int(mes_mensura)-1]).upper(), #MES TEXTO FECHA FIN
                'N45': str(anio_mensura), #AÑO FECHA FIN
                'J46': reemplazos['hora_fin_mensura'], #HORA FECHA FIN
                
                'C62': reemplazos['Nombre_Equipo'], #NOMBRE MARCA
                'K62': reemplazos['Modelo_Equipo'], #MODELO MARCA

                'D65': reemplazos['AREA_DIFERENCIA'], #AREA PRESENTADA
                'M65': reemplazos['AREA_SOLICITUD'], #AREA DE DERECHO

                'N79': reemplazos['NUMERO_EXPEDIENTE'], #EXPEDIENTE
                'N3': reemplazos['NUMERO_EXPEDIENTE'], #EXPEDIENTE

                'I135': "---", #DIA FIRMADO
                'M135': "---", #MES TEXTO FIRMADO
                'P135': "---", #AÑO TEXTO FIRMADO

                'D17': reemplazos['Ubicacion_Inmueble'], 
                
                #'B142': reemplazos['NOMBRE_COMPLETO_AGRIMENSOR'] + var + reemplazos['Agrimensor_a'] + " Contratista CODIA No." + reemplazos['NUMERO_CODIA_AGRIMENSOR'], #DANIEL OMAR MARTINEZ SOLER - Agrimensor Contratista CODIA No. 34525
            }

            # Reemplazar valores en las celdas indicadas
            for celda, valor in variables.items():
                hoja_doc_acta_hitos[celda] = valor
 
            def cm_a_px_excel(ancho_cm = 0, alto_cm = 0):
                cm_to_px = 37.7952755906
                ancho_px = ancho_cm * cm_to_px
                alto_px = alto_cm * cm_to_px
                if(ancho_px == 0): return alto_px
                elif (alto_px == 0): return ancho_px
                else: return [ancho_px,alto_px]



            url_firma_agrimensor_omar = os.path.join(settings.STATICFILES_DIRS[0], 'img_checks_acta','firma_agr_daniel.png')
            #img_firma = Image(url_firma_agrimensor_omar)

            url_check_limites_concreto = os.path.join(settings.STATICFILES_DIRS[0], 'img_checks_acta','concreto_limites.png')
            url_check_limites_alambrada = os.path.join(settings.STATICFILES_DIRS[0], 'img_checks_acta','alambrada_limites.png')
            url_check_limites_verja = os.path.join(settings.STATICFILES_DIRS[0], 'img_checks_acta','verja_limites.png')
            url_check_limites_otro = os.path.join(settings.STATICFILES_DIRS[0], 'img_checks_acta','otro_limites.png')

            url_fondo_acta = os.path.join(settings.STATICFILES_DIRS[0], 'img_checks_acta','fondo_acta.png')
            url_fondo_acta_2 = os.path.join(settings.STATICFILES_DIRS[0], 'img_checks_acta','fondo_acta_2.png')

            url_check_yermo = os.path.join(settings.STATICFILES_DIRS[0], 'img_checks_acta','yermo_checks.png')
            url_check_metodo = os.path.join(settings.STATICFILES_DIRS[0], 'img_checks_acta','metodo_ori_checks.png')
            url_check_metodo_leva = os.path.join(settings.STATICFILES_DIRS[0], 'img_checks_acta','metodo_checks.png')

            check_concreto = Image(url_check_limites_concreto)
            check_alambrada = Image(url_check_limites_alambrada)
            check_verja = Image(url_check_limites_verja)
            check_otro = Image(url_check_limites_otro)
            check_fondo_acta = Image(url_fondo_acta)
            check_fondo_acta_2 = Image(url_fondo_acta_2)

            check_yermo = Image(url_check_yermo)
            check_metodo_orientacion = Image(url_check_metodo)
            check_metodo_levantamiento = Image(url_check_metodo_leva)
            
            check_concreto.width = check_alambrada.width  = check_verja.width  = check_otro.width  = cm_a_px_excel(ancho_cm = 9.3)
            check_concreto.height = check_alambrada.height  = check_verja.height  = check_otro.height  = cm_a_px_excel(alto_cm = 0.45)

            check_fondo_acta.height = cm_a_px_excel(alto_cm = 34.74)
            check_fondo_acta.width = cm_a_px_excel(ancho_cm = 5.34)

            check_fondo_acta_2.height = cm_a_px_excel(alto_cm = 34.74)
            check_fondo_acta_2.width = cm_a_px_excel(ancho_cm = 5.34)

            check_yermo.height = cm_a_px_excel(alto_cm = 1.08)
            check_yermo.width = cm_a_px_excel(ancho_cm = 12.47)

            check_metodo_orientacion.height = cm_a_px_excel(alto_cm = 1.38)
            check_metodo_orientacion.width = cm_a_px_excel(ancho_cm = 19.15)

            check_metodo_levantamiento.height = cm_a_px_excel(alto_cm = 1.32)
            check_metodo_levantamiento.width = cm_a_px_excel(ancho_cm = 8.72)

            if os.path.exists(url_firma_agrimensor_omar):
                img_firma = Image(url_firma_agrimensor_omar)
            else:
                print("La imagen no existe en la ruta especificada:", url_firma_agrimensor_omar)

            #img_firma.width = cm_a_px_excel(ancho_cm = 4.59)
            #img_firma.height = cm_a_px_excel(alto_cm = 2.11)

            #hoja_doc_acta_hitos.add_image(img_firma, "H138")

            hoja_doc_acta_hitos.add_image(check_concreto, "C26")
            hoja_doc_acta_hitos.add_image(check_alambrada, "C27")
            hoja_doc_acta_hitos.add_image(check_verja, "C28")
            hoja_doc_acta_hitos.add_image(check_otro, "C29")
            
            hoja_doc_acta_hitos.add_image(check_fondo_acta, "A3")
            hoja_doc_acta_hitos.add_image(check_fondo_acta_2, "A83")

            hoja_doc_acta_hitos.add_image(check_yermo, "C31")
            hoja_doc_acta_hitos.add_image(check_metodo_levantamiento, "E58")
            hoja_doc_acta_hitos.add_image(check_metodo_orientacion, "B82")
            

            
            # Guardar el documento modificado
            archivo_salida_carta_conformidad = os.path.join(settings.MEDIA_ROOT, 'documentos', f'aviso_carta_conformidad_{nombre_cliente01}.docx')
            archivo_salida_declaracion_escrita = os.path.join(settings.MEDIA_ROOT, 'documentos', f'aviso_declaracion_escrita_{nombre_cliente01}.docx')
            archivo_salida_informe_tecnico = os.path.join(settings.MEDIA_ROOT, 'documentos', f'aviso_informe_tecnico_{nombre_cliente01}.docx')
            #archivo_salida_prorroga = os.path.join(settings.MEDIA_ROOT, 'documentos', f'prorroga_{nombre_cliente01}.docx')
            archivo_salida_acta_hitos = os.path.join(settings.MEDIA_ROOT, 'documentos', f'acta_hitos_{nombre_cliente01}.xlsx')
            
            documento_template_carta_conformidad.save(archivo_salida_carta_conformidad)
            documento_template_declaracion_escrita.save(archivo_salida_declaracion_escrita)
            documento_template_informe_tecnico.save(archivo_salida_informe_tecnico)
            #documento_template_prorroga.save(archivo_salida_prorroga)
            documento_template_acta_hitos.save(archivo_salida_acta_hitos)

            url_archivo_salida_MEDIA_carta_conformidad = os.path.join(settings.MEDIA_URL, 'documentos', f'aviso_carta_conformidad_{nombre_cliente01}.docx')
            url_archivo_salida_MEDIA_declaracion_escrita = os.path.join(settings.MEDIA_URL, 'documentos', f'aviso_declaracion_escrita_{nombre_cliente01}.docx')
            url_archivo_salida_MEDIA_informe_tecnico = os.path.join(settings.MEDIA_URL, 'documentos', f'aviso_informe_tecnico_{nombre_cliente01}.docx')
            #url_archivo_salida_MEDIA_prorroga = os.path.join(settings.MEDIA_URL, 'documentos', f'prorroga_{nombre_cliente01}.docx')
            url_archivo_salida_MEDIA_acta_hitos = os.path.join(settings.MEDIA_URL, 'documentos', f'acta_hitos_{nombre_cliente01}.xlsx')
            
            url_archivo_salida_carta_conformidad = url_archivo_salida_MEDIA_carta_conformidad.replace("\\", "/")
            url_archivo_salida_declaracion_escrita = url_archivo_salida_MEDIA_declaracion_escrita.replace("\\", "/")
            url_archivo_salida_informe_tecnico = url_archivo_salida_MEDIA_informe_tecnico.replace("\\", "/")
            #url_archivo_salida_prorroga = url_archivo_salida_MEDIA_prorroga.replace("\\", "/")
            url_archivo_salida_acta_hitos = url_archivo_salida_MEDIA_acta_hitos.replace("\\", "/")
            
            url_post_enlace_carta_conformidad = f"{API_URL}/conformidad_enlace/{id_conformidad_posesion}"
            url_post_enlace_declaracion_escrita = f"{API_URL}/declaracion_posesion_enlace/{id_declaracion_posesion}"
            url_post_enlace_informe_tecnico = f"{API_URL}/informe_tecnico_enlace/{id_informe_tecnico}"
            #url_post_enlace_prorroga = f"{API_URL}/informe_tecnico_enlace_prorroga/{id_informe_tecnico}"
            url_post_enlace_acta_hitos = f"{API_URL}/informe_tecnico_enlace_acta/{id_informe_tecnico}"

            print()
            print("LLEGANDO ACÁ TAMBIEN 4")
            print()
            url_archivo_salida_s_carta_conformidad = f"{settings.MEDIA_URL}documentos/aviso_carta_conformidad_{urllib.parse.quote(nombre_cliente01)}.docx"
            url_archivo_salida_s_declaracion_escrita = f"{settings.MEDIA_URL}documentos/aviso_periodico_{urllib.parse.quote(nombre_cliente01)}.docx"
            url_archivo_salida_s_informe_tecnico = f"{settings.MEDIA_URL}documentos/aviso_informe_tecnico_{urllib.parse.quote(nombre_cliente01)}.docx"
            #url_archivo_salida_s_prorroga = f"{settings.MEDIA_URL}documentos/prorroga_{urllib.parse.quote(nombre_cliente01)}.docx"
            url_archivo_salida_s_acta_hitos = f"{settings.MEDIA_URL}documentos/acta_hitos_{urllib.parse.quote(nombre_cliente01)}.xlsx"
            
            datos_actualizados_carta_conformidad = {
                "Enlace": str(url_archivo_salida_carta_conformidad),
            }

            datos_actualizados_declaracion_escrita = {
                "Enlace": str(url_archivo_salida_declaracion_escrita),
            }

            datos_actualizados_informe_tecnico = {
                "Enlace": str(url_archivo_salida_informe_tecnico),
            }

            #datos_actualizados_prorroga = {
            #    "Enlace_Prorroga": str(url_archivo_salida_prorroga),
            #}

            datos_actualizados_acta_hitos = {
                "EnlaceActaHitos": str(url_archivo_salida_acta_hitos),
            }

            print()
            print(f"Informe Tecnico: {str(url_archivo_salida_informe_tecnico)}")
            print()

            #url_archivo_salida = urllib.parse.quote(url_archivo_salida)
            #print(f"URL: {url_archivo_salida} ")

            headers = {
                    'Content-Type': 'application/json'
            }

            respuesta_put_enlace_carta_conformidad = requests.put(url_post_enlace_carta_conformidad , json=datos_actualizados_carta_conformidad,headers=headers)
            respuesta_put_enlace_declaracion_escrita = requests.put(url_post_enlace_declaracion_escrita, json=datos_actualizados_declaracion_escrita,headers=headers)
            respuesta_put_enlace_informe_tecnico = requests.put(url_post_enlace_informe_tecnico, json=datos_actualizados_informe_tecnico,headers=headers)
            #respuesta_put_enlace_prorroga = requests.put(url_post_enlace_prorroga, json=datos_actualizados_prorroga,headers=headers)
            respuesta_put_enlace_acta_hitos = requests.put(url_post_enlace_acta_hitos, json=datos_actualizados_acta_hitos,headers=headers)



            #if respuesta_put_enlace.status_code == 200:
            #    print("Recurso actualizado exitosamente.")
            #else:
            #    print(f"Error al actualizar el recurso: {respuesta_put_enlace.status_code}")
            
            
        return JsonResponse({'success': True, 'message': 'Proceso completado con éxito'})

    return JsonResponse({'success': False, 'error': 'Método no permitido'})
