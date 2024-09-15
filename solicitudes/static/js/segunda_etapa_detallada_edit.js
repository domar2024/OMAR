console.log(API_URL)
document.addEventListener('DOMContentLoaded', function() {
    const avisomensuraDetalle = document.getElementById('avisomensura-detalle');
    const logoutButton = document.getElementById('logout');

    const nextStepLink = document.getElementById('next-step-link');

    const downloadLinkMensura = document.getElementById('download_link_mensura');
    const downloadLinkPeriodico = document.getElementById('download_link_periodico');
    const downloadLinkColindante = document.getElementById('download_link_colindante');

    if (!localStorage.getItem('token')) {
        document.getElementById('error-message').innerText = 'You must be logged in to view this page';
        window.location.href = '/login/';
        return;
    }

    const token = localStorage.getItem('token');
    const urlParams = new URLSearchParams(window.location.search);
    const avisoColindantesId = urlParams.get('id');
    const avisoColindantesApiUrl = API_URL + `/avisocolindantes/${avisoColindantesId}`;

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

    handleCheckboxChange('check-mensura', `${API_URL}/aviscolindantes_check_mensura/${avisoColindantesId}`);
    handleCheckboxChange('check-periodico', `${API_URL}/aviscolindantes_check_periodico/${avisoColindantesId}`);
    handleCheckboxChange('check-colindante', `${API_URL}/aviscolindantes_check_colindantes/${avisoColindantesId}`);


    // Cargar detalles del aviso colindantes
    fetch(avisoColindantesApiUrl, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => response.json())
    .then(data => {
        avisoColindante = data; // Asigna el valor aquí

        // Obtener datos adicionales de la solicitud a partir del IdSolicitud
        const solicitudUrl = API_URL + `/solicitud/${avisoColindante.AvisoMensura.IdSolicitud}`;
        return fetch(solicitudUrl, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => response.json())
        .then(solicitudData => ({ avisoColindante, solicitudData }));
    })
    .then(({ avisoColindante, solicitudData }) => {
        conyugue = ""
        if(avisoColindante.SolicitudAutorizacion.Cliente02.Nombre != "Vacio"){
            
            conyugue = `
                <h3>Datos Conyugue:</h3>
                <p><strong>Nombre:</strong> ${avisoColindante.SolicitudAutorizacion.Cliente02.Nombre}</p>
                <p><strong>Apellido:</strong> ${avisoColindante.SolicitudAutorizacion.Cliente02.Apellido}</p>
                <p><strong>Calle:</strong> ${avisoColindante.SolicitudAutorizacion.Cliente02.Calle}</p>
                <p><strong>Cédula o Pasaporte:</strong> ${avisoColindante.SolicitudAutorizacion.Cliente02.CedulaPasaporte}</p>
                <p><strong>Correo:</strong> ${avisoColindante.SolicitudAutorizacion.Cliente02.Correo}</p>
                <p><strong>Estado Civil:</strong> ${avisoColindante.SolicitudAutorizacion.Cliente02.EstadoCivil}</p>
                <p><strong>Nacionalidad:</strong> ${avisoColindante.SolicitudAutorizacion.Cliente02.Nacionalidad}</p>
                <p><strong>Ocupacion:</strong> ${avisoColindante.SolicitudAutorizacion.Cliente02.Ocupacion}</p>
                <p><strong>Calle:</strong> ${avisoColindante.SolicitudAutorizacion.Cliente02.Calle}</p>
                <p><strong>Sector:</strong> ${avisoColindante.SolicitudAutorizacion.Cliente02.Sector.Sector}</p>
                <p><strong>Municipio:</strong> ${avisoColindante.SolicitudAutorizacion.Cliente02.Sector.Municipio}</p>
                <p><strong>Provincia:</strong> ${avisoColindante.SolicitudAutorizacion.Cliente02.Sector.Provincia}</p>
                <p><strong>Provincia:</strong> ${avisoColindante.SolicitudAutorizacion.Cliente02.Sector.Provincia}</p>
                <p><strong>Celular:</strong> ${avisoColindante.SolicitudAutorizacion.Cliente02.Celular}</p>
                <p><strong>Sexo:</strong> ${avisoColindante.SolicitudAutorizacion.Cliente02.Sexo}</p>
            `
            }
        avisomensuraDetalle.innerHTML = `
    
        
        <h3>Datos Cliente:</h3>
        <p><strong>Nombre:</strong> ${avisoColindante.SolicitudAutorizacion.Cliente01.Nombre}</p>
        <p><strong>Apellido:</strong> ${avisoColindante.SolicitudAutorizacion.Cliente01.Apellido}</p>
        <p><strong>Cédula o Pasaporte:</strong> ${avisoColindante.SolicitudAutorizacion.Cliente01.CedulaPasaporte}</p>
        <p><strong>Correo:</strong> ${avisoColindante.SolicitudAutorizacion.Cliente01.Correo}</p>
        <p><strong>Estado Civil:</strong> ${avisoColindante.SolicitudAutorizacion.Cliente01.EstadoCivil}</p>
        <p><strong>Nacionalidad:</strong> ${avisoColindante.SolicitudAutorizacion.Cliente01.Nacionalidad}</p>
        <p><strong>Ocupacion:</strong> ${avisoColindante.SolicitudAutorizacion.Cliente01.Ocupacion}</p>
        <p><strong>Calle:</strong> ${avisoColindante.SolicitudAutorizacion.Cliente01.Calle}</p>
        <p><strong>Sector:</strong> ${avisoColindante.SolicitudAutorizacion.Cliente01.Sector.Sector}</p>
        <p><strong>Municipio:</strong> ${avisoColindante.SolicitudAutorizacion.Cliente01.Sector.Municipio}</p>
        <p><strong>Provincia:</strong> ${avisoColindante.SolicitudAutorizacion.Cliente01.Sector.Provincia}</p>
        <p><strong>País:</strong> ${avisoColindante.SolicitudAutorizacion.Cliente01.Sector.Pais}</p>
        <p><strong>Celular:</strong> ${avisoColindante.SolicitudAutorizacion.Cliente01.Celular}</p>
        <p><strong>Sexo:</strong> ${avisoColindante.SolicitudAutorizacion.Cliente01.Sexo}</p>
    

        ${conyugue}

        <h3>Datos Agrimensor:</h3>
        <p><strong>Nombre:</strong> ${avisoColindante.SolicitudAutorizacion.Agrimensor.Nombre}</p>
        <p><strong>Apellido:</strong> ${avisoColindante.SolicitudAutorizacion.Agrimensor.Apellido}</p>
        <p><strong>Cedula:</strong> ${avisoColindante.SolicitudAutorizacion.Agrimensor.Cedula}</p>
        <p><strong>CODIA:</strong> ${avisoColindante.SolicitudAutorizacion.Agrimensor.CODIA}</p>
        <p><strong>Celular:</strong> ${avisoColindante.SolicitudAutorizacion.Agrimensor.Celular}</p>
        <p><strong>Profesion:</strong> ${avisoColindante.SolicitudAutorizacion.Agrimensor.Profesion}</p>
        <p><strong>Correo:</strong> ${avisoColindante.SolicitudAutorizacion.Agrimensor.Correo}</p>
        <p><strong>Estado Civil:</strong> ${avisoColindante.SolicitudAutorizacion.Agrimensor.EstadoCivil}</p>
        <p><strong>Nacionalidad:</strong> ${avisoColindante.SolicitudAutorizacion.Agrimensor.Nacionalidad}</p>
        <p><strong>Sexo:</strong> ${avisoColindante.SolicitudAutorizacion.Agrimensor.Sexo}</p>

        
        <p><strong>Calle:</strong> ${avisoColindante.SolicitudAutorizacion.Agrimensor.Calle}</p>
        <p><strong>Sector:</strong> ${avisoColindante.SolicitudAutorizacion.Agrimensor.Sector.Sector}</p>
        <p><strong>Provincia:</strong> ${avisoColindante.SolicitudAutorizacion.Agrimensor.Sector.Provincia}</p>
        <p><strong>Municipio:</strong> ${avisoColindante.SolicitudAutorizacion.Agrimensor.Sector.Municipio}</p>
        <p><strong>País:</strong> ${avisoColindante.SolicitudAutorizacion.Agrimensor.Sector.Pais}</p>


        <h3>Datos Notario:</h3>
        <p><strong>Nombres:</strong> ${avisoColindante.SolicitudAutorizacion.Notario.Nombre} ${avisoColindante.SolicitudAutorizacion.Notario.Apellido}</p>
        <p><strong>Nro. Colegiatura:</strong> ${avisoColindante.SolicitudAutorizacion.Notario.NroColegiatura}</p>
        <p><strong>Sexo:</strong> ${avisoColindante.SolicitudAutorizacion.Notario.Sexo}</p>
        <p><strong>Sector:</strong> ${avisoColindante.SolicitudAutorizacion.Notario.Sector.Sector}</p>
        <p><strong>Municipio:</strong> ${avisoColindante.SolicitudAutorizacion.Notario.Sector.Municipio}</p>
        <p><strong>Provincia:</strong> ${avisoColindante.SolicitudAutorizacion.Notario.Sector.Provincia}</p>
        <p><strong>Pais:</strong> ${avisoColindante.SolicitudAutorizacion.Notario.Sector.Pais}</p>
        
        <h3>Datos Generales / Inmueble:</h3>
        <p><strong>Nro. Expediente:</strong> ${avisoColindante.SolicitudAutorizacion.NroExpediente}</p>
        <p><strong>ActuacionTecnica:</strong> ${avisoColindante.SolicitudAutorizacion.ActuacionTecnica}</p>
        <p><strong>Área:</strong> ${avisoColindante.SolicitudAutorizacion.Area}</p>

        <p><strong>Coord. Latitud:</strong> ${avisoColindante.SolicitudAutorizacion.CoordLatitud}</p>
        <p><strong>Coord. Longitud:</strong> ${avisoColindante.SolicitudAutorizacion.CoordLongitud}</p>
        <p><strong>Coord. Este:</strong> ${avisoColindante.SolicitudAutorizacion.CoordX}</p>
        <p><strong>Coord. Norte:</strong> ${avisoColindante.SolicitudAutorizacion.CoordY}</p>
        
        <p><strong>Fecha Autorización:</strong> ${avisoColindante.SolicitudAutorizacion.FechaAutorizacion}</p>
        <p><strong>Fecha Contrato de Venta:</strong> ${avisoColindante.SolicitudAutorizacion.FechaContratoVenta}</p>
        <p><strong>Distrito Catrastal:</strong> ${avisoColindante.SolicitudAutorizacion.DistritoCatrastal}</p>
        <p><strong>Calle:</strong> ${avisoColindante.SolicitudAutorizacion.Calle}</p>
        <p><strong>Sector:</strong> ${avisoColindante.SolicitudAutorizacion.Sector.Sector}</p>
        
        <p><strong>Municipio:</strong> ${avisoColindante.SolicitudAutorizacion.Sector.Municipio}</p>

        <p><strong>Provincia:</strong> ${avisoColindante.SolicitudAutorizacion.Sector.Provincia}</p>
        
        <p><strong>País:</strong> ${avisoColindante.SolicitudAutorizacion.Sector.Pais}</p>
        <p><strong>Parcela:</strong> ${avisoColindante.SolicitudAutorizacion.Parcela}</p>
        
        <p><strong>Departamento Oficina:</strong> ${avisoColindante.DepartamentoOficina.DepartamentoOficina}</p>
        <p><strong>Derecho Sustentado:</strong> ${avisoColindante.SolicitudAutorizacion.DerechoSustentado.DerechoSustentado}</p>
        
        <p><strong>Fecha de Autorizacion:</strong> ${avisoColindante.AvisoMensura.FechaAutorizacion}</p>
        <p><strong>Fecha y hora mensura:</strong> ${avisoColindante.AvisoMensura.FechaHoraMensura}</p>

        
        <!-- Sector en Departamento Oficina
        <p><strong>Municipio:</strong> ${avisoColindante.DepartamentoOficina.sector.Municipio}</p>
        <p><strong>Pais:</strong> ${avisoColindante.DepartamentoOficina.sector.Pais}</p>
        <p><strong>Provincia:</strong> ${avisoColindante.DepartamentoOficina.sector.Provincia}</p>
        <p><strong>Sector:</strong> ${avisoColindante.DepartamentoOficina.sector.Sector}</p>-->
        

        `;

        downloadLinkMensura.href = `${avisoColindante.AvisoMensura.Enlace}`;
        downloadLinkPeriodico.href = `${avisoColindante.AvisoPeriodico.Enlace}`;
        downloadLinkColindante.href = `${avisoColindante.Enlace}`;

        if(avisoColindante.checkMensura == true){
            document.getElementById('check-mensura').checked = true;
        }else{
            document.getElementById('check-mensura').checked = false;
        }   

        if(avisoColindante.checkPeriodico == true){
            document.getElementById('check-periodico').checked = true;
        }else{
            document.getElementById('check-periodico').checked = false;
        }   

        if(avisoColindante.checkColindantes == true){
            document.getElementById('check-colindante').checked = true;
        }else{
            document.getElementById('check-colindante').checked = false;
        }   

        // Construir el enlace con los parámetros requeridos
        nextStepLink.href = `/form_tercera_etapa/?id=${avisoColindante.IdAvisoColindantes}&solicitud=${avisoColindante.AvisoMensura.IdSolicitud}&expediente=${avisoColindante.SolicitudAutorizacion.NroExpediente}&idDerechoSustentado=${avisoColindante.SolicitudAutorizacion.DerechoSustentado.IdDerechoSustentado}&Area=${avisoColindante.SolicitudAutorizacion.Area}&FechaHoraMensura=${avisoColindante.AvisoMensura.FechaHoraMensura}&FechaDocumentoDerecho=${avisoColindante.SolicitudAutorizacion.FechaContratoVenta}`;
    })
    .catch(error => {
        document.getElementById('error-message').innerText = 'Error fetching aviso colindantes details: ' + error.message;
        console.error("Error fetching aviso colindantes details:", error);
    });


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
            const deleteUrl = API_URL + `/avisocolindantes/${avisoColindantesId}`;
            
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
    
                // Realizar la solicitud PUT para activar la solicitud con el JSON "Estatus"
                const activarSolicitudUrl = API_URL + `/solicitud_estatus/${avisoColindante.AvisoMensura.IdSolicitud}`;
                return fetch(activarSolicitudUrl, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ "Estatus": 1 })  // JSON con la clave "Estatus"
                });
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
});
