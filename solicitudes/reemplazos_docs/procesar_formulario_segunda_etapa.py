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

from .utils import *

API_URL = settings.API_URL

def replace_text_in_docx(doc_template, context):
    doc_template.render(context)


@csrf_exempt
def procesar_formulario_segunda_etapa(request):
    if request.method == 'POST':
        # Recibir los datos del formulario

        data = json.loads(request.body)

        idAvisoColindantes = data.get('IdAvisoColindantes')
        print(idAvisoColindantes)
        api_url = f"{API_URL}/avisocolindantes/{idAvisoColindantes}"
        api_response = requests.get(api_url)
        
        if api_response.status_code == 200:
            
            api_data = api_response.json()
            print(api_data)
            

            # Variables para los datos en la clave "AvisoMensura"
            enlace_aviso_mensura = api_data.get('AvisoMensura', {}).get('Enlace')
            estatus_aviso_mensura = api_data.get('AvisoMensura', {}).get('Estatus')
            fecha_autorizacion_aviso_mensura = api_data.get('AvisoMensura', {}).get('FechaAutorizacion')
            fecha_hora_mensura = api_data.get('AvisoMensura', {}).get('FechaHoraMensura')
            id_aviso_mensura = api_data.get('AvisoMensura', {}).get('IdAvisoMensura')
            id_departamento_oficina_aviso_mensura = api_data.get('AvisoMensura', {}).get('IdDepartamentoOficina')
            id_solicitud_aviso_mensura = api_data.get('AvisoMensura', {}).get('IdSolicitud')
            
            # Variables para los datos en la clave "AvisoPeriodico"
            enlace_aviso_periodico = api_data.get('AvisoPeriodico', {}).get('Enlace')
            estatus_aviso_periodico = api_data.get('AvisoPeriodico', {}).get('Estatus')
            id_aviso_mensura_aviso_periodico = api_data.get('AvisoPeriodico', {}).get('IdAvisoMensura')
            id_aviso_periodico = api_data.get('AvisoPeriodico', {}).get('IdAvisoPeriodico')
            
            # Variables para los datos en la clave "DepartamentoOficina"
            departamento_oficina = api_data.get('DepartamentoOficina', {}).get('DepartamentoOficina')
            encargado_departamento_oficina = api_data.get('DepartamentoOficina', {}).get('Encargado')
            estatus_departamento_oficina = api_data.get('DepartamentoOficina', {}).get('Estatus')
            id_departamento_oficina = api_data.get('DepartamentoOficina', {}).get('IdDepartamentoOficina')
            id_sector_departamento_oficina = api_data.get('DepartamentoOficina', {}).get('IdSector')
            
            # Variables para los datos en la clave "sector" dentro de "DepartamentoOficina"
            estatus_sector_departamento_oficina = api_data.get('DepartamentoOficina', {}).get('sector', {}).get('Estatus')
            id_sector_sector_departamento_oficina = api_data.get('DepartamentoOficina', {}).get('sector', {}).get('IdSector')
            municipio_sector_departamento_oficina = api_data.get('DepartamentoOficina', {}).get('sector', {}).get('Municipio')
            pais_sector_departamento_oficina = api_data.get('DepartamentoOficina', {}).get('sector', {}).get('Pais')
            provincia_sector_departamento_oficina = api_data.get('DepartamentoOficina', {}).get('sector', {}).get('Provincia')
            sector_sector_departamento_oficina = api_data.get('DepartamentoOficina', {}).get('sector', {}).get('Sector')

            # Variables para los datos en la clave "SolicitudAutorizacion"
            actuacion_tecnica = api_data.get('SolicitudAutorizacion', {}).get('ActuacionTecnica')

            # Variables para los datos en la clave "Agrimensor" dentro de "SolicitudAutorizacion"
            nombre_agrimensor = api_data.get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('Nombre')
            apellido_agrimensor = api_data.get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('Apellido')
            codia_agrimensor = api_data.get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('CODIA')
            calle_agrimensor = api_data.get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('Calle')
            cedula_agrimensor = api_data.get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('Cedula')
            celular_agrimensor = api_data.get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('Celular')
            correo_agrimensor = api_data.get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('Correo')
            estado_civil_agrimensor = api_data.get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('EstadoCivil')
            estatus_agrimensor = api_data.get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('Estatus')
            id_agrimensor = api_data.get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('IdAgrimensor')
            id_sector_agrimensor = api_data.get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('IdSector')
            sector_agrimensor = api_data.get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('Sector', {}).get('Sector', {})
            municipio_agrimensor = api_data.get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('Sector', {}).get('Municipio', {})
            pais_agrimensor = api_data.get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('Sector', {}).get('Pais', {})
            provincia_agrimensor = api_data.get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('Sector', {}).get('Provincia', {})
            nacionalidad_agrimensor = api_data.get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('Nacionalidad')
            profesion_agrimensor = api_data.get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('Profesion')
            sexo_agrimensor = api_data.get('SolicitudAutorizacion', {}).get('Agrimensor', {}).get('Sexo')

            # Variables para los datos en la clave "Cliente01" dentro de "SolicitudAutorizacion"
            nombre_cliente01 = api_data.get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('Nombre')
            apellido_cliente01 = api_data.get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('Apellido')
            calle_cliente01 = api_data.get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('Calle')
            cedula_pasaporte_cliente01 = api_data.get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('CedulaPasaporte')
            celular_cliente01 = api_data.get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('Celular')
            correo_cliente01 = api_data.get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('Correo')
            estado_civil_cliente01 = api_data.get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('EstadoCivil')
            estatus_cliente01 = api_data.get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('Estatus')
            id_cliente01 = api_data.get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('IdCliente')
            id_sector_cliente01 = api_data.get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('IdSector')
            provincia_cliente01 = api_data.get('SolicitudAutorizacion', {}).get('SectorCliente01', {}).get('Provincia')
            municipio_cliente01 = api_data.get('SolicitudAutorizacion', {}).get('SectorCliente01', {}).get('Municipio')
            nacionalidad_cliente01 = api_data.get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('Nacionalidad')
            ocupacion_cliente01 = api_data.get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('Ocupacion')
            sexo_cliente01 = api_data.get('SolicitudAutorizacion', {}).get('Cliente01', {}).get('Sexo')


            # Variables para los datos en la clave "Cliente02" dentro de "SolicitudAutorizacion"
            nombre_cliente02 = api_data.get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('Nombre')
            apellido_cliente02 = api_data.get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('Apellido')
            calle_cliente02 = api_data.get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('Calle')
            cedula_pasaporte_cliente02 = api_data.get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('CedulaPasaporte')
            celular_cliente02 = api_data.get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('Celular')
            correo_cliente02 = api_data.get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('Correo')
            estado_civil_cliente02 = api_data.get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('EstadoCivil')
            if(str(estado_civil_cliente02) == "Vacio") : estado_civil_cliente02 = ""
            estatus_cliente02 = api_data.get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('Estatus')
            id_cliente02 = api_data.get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('IdCliente')
            id_sector_cliente02 = api_data.get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('IdSector')
            nacionalidad_cliente02 = api_data.get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('Nacionalidad')
            if(str(nacionalidad_cliente02) == "Vacio") : nacionalidad_cliente02 = ""
            ocupacion_cliente02 = api_data.get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('Ocupacion')
            sexo_cliente02 = api_data.get('SolicitudAutorizacion', {}).get('Cliente02', {}).get('Sexo')


            if(int(id_cliente02) == 1):
                un_cliente = True
            else:
                un_cliente = False

            # Variables para los datos en la clave "DerechoSustentado" dentro de "SolicitudAutorizacion"
            estatus_derecho_sustentado = api_data.get('SolicitudAutorizacion', {}).get('DerechoSustentado', {}).get('Estatus')

            # Variables para los datos en la clave "Notario" dentro de "SolicitudAutorizacion"
            nombre_notario = api_data.get('SolicitudAutorizacion', {}).get('Notario', {}).get('Nombre')
            apellido_notario = api_data.get('SolicitudAutorizacion', {}).get('Notario', {}).get('Apellido')
            estatus_notario = api_data.get('SolicitudAutorizacion', {}).get('Notario', {}).get('Estatus')
            id_notario = api_data.get('SolicitudAutorizacion', {}).get('Notario', {}).get('IdNotario')
            id_sector_notario = api_data.get('SolicitudAutorizacion', {}).get('Notario', {}).get('IdSector')
            nro_colegiatura_notario = api_data.get('SolicitudAutorizacion', {}).get('Notario', {}).get('NroColegiatura')
            sexo_notario = api_data.get('SolicitudAutorizacion', {}).get('Notario', {}).get('Sexo')

            # Variables para los datos en la clave "Sector" dentro de "SolicitudAutorizacion"
            estatus_sector = api_data.get('SolicitudAutorizacion', {}).get('Sector', {}).get('Estatus')
            id_sector_sector = api_data.get('SolicitudAutorizacion', {}).get('Sector', {}).get('IdSector')
            municipio_sector = api_data.get('SolicitudAutorizacion', {}).get('Sector', {}).get('Municipio')
            pais_sector = api_data.get('SolicitudAutorizacion', {}).get('Sector', {}).get('Pais')
            provincia_sector = api_data.get('SolicitudAutorizacion', {}).get('Sector', {}).get('Provincia')
            sector_sector = api_data.get('SolicitudAutorizacion', {}).get('Sector', {}).get('Sector')

            # Variables para los datos en la clave "SolicitudAutorizacion" (otros)
            area_solicitud_autorizacion = api_data.get('SolicitudAutorizacion', {}).get('Area')
            calle_solicitud_autorizacion = api_data.get('SolicitudAutorizacion', {}).get('Calle')
            coord_latitud = api_data.get('SolicitudAutorizacion', {}).get('CoordLatitud')
            coord_longitud = api_data.get('SolicitudAutorizacion', {}).get('CoordLongitud')
            coord_x = api_data.get('SolicitudAutorizacion', {}).get('CoordX')
            coord_y = api_data.get('SolicitudAutorizacion', {}).get('CoordY')
            distrito_catastral = api_data.get('SolicitudAutorizacion', {}).get('DistritoCatrastal')
            enlace_solicitud_autorizacion = api_data.get('SolicitudAutorizacion', {}).get('Enlace')
            estatus_solicitud_autorizacion = api_data.get('SolicitudAutorizacion', {}).get('Estatus')
            fecha_autorizacion_solicitud_autorizacion = api_data.get('SolicitudAutorizacion', {}).get('FechaAutorizacion')
            fecha_contrato_venta = api_data.get('SolicitudAutorizacion', {}).get('FechaContratoVenta')
            id_agrimensor_solicitud_autorizacion = api_data.get('SolicitudAutorizacion', {}).get('IdAgrimensor')
            id_cliente01_solicitud_autorizacion = api_data.get('SolicitudAutorizacion', {}).get('IdCliente01')
            id_cliente02_solicitud_autorizacion = api_data.get('SolicitudAutorizacion', {}).get('IdCliente02')
            id_departamento_oficina_solicitud_autorizacion = api_data.get('SolicitudAutorizacion', {}).get('IdDepartamentoOficina')
            id_derecho_sustentado = api_data.get('SolicitudAutorizacion', {}).get('IdDerechoSustentado')
            id_notario_solicitud_autorizacion = api_data.get('SolicitudAutorizacion', {}).get('IdNotario')
            id_sector_solicitud_autorizacion = api_data.get('SolicitudAutorizacion', {}).get('IdSector')
            id_solicitud_solicitud_autorizacion = api_data.get('SolicitudAutorizacion', {}).get('IdSolicitud')
            nro_expediente = api_data.get('SolicitudAutorizacion', {}).get('NroExpediente')
            parcela = api_data.get('SolicitudAutorizacion', {}).get('Parcela')

            archivo_template_mensura = os.path.join(settings.MEDIA_ROOT, 'documentos_templates', 'plantilla_aviso_mensura.docx')
            archivo_template_periodico = os.path.join(settings.MEDIA_ROOT, 'documentos_templates', 'plantilla_aviso_periodico.docx')
            archivo_template_colindante = os.path.join(settings.MEDIA_ROOT, 'documentos_templates', 'plantilla_aviso_colindantes.docx')

            archivo_template_prorroga = os.path.join(settings.MEDIA_ROOT, 'documentos_templates', 'plantilla_prorroga.docx')

            documento_template_mensura = DocxTemplate(archivo_template_mensura)
            documento_template_periodico = DocxTemplate(archivo_template_periodico)
            documento_template_colindante = DocxTemplate(archivo_template_colindante)

            documento_template_prorroga = DocxTemplate( archivo_template_prorroga)


            dia_fecha_autorizacion = fecha_autorizacion_solicitud_autorizacion.split('-')[2]
            mes_fecha_autorizacion = fecha_autorizacion_solicitud_autorizacion.split('-')[1]
            anio_fecha_autorizacion = fecha_autorizacion_solicitud_autorizacion.split('-')[0]
            
            #2024-08-08T22:03:00
            fecha_mensura = fecha_hora_mensura.split('T')[0]
            anio_mensura = fecha_mensura.split('-')[0]
            mes_mensura = fecha_mensura.split('-')[1]
            dia_mensura = fecha_mensura.split('-')[2]

            hora_mensura = fecha_hora_mensura.split('T')[1]

            p_cliente_01 = Persona(nombre_cliente01,apellido_cliente01,sexo_cliente01,cedula_pasaporte_cliente01)
            p_cliente_02 = Persona('E','A','M','11111')
            p_agrimensor = Persona(nombre_agrimensor,apellido_agrimensor,sexo_agrimensor,cedula_agrimensor)

            c = Conjuncion(p_cliente_01,p_cliente_02,un_cliente)

            meses = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
            
            reemplazos = {
                'ACTUACION_TECNICA': str(actuacion_tecnica.upper() or ""),
                'Actuacion_Tecnica': str(actuacion_tecnica.title() or ""),
                'NUMERO_EXPEDIENTE': str(str(nro_expediente).upper() or ""),
                'dia_mes_texto_anio_hora_convencion_fechahora_mensura': f"el día {dia_mensura} de {meses[int(mes_mensura)-1]} del año {anio_mensura} a las {hora_completa_24_a_12_horas_y_minutos(hora_mensura)}",
                'dia_mes_texto_anio_convencion_fechaautorizacion_mensura': f"{dia_fecha_autorizacion} de {meses[int(mes_fecha_autorizacion)-1]} del {anio_fecha_autorizacion}",

                'Parcela_Solicitud': str(parcela or ""),
                'Distrito_Catastral': str(distrito_catastral.upper() or ""),
                'Calle_Solicitud': str(calle_solicitud_autorizacion or ""),
                'Sector_Solicitud': str(sector_sector.upper() or ""),
                'Municipio_Solicitud': str(municipio_sector or ""),
                'Provincia_Solicitud': str(provincia_sector or ""),
                'AREA_SOLICITUD': str(area_solicitud_autorizacion or ""),
                'DEPARTAMENTO_SOLICITUD': str(departamento_oficina or ""),
                'COORDENADAS_LATITUD': str(coord_latitud or ""),
                'COORDENADAS_LONGITUD': str(coord_longitud or ""),
                'COORDENADAS_X': str(coord_x or ""),
                'COORDENADAS_Y': str(coord_y or ""),
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
                
                'el_la_agrimensor_a': str(p_agrimensor.el_la()) + ' ' + str(p_agrimensor.agrimensor_a()),
                'Agrimensor_a': str(p_agrimensor.agrimensor_a()).title(),
                'AGRIMENSOR_A': str(p_agrimensor.agrimensor_a()).upper(),
                'nacionalidad_Agrimensor': str(nacionalidad_agrimensor or ""),
                'estado_civil_Agrimensor': str(estado_civil_agrimensor or ""),
                'cedula_pasaporte_Agrimensor': str(cedula_agrimensor or ""),
                'estado_civil_cliente_01': str(estado_civil_cliente01 or ""),
                'portador_cedula_o_pasaporte_cliente_01': str(c.portador_cliente_01()) + " " + str(c.del_pasaporte_de_la_cedula_cliente_01()),
                'domiciliado_a_y_residente_cliente_01': str(parcela or ""),
                'ciudad_cliente_01': str(municipio_cliente01 or ""),
                
            }



                # Reemplazar el texto en el documento
            replace_text_in_docx(documento_template_mensura, reemplazos)
            replace_text_in_docx(documento_template_periodico, reemplazos)
            replace_text_in_docx(documento_template_colindante, reemplazos)

            replace_text_in_docx(documento_template_prorroga, reemplazos)

            # Guardar el documento modificado
            archivo_salida_mensura = os.path.join(settings.MEDIA_ROOT, 'documentos', f'aviso_mensura_{nombre_cliente01}.docx')
            archivo_salida_periodico = os.path.join(settings.MEDIA_ROOT, 'documentos', f'aviso_periodico_{nombre_cliente01}.docx')
            archivo_salida_colindante = os.path.join(settings.MEDIA_ROOT, 'documentos', f'aviso_colindante_{nombre_cliente01}.docx')

            archivo_salida_prorroga = os.path.join(settings.MEDIA_ROOT, 'documentos', f'prorroga_{nombre_cliente01}.docx')

            documento_template_mensura.save(archivo_salida_mensura)
            documento_template_periodico.save(archivo_salida_periodico)
            documento_template_colindante.save(archivo_salida_colindante)

            documento_template_prorroga.save(archivo_salida_prorroga)

            url_archivo_salida_MEDIA_mensura = os.path.join(settings.MEDIA_URL, 'documentos', f'aviso_mensura_{nombre_cliente01}.docx')
            url_archivo_salida_MEDIA_periodico = os.path.join(settings.MEDIA_URL, 'documentos', f'aviso_periodico_{nombre_cliente01}.docx')
            url_archivo_salida_MEDIA_colindante = os.path.join(settings.MEDIA_URL, 'documentos', f'aviso_colindante_{nombre_cliente01}.docx')

            url_archivo_salida_MEDIA_prorroga = os.path.join(settings.MEDIA_URL, 'documentos', f'prorroga_{nombre_cliente01}.docx')

            url_archivo_salida_mensura = url_archivo_salida_MEDIA_mensura.replace("\\", "/")
            url_archivo_salida_periodico = url_archivo_salida_MEDIA_periodico.replace("\\", "/")
            url_archivo_salida_colindante = url_archivo_salida_MEDIA_colindante.replace("\\", "/")

            url_archivo_salida_prorroga = url_archivo_salida_MEDIA_prorroga.replace("\\", "/")
            
            url_post_enlace_mensura = f"{API_URL}/avisomensura_enlace/{id_aviso_mensura}"
            url_post_enlace_periodico = f"{API_URL}/avisoperiodico_enlace/{id_aviso_periodico}"
            url_post_enlace_colindante = f"{API_URL}/avisocolindantes_enlace/{idAvisoColindantes}"

            url_post_enlace_prorroga = f"{API_URL}/aviso_colindante_enlace_prorroga/{idAvisoColindantes}"
            
            url_archivo_salida_s_mensura = f"{settings.MEDIA_URL}documentos/aviso_mensura_{urllib.parse.quote(nombre_cliente01)}.docx"
            url_archivo_salida_s_periodico = f"{settings.MEDIA_URL}documentos/aviso_periodico_{urllib.parse.quote(nombre_cliente01)}.docx"
            url_archivo_salida_s_colindante = f"{settings.MEDIA_URL}documentos/aviso_colindante_{urllib.parse.quote(nombre_cliente01)}.docx"

            url_archivo_salida_s_prorroga = f"{settings.MEDIA_URL}documentos/prorroga_{urllib.parse.quote(nombre_cliente01)}.docx"
            
            datos_actualizados_mensura = {
                "Enlace": str(url_archivo_salida_mensura),
            }

            datos_actualizados_periodico = {
                "Enlace": str(url_archivo_salida_periodico),
            }

            datos_actualizados_colindante = {
                "Enlace": str(url_archivo_salida_colindante),
            }

            datos_actualizados_prorroga = {
                "EnlaceProrroga": str(url_archivo_salida_prorroga),
            }
            
            headers = {
                    'Content-Type': 'application/json'
            }

            respuesta_put_enlace_mensura = requests.put(url_post_enlace_mensura , json=datos_actualizados_mensura,headers=headers)
            respuesta_put_enlace_periodico = requests.put(url_post_enlace_periodico, json=datos_actualizados_periodico,headers=headers)
            respuesta_put_enlace_colindante = requests.put(url_post_enlace_colindante, json=datos_actualizados_colindante,headers=headers)

            respuesta_put_enlace_prorroga = requests.put(url_post_enlace_prorroga, json=datos_actualizados_prorroga,headers=headers)
         
            
        return JsonResponse({'success': True, 'message': 'Proceso completado con éxito'})

    return JsonResponse({'success': False, 'error': 'Método no permitido'})

