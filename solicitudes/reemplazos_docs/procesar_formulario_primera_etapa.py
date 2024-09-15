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

API_URL = settings.API_URL

def replace_text_in_docx(doc_template, context):
    doc_template.render(context)


@csrf_exempt
def procesar_formulario_solicitudes(request):
    if request.method == 'POST':
        # Recibir los datos del formulario

        data = json.loads(request.body)

        idSolicitud = data.get('IdSolicitud')
        print(idSolicitud)
        api_url = f"{API_URL}/solicitud/{idSolicitud}"
        api_response = requests.get(api_url)

        if api_response.status_code == 200:
            api_data = api_response.json()

            actuacionTecnica = api_data.get('ActuacionTecnica')
            area = api_data.get('Area')
            calle = api_data.get('Calle')
            coordLatitud = api_data.get('CoordLatitud')
            coordLongitud = api_data.get('CoordLongitud')
            coord_x = api_data.get('CoordX')
            coord_y = api_data.get('CoordY')
            distritoCatastral = api_data.get('DistritoCatrastal')
            fechaAutorizacion = api_data.get('FechaAutorizacion')
            fechaContratoVenta = api_data.get('FechaContratoVenta')
            numeroExpediente = api_data.get('NroExpediente')
            parcela = api_data.get('Parcela')
            derechoSustentado = api_data.get('DerechoSustentado', {}).get('DerechoSustentado')


            nombre_agrimensor = str(api_data.get('Agrimensor', {}).get('Nombre'))
            apellido_agrimensor = str(api_data.get('Agrimensor', {}).get('Apellido'))
            nacionalidad_agrimensor = api_data.get('Agrimensor', {}).get('Nacionalidad')
            sexoLetraAgrimensor = api_data.get('Agrimensor', {}).get('Sexo')
            estadoCivil_agrimensor = api_data.get('Agrimensor', {}).get('EstadoCivil')
            numeroCodia_agrimensor = api_data.get('Agrimensor', {}).get('CODIA')
            cedulaPasaporte_agrimensor = api_data.get('Agrimensor', {}).get('Cedula')
            celular_agrimensor = api_data.get('Agrimensor', {}).get('Celular')
            calle_agrimensor = api_data.get('Agrimensor', {}).get('Calle')
            sector_agrimensor = api_data.get('Agrimensor', {}).get('Sector', {}).get('Sector')
            ciudad_agrimensor = api_data.get('Agrimensor', {}).get('Sector', {}).get('Municipio')
            provincia_agrimensor = api_data.get('Agrimensor', {}).get('Sector', {}).get('Provincia')


            nombre_cliente01 = str(api_data.get('Cliente01', {}).get('Nombre'))
            apellido_cliente01 = str(api_data.get('Cliente01', {}).get('Apellido'))
            nacionalidad_cliente01 = str(api_data.get('Cliente01', {}).get('Nacionalidad'))
            sexoLetraCliente01 = api_data.get('Cliente01', {}).get('Sexo')
            estadoCivil_cliente01 = str(api_data.get('Cliente01', {}).get('EstadoCivil'))
            cedulaPasaporte_cliente01 = str(api_data.get('Cliente01', {}).get('CedulaPasaporte'))
            celular_cliente01 = api_data.get('Cliente01', {}).get('Celular')
            calle_cliente01 = api_data.get('Cliente01', {}).get('Calle')
            sector_cliente01 = api_data.get('Cliente01', {}).get('Sector', {}).get('Sector')
            ciudad_cliente01 = api_data.get('Cliente01', {}).get('Sector', {}).get('Municipio')
            provincia_cliente01 = api_data.get('Cliente01', {}).get('Sector', {}).get('Provincia')
            ocupacion_cliente01 = api_data.get('Cliente01', {}).get('Ocupacion')

            id_cliente02 = api_data.get('Cliente02', {}).get('IdCliente')
            estadoCivil_cliente02 = str(api_data.get('Cliente02', {}).get('EstadoCivil'))


            if(int(id_cliente02) == 1):
                un_cliente = True

                nombre_cliente02 = ""
                apellido_cliente02 = ""
                nacionalidad_cliente02 = ""
                sexoLetraCliente02 = ""
                estadoCivil_cliente02 = ""
                cedulaPasaporte_cliente02 = ""
                celular_cliente02 = ""
                calle_cliente02 = ""
                sector_cliente02 = ""
                ciudad_cliente02 = ""
                provincia_cliente02 = ""
                ocupacion_cliente02 = ""
                mayor_de_edad_cliente02 = ""
                cedula_pasaporte_cliente_02 = ""
            else:
                un_cliente = False
                nombre_cliente02 = str(api_data.get('Cliente02', {}).get('Nombre'))
                apellido_cliente02 = str(api_data.get('Cliente02', {}).get('Apellido'))
                nacionalidad_cliente02 = api_data.get('Cliente02', {}).get('Nacionalidad')
                if(str(nacionalidad_cliente02) == "Vacio") : nacionalidad_cliente02 = ""
                sexoLetraCliente02 = api_data.get('Cliente02', {}).get('Sexo')
                estadoCivil_cliente02 = str(api_data.get('Cliente02', {}).get('EstadoCivil')) + ","
                if(str(estadoCivil_cliente02) == "Vacio") : estadoCivil_cliente02 = ""
                cedulaPasaporte_cliente02 = api_data.get('Cliente02', {}).get('CedulaPasaporte')
                celular_cliente02 = api_data.get('Cliente02', {}).get('Celular')
                calle_cliente02 = api_data.get('Cliente02', {}).get('Calle')
                sector_cliente02 = api_data.get('Cliente02', {}).get('Sector', {}).get('Sector')
                ciudad_cliente02 = api_data.get('Cliente02', {}).get('Sector', {}).get('Municipio')
                provincia_cliente02 = api_data.get('Cliente02', {}).get('Sector', {}).get('Provincia')
                ocupacion_cliente02 = api_data.get('Cliente02', {}).get('Ocupacion')
                mayor_de_edad_cliente02 = ", mayor de edad,"
                cedula_pasaporte_cliente_02 = "No." + cedulaPasaporte_cliente02



            nombre_notario = str(api_data.get('Notario', {}).get('Nombre'))
            apellido_notario = str(api_data.get('Notario', {}).get('Apellido'))
            sexoLetraNotario = api_data.get('Notario', {}).get('Sexo')
            nroColegiatura_notario = api_data.get('Notario', {}).get('NroColegiatura')
            sector_notario = api_data.get('Notario', {}).get('Sector', {}).get('Sector')
            ciudad_notario = api_data.get('Notario', {}).get('Sector', {}).get('Municipio')
            provincia_notario = api_data.get('Notario', {}).get('Sector', {}).get('Provincia')


            sector_nombre = api_data.get('Sector', {}).get('Sector')
            sector_ciudad = api_data.get('Sector', {}).get('Municipio')
            sector_provincia = api_data.get('Sector', {}).get('Provincia')
            sector_pais = api_data.get('Sector', {}).get('Pais')


            departamento_nombre = api_data.get('DepartamentoOficina', {}).get('DepartamentoOficina')
            encargado_departamento = api_data.get('DepartamentoOficina', {}).get('Encargado')
            sector_departamento = api_data.get('DepartamentoOficina', {}).get('sector', {}).get('Sector')
            ciudad_departamento = api_data.get('DepartamentoOficina', {}).get('sector', {}).get('Municipio')
            provincia_departamento = api_data.get('DepartamentoOficina', {}).get('sector', {}).get('Provincia')


            archivo_template = os.path.join(settings.MEDIA_ROOT, 'documentos_templates', 'solicitud_deslinde_plantilla_s_d.docx')
            documento_template = DocxTemplate(archivo_template)


            dia_fecha_autorizacion = fechaAutorizacion.split('-')[2]
            mes_fecha_autorizacion = fechaAutorizacion.split('-')[1]
            anio_fecha_autorizacion = fechaAutorizacion.split('-')[0]

            dia_fecha_contrato_venta = fechaContratoVenta.split('-')[2]
            mes_fecha_contrato_venta = fechaContratoVenta.split('-')[1]
            anio_fecha_contrato_venta = fechaContratoVenta.split('-')[0]

            meses = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]

            p_cliente_01 = Persona(nombre_cliente01,apellido_cliente01,sexoLetraCliente01,cedulaPasaporte_cliente01)
            p_cliente_02 = Persona(nombre_cliente02,apellido_cliente02,sexoLetraCliente02,cedulaPasaporte_cliente02)
            p_agrimensor = Persona(nombre_agrimensor,apellido_agrimensor,sexoLetraAgrimensor,cedulaPasaporte_agrimensor)
            p_notario = Persona(nombre_notario,apellido_notario,sexoLetraNotario,"")

            c = Conjuncion(p_cliente_01,p_cliente_02,un_cliente)


            if(int(id_cliente02) == 1):
                SR_SRA_NOMBRE_COMPLETO_CLIENTE_02 = " "
            else:
                SR_SRA_NOMBRE_COMPLETO_CLIENTE_02 = str(c.SR_SRA_CLIENTE_02()) + " "


            verbo_actuacion_tecnica = {
                'DESLINDE': 'DESLINDAR',
                'REGULARIZACIÓN PARCELARIA': 'REGULARIZAR',
                'SUBDIVISIÓN': 'SUBDIVIDIR',
                'ACTUALIZACIÓN DE MENSURA': 'ACTUALIZAR',
                'SANEAMIENTO': 'SANEAR',
                'NUEVA MENSURA': 'MENSURAR',
                'REFUNDICIÓN': 'REFUNDIR',
                'SUBDIVISIÓN PARA PARTICIÓN': 'SUBDIVIDIR',
            }


            reemplazos = {
                'ACTUACION_TECNICA': str(actuacionTecnica.upper() or ""),
                'Actuacion_Tecnica': str(actuacionTecnica.title() or ""),
                'VERBO_ACTUACION_TECNICA': verbo_actuacion_tecnica[actuacionTecnica.upper()],
                'derecho_sustentado': str(derechoSustentado or ""),
                
                #'NOMBRE_COMPLETO_CLIENTE_01': str(nombreApellido_cliente01.upper() or ""),
                'nacionalidad_cliente_01': str(nacionalidad_cliente01.lower() or ""),
                'estado_civil_cliente_01': str(estadoCivil_cliente01.lower() or ""),
                'cedula_o_pasaporte_cliente_01': str(cedulaPasaporte_cliente01 or ""),
                
                #'NOMBRE_COMPLETO_CLIENTE_02': str(nombreApellido_cliente02.upper() or ""),
                'nacionalidad_cliente_02_mayor_edad': str(nacionalidad_cliente02.lower() or "") + mayor_de_edad_cliente02,
                'estado_civil_cliente_02_coma': " " + str(estadoCivil_cliente02.lower() or "").lower(),
                'cedula_o_pasaporte_cliente_02': str(cedulaPasaporte_cliente02 or ""),
                'Municipio_cliente_01': str(ciudad_cliente01 or ""),
                'Provincia_cliente_01': str(provincia_cliente01 or ""),
                
                'DEPARTAMENTO_SOLICITUD': str(departamento_nombre.upper() or ""),
                
                'NOMBRE_COMPLETO_AGRIMENSOR': str(nombre_agrimensor.upper() or "") + " " + str(apellido_agrimensor.upper() or ""),
                'nacionalidad_agrimensor': str(nacionalidad_agrimensor or "").lower(),
                'estado_civil_agrimensor': str(estadoCivil_agrimensor or "").lower(),
                'NUMERO_CODIA_AGRIMENSOR': str(numeroCodia_agrimensor or ""),
                'cedula_o_pasaporte_agrimensor': str(cedulaPasaporte_agrimensor or ""),
                'CELULAR_AGRIMENSOR': str(celular_agrimensor or ""),
                'Calle_Agrimensor': str(calle_agrimensor or ""), 
                'Sector_Agrimensor': str(sector_agrimensor or ""),
                'Ciudad_Agrimensor': str(ciudad_agrimensor or ""),
                'Provincia_Agrimensor': str(provincia_agrimensor or ""),
                
                'AREA_SOLICITUD': str(area or ""),
                'PARCELA_SOLICITUD': str(parcela or ""),
                'DISTRITO_CATASTRAL': str(distritoCatastral or ""),
                'fecha_contrato_venta': str(fechaContratoVenta or ""),
                'Calle_Solicitud': str(calle or ""),
                'Sector_Solicitud': str(sector_nombre or ""),
                'Ciudad_Solicitud': str(sector_ciudad or ""),
                'Provincia_Solicitud': str(sector_provincia or ""),
                'COORDENADAS_X': str(coord_x or ""),
                'COORDENADAS_Y': str(coord_y or ""),
                'COORDENADAS_LATITUD': str(coordLatitud or ""),
                'COORDENADAS_LONGITUD': str(coordLongitud or ""),
                
                'NOMBRE_COMPLETO_NOTARIO': str(nombre_notario.upper() or "") + " " + str(apellido_notario.upper() or ""),
                'Municipio_Solicitud': str(sector_ciudad or ""),
                'Nro_Colegiatura_Notario': str(nroColegiatura_notario or ""),

                'dias_fecha_contrato_venta_texto': str(num2words(dia_fecha_contrato_venta,lang='es')),
                'dias_fecha_contrato_venta': str(dia_fecha_contrato_venta or ""),
                'mes_fecha_contrato_venta_texto': str(meses[int(mes_fecha_contrato_venta)-1]),
                'mes_fecha_contrato_venta': str(mes_fecha_contrato_venta or ""),
                'anio_fecha_contrato_venta_texto': str(num2words(anio_fecha_contrato_venta,lang='es')),
                'anio_fecha_contrato_venta': str(anio_fecha_contrato_venta or ""), 
                
                'dias_fecha_autorizacion_texto': str(num2words(dia_fecha_autorizacion,lang='es')),
                'dias_fecha_autorizacion': str(dia_fecha_autorizacion or ""),
                'mes_fecha_autorizacion_texto': str(meses[int(mes_fecha_autorizacion)-1]),
                'mes_fecha_autorizacion': str(mes_fecha_autorizacion or ""),
                'anio_fecha_autorizacion_texto': str(num2words(anio_fecha_autorizacion,lang='es')),
                'anio_fecha_autorizacion': str(anio_fecha_autorizacion or ""), 

                'el_SR_la_SRA_NOMBRE_COMPLETO_CLIENTE_01': str(c.el_SR_la_SRA_CLIENTE_01()),
                'SR_SRA_NOMBRE_COMPLETO_CLIENTE_01': str(c.SR_SRA_CLIENTE_01()),
                'portador_cedula_o_pasaporte_cliente_01': str(c.portador_cliente_01()) + " " + str(c.del_pasaporte_de_la_cedula_cliente_01()),
                'y_el_SR_la_SRA_NOMBRE_COMPLETO_CLIENTE_02': str(c.y_no()) + " " + str(c.el_SR_la_SRA_CLIENTE_02()) + str(c.coma_no()),
                'SR_SRA_NOMBRE_COMPLETO_CLIENTE_02': SR_SRA_NOMBRE_COMPLETO_CLIENTE_02,
                'portador_la_el_cedula_o_pasaporte_cliente_02': str(c.portador_cliente_02()) + " " + str(c.del_pasaporte_de_la_cedula_cliente_02()),
                'ambos_domiciliada_o_os_y_residente' : str(c.ambos_no()) + " " + str(c.domiciliado_s_residente_s()),
                'el_SR_los_SRES_NOMBRES': str(c.el_la_los_SR_SRA_SRES()) +  str(c.cliente_01_r()) + "y" + str(c.cliente_02_r()) ,
                'el_SR_los_SRES_NOMBRES_upper': str(c.el_la_los_SR_SRA_SRES()) + str(c.cliente_01_r()).upper() + str(c.y_no()) + str(c.cliente_02_r()).upper() ,
                'el_senior_los_seniores_NOMBRES': str(c.el_la_los_senior_seniora_seniores()) + " " + str(c.cliente_01_r()) + str(c.cliente_02_r()) ,
                'el_senior_los_seniores_NOMBRES_upper': str(c.el_la_los_senior_seniora_seniores()) + " " + str(c.cliente_01_r()).upper() + str(c.coma_espacio_client02()) + str(c.cliente_02_r()).upper() ,
                'portador_cedula_o_pasaporte_agrimensor': str(p_agrimensor.portador_a()) + " " + str(p_agrimensor.cedula_pasaporte()),
                'agrimensor_a': str(p_agrimensor.agrimensor_a()),

                'Propietario_cliente_01': str(p_cliente_01.Propietario_a()),
                'Propietario_cliente_02': str(c.Propietario02()),
                #'dominicano_, mayor de edad, divorciado': str(", dominicano , mayor de edad, divorciado"),

                'NOTARIO_A': str(p_notario.NOTARIO_A()),
                'Notario_a': str(p_notario.NOTARIO_A()).title(),
                'Licdo_a': str(p_notario.Licdo_Licda()),

                'agrimensor_a': str(p_agrimensor.agrimensor_a()),
                'el_la_agrimensor_a': str(p_agrimensor.el_la()) + ' ' + str(p_agrimensor.agrimensor_a()),
                'El_La_agrimensor_a': str(p_agrimensor.el_la()).title() + ' ' + str(p_agrimensor.agrimensor_a()),
                'el_la_notario': str(p_notario.el_la()),
                'Registrado_a_notario': str(p_notario.Registrado_a()),
            }


            # Reemplazar el texto en el documento
            replace_text_in_docx(documento_template,reemplazos)

            # Guardar el documento modificado
            archivo_salida = os.path.join(settings.MEDIA_ROOT, 'documentos', f'Solicitud_Autorizacion_{nombre_cliente01}.docx')
            documento_template.save(archivo_salida)

            url_archivo_salida_MEDIA = os.path.join(settings.MEDIA_URL, 'documentos', f'Solicitud_Autorizacion_{nombre_cliente01}.docx')
            url_archivo_salida = url_archivo_salida_MEDIA.replace("\\", "/")
            url_post_enlace = f"{API_URL}/solicitud_enlace/{idSolicitud}"
            url_archivo_salida_s = f"{settings.MEDIA_URL}documentos/Solicitud_Autorizacion_{urllib.parse.quote(nombre_cliente01)}.docx"
            datos_actualizados = {
                "Enlace": str(url_archivo_salida),
            }

            url_archivo_salida = urllib.parse.quote(url_archivo_salida)
            print(f"URL: {url_archivo_salida} ")
            headers = {
                    'Content-Type': 'application/json'
            }

            respuesta_put_enlace = requests.put(url_post_enlace, json=datos_actualizados,headers=headers)



            if respuesta_put_enlace.status_code == 200:
                print("Recurso actualizado exitosamente.")
            else:
                print(f"Error al actualizar el recurso: {respuesta_put_enlace.status_code}")

        

    return JsonResponse({'success': False, 'error': 'Método no permitido'})

