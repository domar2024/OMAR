console.log(API_URL)
document.addEventListener('DOMContentLoaded', function () {
    let idInformeTecnico;
    
    const conformidadForm = document.getElementById('conformidad-form');
    const solicitudIdElement = document.getElementById('solicitud-id');
    const expedienteNumeroElement = document.getElementById('expediente-numero');
    const token = localStorage.getItem('token');
    const selectAreaDiferencia = document.getElementById('area-diferencia');
    
    if (!token) {
        window.location.href = '/login/';
        return;
    }
    
    const urlParams = new URLSearchParams(window.location.search);
    const avisoColindantesId = urlParams.get('id');
    const solicitudId = urlParams.get('solicitud');
    const nroExpediente = urlParams.get('expediente');
    const IdDefectodDerechoSustentado = urlParams.get('idDerechoSustentado');
    const Area = urlParams.get('Area');
    const FechaHoraMensura = urlParams.get('FechaHoraMensura');
    const FechaDocumentoDerecho = urlParams.get('FechaDocumentoDerecho');

    // Aquí insertamos las definiciones de las constantes y la función
    const areaDerecho = document.getElementById('area');
    const areaDiferenciada = document.getElementById('area-diferenciada');
    const areaMensura = document.getElementById('area-total');
    const areaDiferenciaSelect = document.getElementById('area-diferencia');
    const inputDescripcionInmueble = document.getElementById('descripcion-inmueble')
    var valorAreaDiferenciada =  0;


    function getValueDescripcion() {
        return inputDescripcionInmueble.disabled ? 'Yermo' : inputDescripcionInmueble.value || null;
    }

    function actualizarAreaTotal() {
        const valorAreaDerecho = parseFloat(areaDerecho.value) || 0;
        const valorAreaMensura = parseFloat(areaMensura.value) || 0;
        const tipoDiferencia = areaDiferenciaSelect.value;  // Obtén el valor del selector de diferencia

        console.log('Valor Área:', valorAreaDerecho);
        console.log('Valor Área Mensura:', valorAreaMensura);
        console.log('Tipo Diferencia:', tipoDiferencia);

        let resultado = 0;

        // Realiza la operación de suma o resta basada en la selección

        valorAreaDiferenciada = valorAreaDerecho - valorAreaMensura;
        if (valorAreaMensura < valorAreaDerecho) {
            selectAreaDiferencia.value = 2;
            
        } else if (valorAreaMensura > valorAreaDerecho) {
            selectAreaDiferencia.value = 1;
        }

        areaDiferenciada.value = valorAreaDiferenciada.toFixed(2);

        console.log(valorAreaDiferenciada)

    }

    areaDerecho.addEventListener('input', actualizarAreaTotal);
    areaMensura.addEventListener('input', actualizarAreaTotal);

    console.log(nroExpediente)

    

    solicitudIdElement.textContent = solicitudId;
    expedienteNumeroElement.textContent = "Formulario Expediente - " + nroExpediente;

    const loadOptions = (url, selectElementId, idField, textField) => {
        fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
            .then(response => response.json())
            .then(data => {
                const selectElement = document.getElementById(selectElementId);
                data.forEach(item => {
                    const option = document.createElement('option');
                    option.value = item[idField];
                    option.textContent = item[textField];
                    selectElement.appendChild(option);
                });

                if (selectElementId === 'derecho-sustentado') {
                    console.log(IdDefectodDerechoSustentado)
                    selectElement.value = IdDefectodDerechoSustentado;  // Ajusta el valor del selector
                }
            })
            .catch(error => {
                document.getElementById('error-message').innerText = `Error fetching ${selectElementId}: ` + error.message;
            });
    };

    loadOptions(API_URL + '/derechos_sustentados', 'derecho-sustentado', 'IdDerechoSustentado', 'DerechoSustentado');
    loadOptions(API_URL + '/area_diferencias', 'area-diferencia', 'IdAreaDiferencia', 'AreaDiferencia');
    document.getElementById('area').value = Number(Area)
    document.getElementById('hora-inicio-mensura').value = FechaHoraMensura.substring(11)
    conformidadForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const conformidadData = {
            IdSolicitud: parseInt(solicitudId),
            IdAvisoColindantes: parseInt(avisoColindantesId)
        };

        fetch(API_URL + '/conformidad', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(conformidadData)
        })
            .then(response => response.json())
            .then(conformidad => {
                const declaracionPosesionData = {
                    IdConformidad: conformidad.IdConformidad,
                    IdDerechoSustentado: parseInt(document.getElementById('derecho-sustentado').value),
                    FechaDocumentoDerecho: FechaDocumentoDerecho
                };

                return fetch(API_URL + '/declaracion_posesion', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(declaracionPosesionData)
                });
            })

            //FechaHoraInicioMensura: document.getElementById('fecha-hora-inicio-mensura').value,
            .then(response => response.json())
            .then(declaracionPosesion => {
                const informeTecnicoData = {
                    IdDeclaracionPosesion: parseInt(declaracionPosesion.IdDeclaracionPosesion),
                    FechaHoraInicioMensura: FechaHoraMensura,
                    HoraFinMesura: document.getElementById('hora-fin-mensura').value,
                    FechaDocumentoDerecho: FechaDocumentoDerecho,
                    IdAreaDiferencia: parseInt(document.getElementById('area-diferencia').value),
                    AreaTotal: parseFloat(document.getElementById('area-total').value),
                    AreaDiferenciada: parseFloat(document.getElementById('area-diferenciada').value),
                    DelimitacionNorte: document.getElementById('delimitacion-norte').value,
                    DelimitacionSur: document.getElementById('delimitacion-sur').value,
                    DelimitacionOeste: document.getElementById('delimitacion-oeste').value,
                    DelimitacionEste: document.getElementById('delimitacion-este').value,
                    UbicacionInmueble: document.getElementById('ubicacion-inmueble').value,  // Nuevo campo
                    DescripcionInmueble: getValueDescripcion(),  // Nuevo campo
                    NombreEquipo: document.getElementById('nombre-equipo').value,  // Nuevo campo
                    ModeloEquipo: document.getElementById('modelo-equipo').value,  // Nuevo campo
                    Enlace: ""
                };

                console.log('Enviando informeTecnicoData:', informeTecnicoData);

                return fetch(API_URL + '/informe_tecnico', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(informeTecnicoData)

                });

            })
            .then(response => response.json())
            .then((informeTecnico) => {

                idInformeTecnico = informeTecnico.IdInformeTecnico;

                console.log('IdInformeTecnico obtenido:', idInformeTecnico);

                return fetch(API_URL + `/avisocolindantes/${avisoColindantesId}`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
            })
            .then(response => response.json())
            .then(avisoColindante => {
                const avisoMensuraId = avisoColindante.AvisoMensura.IdAvisoMensura;
                return fetch(API_URL + `/avisomensura/${avisoMensuraId}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
            })
            // Supongamos que este es el código donde tienes el await
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error al eliminar el aviso mensura');
                }
                // Ahora eliminamos el aviso colindante
                return fetch(API_URL + `/avisocolindantes/${avisoColindantesId}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error al eliminar el aviso colindante');
                }
                alert('Proceso completado y aviso mensura eliminado');

                // Aquí es donde necesitas modificar para usar async/await correctamente
                const enviarDatosADjango = async () => {  // Cambiado para ser async
                    const djangoResponse = await fetch('/procesar_formulario_tercera_etapa/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ "IdInformeTecnico": idInformeTecnico  })
                    });

                    const djangoResult = await djangoResponse.json();

                    if (!djangoResponse.ok) {
                        throw new Error(djangoResult.message || 'Error al procesar los datos en Django');
                    }

                    console.log('Datos enviados a Django exitosamente');
                    // Puedes realizar alguna acción adicional después de que Django haya procesado los datos

                    window.location.href = '/tercera_etapa/';
                };

                // Llamar a la función async de manera correcta
                enviarDatosADjango(); // No uses await aquí porque no estás en una función async
            })
            .catch(error => {
                document.getElementById('error-message').innerText = 'Error: ' + error.message;
                console.error('Error:', error);
            });

    });

    document.getElementById('idCheckboxDescripcion').addEventListener('click', function() {
        const inputDescripcionInmueble = document.getElementById('descripcion-inmueble');

        if (this.checked) {
            inputDescripcionInmueble.disabled = false;
        } else {
            inputDescripcionInmueble.disabled = true;
            inputDescripcionInmueble.value = 'Yermo';  // Resetea el valor del select
        }
    });
});
