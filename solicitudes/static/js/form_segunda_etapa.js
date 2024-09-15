console.log(API_URL)
document.addEventListener('DOMContentLoaded', function() {
    const avisomensuraForm = document.getElementById('avisomensura-form');
    const solicitudIdElement = document.getElementById('solicitud-id');
    const expedienteNumeroElement = document.getElementById('expediente-numero');
    let idDepartamentoOficina;;
    const token = localStorage.getItem('token');

    // Verificar autenticación
    if (!token) {
        window.location.href = '/login/';
        return;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const solicitudId = urlParams.get('id');
    const nroExpediente = urlParams.get('expediente');

    if (!solicitudId) {
        document.getElementById('error-message').innerText = 'No se encontró el ID de la solicitud.';
        return;
    }

    // Mostrar ID de Solicitud y Número de Expediente
    solicitudIdElement.textContent = solicitudId;
    expedienteNumeroElement.textContent = "Formulario Publicidad - " + nroExpediente ;

    //const departamentosApiUrl = API_URL + '/departamentos';
    const solicitudApiUrl = API_URL + `/solicitud/${solicitudId}`;


        // Después de cargar las opciones, buscar y seleccionar el Departamento Oficina correspondiente
        fetch(solicitudApiUrl, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
    //})
    .then(response => response.json())
    .then(solicitud => {
        idDepartamentoOficina = solicitud.DepartamentoOficina.IdDepartamentoOficina;
    })
    .catch(error => {
        document.getElementById('error-message').innerText = 'Error fetching data: ' + error.message;
        console.error("Error fetching data:", error);
    });

    // Manejar el envío del formulario
    avisomensuraForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const avisomensuraData = {
            IdSolicitud: parseInt(solicitudId),
            FechaHoraMensura: document.getElementById('fecha-hora-mensura').value,
            FechaAutorizacion: document.getElementById('fecha-autorizacion').value,
            IdDepartamentoOficina: idDepartamentoOficina,
            Enlace: "",  // Se envía el campo "Enlace" como vacío
            Estatus: 1
        };

        fetch(API_URL + '/avisomensura', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(avisomensuraData)
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => { throw new Error(data.message || 'Error al enviar el aviso de mensura'); });
            }
            return response.json();
        })
        .then(avisomensura => {
            alert('Aviso de mensura enviado exitosamente');
            // Enviar datos a avisoperiodico
            const avisoPeriodicoData = {
                IdAvisoMensura: avisomensura.IdAvisoMensura,
                Estatus: 1
            };
            return fetch(API_URL + '/avisoperiodico', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(avisoPeriodicoData)
            });
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => { throw new Error(data.message || 'Error al enviar el aviso periodico'); });
            }
            return response.json();
        })
        .then(avisoPeriodico => {
            // Enviar datos a avisocolindantes
            const avisoColindantesData = {
                IdAvisoPeriodico: avisoPeriodico.IdAvisoPeriodico,
                FechaVencimiento: document.getElementById('fecha-vencimiento').value,
                Estatus: 1
            };
            return fetch(API_URL + '/avisocolindantes', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(avisoColindantesData)
            });
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => { throw new Error(data.message || 'Error al enviar el aviso colindantes'); });
            }
            return response.json();
        })
        .then(avisoColindantes => {
            // Guarda el IdAvisoColindantes en la variable
            idAvisoColindantes = avisoColindantes.IdAvisoColindantes;
            alert('Aviso colindantes enviado exitosamente');
            
            // Aquí agregamos la funcionalidad DELETE
            return fetch(API_URL + `/solicitud/${solicitudId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
        })
        .then(async response => {
            if (!response.ok) {
                throw new Error('Error al eliminar la solicitud');
            }

            // Función para manejar el segundo POST a Django
            const enviarDatosADjango = async () => {
                const djangoResponse = await fetch('/procesar_formulario_segunda_etapa/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({"IdAvisoColindantes": idAvisoColindantes})
                });

                const djangoResult = await djangoResponse.json();

                if (!djangoResponse.ok) {
                    throw new Error(djangoResult.message || 'Error al procesar los datos en Django');
                }

                console.log('Datos enviados a Django exitosamente');
                // Puedes realizar alguna acción adicional después de que Django haya procesado los datos

                window.location.href = '/segunda_etapa/';
            };

            // Llamar a la función async
            await enviarDatosADjango();
        })
        .catch(error => {
            document.getElementById('error-message').innerText = 'Error: ' + error.message;
            console.error('Error:', error);
        });
    });
});
