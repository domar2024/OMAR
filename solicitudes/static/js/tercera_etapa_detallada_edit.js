console.log(API_URL)

document.addEventListener('DOMContentLoaded', function() {


    const avisomensuraDetalle = document.getElementById('informe-tecnica-detalle');
    const logoutButton = document.getElementById('logout');

    const downloadLinkConformidad = document.getElementById('download_link_conformidad');
    const downloadLinkDeclaracion = document.getElementById('download_link_declaracion');
    const downloadLinkInforme = document.getElementById('download_link_informe');
    const downloadLinkActa = document.getElementById('download_link_acta');

    if (!localStorage.getItem('token')) {
        document.getElementById('error-message').innerText = 'You must be logged in to view this page';
        window.location.href = '/login/';
        return;
    }

    const token = localStorage.getItem('token');
    const urlParams = new URLSearchParams(window.location.search);
    const informeTecnicoId = urlParams.get('id');
    const informeTecnicoApiUrl = API_URL + `/informe_tecnico/${informeTecnicoId}`;


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

    handleCheckboxChange('check-carta', `${API_URL}/informe_tecnico_check_carta/${informeTecnicoId}`);
    handleCheckboxChange('check-declaracion', `${API_URL}/informe_tecnico_check_declaracion/${informeTecnicoId}`);
    handleCheckboxChange('check-informe', `${API_URL}/informe_tecnico_check_informe/${informeTecnicoId}`);

    // Declarar informeTecnico en un alcance más amplio
    let informeTecnico;

    // Cargar detalles del aviso colindantes
    fetch(informeTecnicoApiUrl, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error fetching informe técnico');
        }
        return response.json();
    })
    .then(data => { 
        informeTecnico = data; // Asigna el valor a la variable definida en un ámbito más amplio
        
        conyugue = ""
        if(informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Cliente02.Nombre != "Vacio"){
            
            conyugue = `
                <h3>Datos Conyugue:</h3>
                <p><strong>Nombre:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Cliente02.Nombre}</p>
                <p><strong>Apellido:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Cliente02.Apellido}</p>
                <p><strong>Calle:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Cliente02.Calle}</p>
                <p><strong>Cedula:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Cliente02.CedulaPasaporte}</p>
                <p><strong>Celular:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Cliente02.Celular}</p>
                <p><strong>Correo:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Cliente02.Correo}</p>
                <p><strong>Estado Civil:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Cliente02.EstadoCivil}</p>
                <p><strong>Nacionalidad:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Cliente02.Nacionalidad}</p>
                <p><strong>Ocupacion:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Cliente02.Ocupacion}</p>
                <p><strong>Sexo:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Cliente02.Sexo}</p>
            `
        }
        avisomensuraDetalle.innerHTML = `
        <h3>Datos:</h3>
        <p><strong>Nombre:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Agrimensor.Nombre}</p>
        <p><strong>Apellido:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Agrimensor.Apellido}</p>
        <p><strong>CODIA:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Agrimensor.CODIA}</p>
        <p><strong>Calle:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Agrimensor.Calle}</p>
        <p><strong>Cedula:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Agrimensor.Cedula}</p>
        <p><strong>Celular:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Agrimensor.Celular}</p>
        <p><strong>Correo:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Agrimensor.Correo}</p>
        <p><strong>Estado Civil:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Agrimensor.EstadoCivil}</p>
        <p><strong>Nacionalidad:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Agrimensor.Nacionalidad}</p>
        <p><strong>Profesion:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Agrimensor.Profesion}</p>
        <p><strong>Sexo:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Agrimensor.Sexo}</p>
        

        <h3>Datos:</h3>
        <p><strong>Nombre:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Cliente01.Nombre}</p>
        <p><strong>Apellido:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Cliente01.Apellido}</p>
        <p><strong>Calle:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Cliente01.Calle}</p>
        <p><strong>Cedula:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Cliente01.CedulaPasaporte}</p>
        <p><strong>Celular:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Cliente01.Celular}</p>
        <p><strong>Correo:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Cliente01.Correo}</p>
        <p><strong>Estado Civil:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Cliente01.EstadoCivil}</p>
        <p><strong>Nacionalidad:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Cliente01.Nacionalidad}</p>
        <p><strong>Ocupacion:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Cliente01.Ocupacion}</p>
        <p><strong>Sexo:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Cliente01.Sexo}</p>
        

        ${conyugue}
        

        <h3>Datos:</h3>
        <p><strong>Nombre:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Notario.Nombre}</p>
        <p><strong>Apellido:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Notario.Apellido}</p>
        <p><strong>Nro Colegiatura:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Notario.NroColegiatura}</p>
        <p><strong>Sexo:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Notario.Sexo}</p>
        <p><strong>Sector:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Notario.Sector.Sector}</p>
        <p><strong>Municipio:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Notario.Sector.Municipio}</p>
        <p><strong>Pais:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Notario.Sector.Pais}</p>
        <p><strong>Provincia:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Notario.Sector.Provincia}</p>
        

        <h3>Otros Datos:</h3>
        <p><strong>Coord Latitud:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.CoordLatitud}</p>
        <p><strong>Coord Longitud:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.CoordLongitud}</p>
        <p><strong>Coord X:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.CoordX}</p>
        <p><strong>Coord Y:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.CoordY}</p>
        <p><strong>Distrito Catastral:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.DistritoCatrastal}</p>
        <p><strong>Fecha Autorizacion:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.FechaAutorizacion}</p>
        <p><strong>Fecha Documento de Derecho:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.FechaContratoVenta}</p>
        <p><strong>Nro Expediente:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.NroExpediente}</p>
        <p><strong>Parcela:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Parcela}</p>
        <p><strong>Sector:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Sector.Sector}</p>
        <p><strong>Municipio:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Sector.Municipio}</p>
        <p><strong>Pais:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Sector.Pais}</p>
        <p><strong>Provincia:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Sector.Provincia}</p>
        
        <p><strong>Delimitacion Este:</strong> ${informeTecnico.DelimitacionEste}</p>
        <p><strong>Delimitacion Norte:</strong> ${informeTecnico.DelimitacionNorte}</p>
        <p><strong>Delimitacion Oeste:</strong> ${informeTecnico.DelimitacionOeste}</p>
        <p><strong>Delimitacion Sur:</strong> ${informeTecnico.DelimitacionSur}</p>
        
        
        <p><strong>Fecha Hora Inicio Mensura:</strong> ${informeTecnico.FechaHoraInicioMensura}</p>
        <p><strong>Hora Fin Mesura:</strong> ${informeTecnico.HoraFinMesura}</p>

        <p><strong>Area Diferencia:</strong> ${informeTecnico.AreaDiferencia.AreaDiferencia}</p>
        
        <p><strong>Area Diferenciada:</strong> ${informeTecnico.AreaDiferenciada}</p>
        <p><strong>Area Total:</strong> ${informeTecnico.AreaTotal}</p>
        
        <p><strong>Derecho Sustentado:</strong> ${informeTecnico.DeclaracionPosesion.DerechoSustentado.DerechoSustentado}</p>
        
        <p><strong>Fecha Autorizacion Aviso Mensura:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.AvisoMensura.FechaAutorizacion}</p>
        <p><strong>Fecha y Hora de Mensura:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.AvisoMensura.FechaHoraMensura}</p>
        
        
        <p><strong>Departamento Oficina:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.DepartamentoOficina.DepartamentoOficina}</p>
        <p><strong>Encargado Departamento Oficina:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.DepartamentoOficina.Encargado}</p>
        

        <p><strong>Actuacion Tecnica:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.ActuacionTecnica}</p>
        <p><strong>Area:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Area}</p>
        <p><strong>Calle:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.Calle}</p>

        <h3>Departamento Oficina:</h3>
        <p><strong>Municipio:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.DepartamentoOficina.sector.Municipio}</p>
        <p><strong>Pais:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.DepartamentoOficina.sector.Pais}</p>
        <p><strong>Provincia:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.DepartamentoOficina.sector.Provincia}</p>
        <p><strong>Sector:</strong> ${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.DepartamentoOficina.sector.Sector}</p>
        `;

        downloadLinkConformidad.href = `${informeTecnico.DeclaracionPosesion.CartaConformidad.Enlace}`;
        downloadLinkDeclaracion.href = `${informeTecnico.DeclaracionPosesion.Enlace}`;
        downloadLinkInforme.href = `${informeTecnico.Enlace}`;
        downloadLinkActa.href = `${informeTecnico.EnlaceActaHitos}`;

        if(informeTecnico.checkCarta == true){
            document.getElementById('check-carta').checked = true;
        }else{
            document.getElementById('check-carta').checked = false;
        }   

        if(informeTecnico.checkDeclaracion == true){
            document.getElementById('check-declaracion').checked = true;
        }else{
            document.getElementById('check-declaracion').checked = false;
        }   

        if(informeTecnico.checkInforme == true){
            document.getElementById('check-informe').checked = true;
        }else{
            document.getElementById('check-informe').checked = false;
        }   
    })
    .catch(error => {
        document.getElementById('error-message').innerText = 'Error fetching informe técnico details: ' + error.message;
        console.error("Error fetching informe técnico details:", error);
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
            const deleteUrl = API_URL + `/informe_tecnico/${informeTecnicoId}`;
            
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
                const activarSolicitudUrl = API_URL + `/avisocolindantes_estatus/${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.IdAvisoColindantes}`;
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
                // Redirigir a la página de segunda etapa
                window.location.href = '/segunda_etapa/';
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
