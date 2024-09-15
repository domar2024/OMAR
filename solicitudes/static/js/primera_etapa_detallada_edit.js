console.log(API_URL)
document.addEventListener('DOMContentLoaded', function() {
    const solicitudDetalle = document.getElementById('solicitud-detalle');
    const logoutButton = document.getElementById('logout');
    const backButton = document.getElementById('back-btn');
    const nextStepLink = document.getElementById('next-step-link');
    const downloadLink = document.getElementById('download_link');

    if (!localStorage.getItem('token')) {
        document.getElementById('error-message').innerText = 'You must be logged in to view this page';
        window.location.href = '/login/';
        return;
    }

    const token = localStorage.getItem('token');
    const urlParams = new URLSearchParams(window.location.search);
    const solicitudId = urlParams.get('id');


    function handleCheckboxChange(checkboxId, endpoint) {
        const checkbox = document.getElementById(checkboxId);
    
        checkbox.addEventListener('change', function() {
            const value = checkbox.checked; // true si está marcado, false si no
    
            // Realizar la solicitud fetch al endpoint correspondiente
            fetch(endpoint, {
                method: 'PUT', // Puedes cambiar el método a PUT si es necesario
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}` // Asegúrate de que token esté disponible
                },
                body: JSON.stringify({ value: value })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error al enviar la solicitud: ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                console.log('Respuesta del servidor:', data);
            })
            .catch(error => {
                console.error('Error en la solicitud:', error);
            });
        });
    }

    handleCheckboxChange('check-solicitud', `${API_URL}/solicitud_autorizacion_check_solicitud/${solicitudId}`);


    if (!solicitudId) {
        document.getElementById('error-message').innerText = 'Solicitud ID is missing in the URL';
        return;
    }

    lista_derecho_sustentados = ["","Contrato de Venta","Constancia Anotada","Certificado de Titulo"]


    const solicitudApiUrl = API_URL + `/solicitud/${solicitudId}`;

    // Cargar detalles de la solicitud
    fetch(solicitudApiUrl, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(solicitud => {
        conyugue = ""
        if(solicitud.Cliente02.Nombre != "Vacio"){
            conyugue = `
        <h3>Datos Conyugue:</h3>

        <p><strong>Nombre:</strong> ${solicitud.Cliente02.Nombre}</p>
        <p><strong>Apellidos:</strong> ${solicitud.Cliente02.Apellido}</p>
        <p><strong>Cédula o Pasaporte:</strong> ${solicitud.Cliente02.CedulaPasaporte}</p>
        <p><strong>Correo:</strong> ${solicitud.Cliente02.Correo}</p>
        <p><strong>Estado Civil:</strong> ${solicitud.Cliente02.EstadoCivil}</p>
        <p><strong>Nacionalidad:</strong> ${solicitud.Cliente02.Nacionalidad}</p>
        <p><strong>Ocupación:</strong> ${solicitud.Cliente02.Ocupacion}</p>
        <p><strong>Calle:</strong> ${solicitud.Cliente02.Calle}</p>
        <p><strong>Sector:</strong> ${solicitud.Cliente02.Sector.Sector}</p>
        <p><strong>Municipio:</strong> ${solicitud.Cliente02.Sector.Municipio}</p>
        <p><strong>Provincia:</strong> ${solicitud.Cliente02.Sector.Provincia}</p>
        <p><strong>País:</strong> ${solicitud.Cliente02.Sector.Pais}</p>
        <p><strong>Celular:</strong> ${solicitud.Cliente02.Celular}</p>
        <p><strong>Sexo:</strong> ${solicitud.Cliente02.Sexo}</p>
        `
        }

        solicitudDetalle.innerHTML = `
        <h3>Datos Cliente:</h3>
        
        <p><strong>Nombre:</strong> ${solicitud.Cliente01.Nombre}</p>
        <p><strong>Apellidos:</strong> ${solicitud.Cliente01.Apellido}</p>
        <p><strong>Cédula o Pasaporte:</strong> ${solicitud.Cliente01.CedulaPasaporte}</p>
        <p><strong>Correo:</strong> ${solicitud.Cliente01.Correo}</p>
        <p><strong>Estado Civil:</strong> ${solicitud.Cliente01.EstadoCivil}</p>
        <p><strong>Nacionalidad:</strong> ${solicitud.Cliente01.Nacionalidad}</p>
        <p><strong>Ocupación:</strong> ${solicitud.Cliente01.Ocupacion}</p>
        <p><strong>Calle:</strong> ${solicitud.Cliente01.Calle}</p>
        <p><strong>Sector:</strong> ${solicitud.Cliente01.Sector.Sector}</p>
        <p><strong>Municipio:</strong> ${solicitud.Cliente01.Sector.Municipio}</p>
        <p><strong>Provincia:</strong> ${solicitud.Cliente01.Sector.Provincia}</p>
        <p><strong>País:</strong> ${solicitud.Cliente01.Sector.Pais}</p>
        <p><strong>Celular:</strong> ${solicitud.Cliente01.Celular}</p>
        <p><strong>Sexo:</strong> ${solicitud.Cliente01.Sexo}</p>

        ${conyugue}
        
        <h3>Datos Agrimensor:</h3>

        
        <p><strong>Nombres:</strong> ${solicitud.Agrimensor.Nombre}</p>
        <p><strong>Apellidos:</strong> ${solicitud.Agrimensor.Apellido}</p>
        <p><strong>Cedula:</strong> ${solicitud.Agrimensor.Cedula}</p>
        <p><strong>CODIA:</strong> ${solicitud.Agrimensor.CODIA}</p>
        <p><strong>Celular:</strong> ${solicitud.Agrimensor.Celular}</p>
        <p><strong>Profesion:</strong> ${solicitud.Agrimensor.Profesion}</p>
        <p><strong>Correo:</strong> ${solicitud.Agrimensor.Correo}</p>
        <p><strong>Estado Civil:</strong> ${solicitud.Agrimensor.EstadoCivil}</p>
        <p><strong>Estado Civil:</strong> ${solicitud.Agrimensor.Nacionalidad}</p>
        <p><strong>Sexo:</strong> ${solicitud.Agrimensor.Sexo}</p>
        <p><strong>Calle:</strong> ${solicitud.Agrimensor.Calle}</p>
        <p><strong>Sector:</strong> ${solicitud.Agrimensor.Sector.Sector}</p>
        <p><strong>Provincia:</strong> ${solicitud.Agrimensor.Sector.Provincia}</p>
        <p><strong>Municipio:</strong> ${solicitud.Agrimensor.Sector.Municipio}</p>
        <p><strong>País:</strong> ${solicitud.Agrimensor.Sector.Pais}</p>

        <h3>Datos Notario:</h3>

        <p><strong>Nombres:</strong> ${solicitud.Notario.Nombre} ${solicitud.Notario.Apellido}</p>
        <p><strong>Nro. Colegiatura:</strong> ${solicitud.Notario.NroColegiatura}</p>
        <p><strong>Sexo:</strong> ${solicitud.Notario.Sexo}</p>
        <p><strong>Sector:</strong> ${solicitud.Notario.Sector.Sector}</p>
        <p><strong>Municipio:</strong> ${solicitud.Notario.Sector.Municipio}</p>
        <p><strong>Provincia:</strong> ${solicitud.Notario.Sector.Provincia}</p>
        <p><strong>Pais:</strong> ${solicitud.Notario.Sector.Pais}</p>

        
        <h3>Datos Generales / Inmueble:</h3>
        
        <p><strong>Nro Expediente:</strong> ${solicitud.NroExpediente}</p>
        <p><strong>Actuación Técnica:</strong> ${solicitud.ActuacionTecnica}</p>
        <p><strong>Área:</strong> ${solicitud.Area}</p>
        <p><strong>Coord. Latitud:</strong> ${solicitud.CoordLatitud}</p>
        <p><strong>Coord. Longitud:</strong>${solicitud.CoordLongitud}</p>
        <p><strong>Coord. Este:</strong> ${solicitud.CoordX}</p>
        <p><strong>Coord. Norte:</strong> ${solicitud.CoordY}</p>
        <p><strong>Fecha de Autorización:</strong> ${solicitud.FechaAutorizacion}</p>
        <p><strong>Fecha de Contrato de Venta:</strong> ${solicitud.FechaContratoVenta}</p>
        <p><strong>Distrito Catrastal:</strong> ${solicitud.DistritoCatrastal}</p>
        <p><strong>Calle:</strong> ${solicitud.Calle}</p>
        <p><strong>Sector:</strong> ${solicitud.Sector.Sector}</p>
        <p><strong>Municipio:</strong> ${solicitud.Sector.Municipio}</p>
        <p><strong>Provincia:</strong> ${solicitud.Sector.Provincia}</p>
        <p><strong>País:</strong> ${solicitud.Sector.Pais}</p>
        <p><strong>Parcela:</strong> ${solicitud.Parcela}</p>
        <p><strong>Departamento Oficina:</strong> ${solicitud.DepartamentoOficina.DepartamentoOficina}</p>
        <p><strong>Derecho Sustentado:</strong> ${lista_derecho_sustentados[solicitud.IdDerechoSustentado]}</p>
        `;
        if(solicitud.NroExpediente != 0){
            nextStepLink.href = `/form_segunda_etapa/?id=${solicitud.IdSolicitud}&expediente=${solicitud.NroExpediente}`;
            const colorAzul = getComputedStyle(document.documentElement).getPropertyValue('--color_azul');
            nextStepLink.style.backgroundColor = colorAzul;
        }else{
            nextStepLink.style.backgroundColor = "gray"
        }

        if(solicitud.checkSolicitud == true){
            document.getElementById('check-solicitud').checked = true;
        }else{
            document.getElementById('check-solicitud').checked = false;
        }   

        
        downloadLink.href = `${solicitud.Enlace}`;
    })
    
    .catch(error => {
        document.getElementById('error-message').innerText = 'Error fetching solicitud details: ' + error.message;
        console.error("Error fetching solicitud details:", error);
    });

    if (backButton) {
        backButton.addEventListener('click', function() {
            window.history.back();
        });
    }

    const deleteButton = document.getElementById('delete-button-total');
    const deleteButtonDesplegar = document.getElementById('delete_etapa_desplegar');
    const salirVentanaButton = document.getElementById('boton-salir-ventana');


    //Eliminar notificacion
    function dezplegar_ventana_eliminar(){
        ventana_confirmar = document.getElementById("ventana_confirmar");
        ventana_confirmar.style.display = "flex";
    }

    function ocultar_ventana_eliminar(){
        ventana_confirmar = document.getElementById("ventana_confirmar");
        ventana_confirmar.style.display = "none";
    }

    deleteButtonDesplegar.addEventListener('click', dezplegar_ventana_eliminar);
    salirVentanaButton.addEventListener('click', ocultar_ventana_eliminar);

    if (deleteButton) {
        deleteButton.addEventListener('click', function() {
            const deleteUrl = API_URL + `/solicitud/${solicitudId}`;
            
            fetch(deleteUrl, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                // Redirigir a la página de primera etapa
                window.location.href = '/primera_etapa/';
            })
            .catch((error) => {
                console.error('Error:', error);
                document.getElementById('error-message').innerText = 'Error deleting solicitud: ' + error.message;
            });
        });
    }


    if (logoutButton) {
        logoutButton.addEventListener('click', function() {
            localStorage.removeItem('token');
            window.location.href = '/login/';
        });
    }

    const expedienteForm = document.getElementById('expedienteForm');
    if (expedienteForm) {
        expedienteForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Previene que el formulario se envíe de manera tradicional
        
            const nroExpediente = document.getElementById('edit-num-expediente').value;
            const updateUrl = API_URL + `/solicitud_expediente/${solicitudId}`;

            const data = {
                NroExpediente: nroExpediente
            };
        
            fetch(updateUrl, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(data)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Respuesta del servidor:', data);
                // Recargar la página para ver los cambios
                window.location.reload();
            })
            .catch((error) => {
                console.error('Error:', error);
                document.getElementById('error-message').innerText = 'Error updating solicitud: ' + error.message;
            });
        });
    }
});
