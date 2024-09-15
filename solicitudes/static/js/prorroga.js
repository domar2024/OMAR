console.log(API_URL)
document.addEventListener('DOMContentLoaded', function() {
    const informesTecnicosTable = document.getElementById('informes-tecnicos-table');
    const logoutButton = document.getElementById('logout');

    if (!localStorage.getItem('token')) {
        document.getElementById('error-message').innerText = 'You must be logged in to view this page';
        window.location.href = '/login/';
        return;
    }

    const token = localStorage.getItem('token');
    const informesTecnicosApiUrl = API_URL + '/informes_tecnicos';
    const avisosColindantesApiUrl = API_URL + '/avisoscolindantes';


    function calcularDiasRestantes(fecha) {
        // Convertir la fecha actual y la fecha dada a objetos Date
        const fechaActual = new Date();
        const fechaObjetivo = new Date(fecha);
        
        // Calcular la diferencia en milisegundos
        const diferenciaMilisegundos = fechaObjetivo - fechaActual;
        
        // Convertir la diferencia de milisegundos a días
        const diasRestantes = Math.ceil(diferenciaMilisegundos / (1000 * 60 * 60 * 24));
        
        return diasRestantes;
    }
    // Cargar lista de informes técnicos
    fetch(informesTecnicosApiUrl, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => response.json())
    .then(data => {
        if (!Array.isArray(data)) {
            throw new Error('La respuesta de la API no es un array.');
        }

        const filteredInformesTecnicos = data.filter(informe => informe.Estatus === 1 && informe.DeclaracionPosesion.CartaConformidad.AvisoColindantes?.SolicitudAutorizacion?.IdSolicitud);


        return Promise.all(filteredInformesTecnicos.map(informeTecnico => {
            const solicitudUrl = `${API_URL}/solicitud/${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.SolicitudAutorizacion.IdSolicitud}`;
            return fetch(solicitudUrl, {
                method: 'GET',
                headers: { 'Authorization': `Bearer ${token}` }
            })
            .then(response => response.json())
            .then(solicitudData => ({
                informeTecnico,
                solicitudData
            }))
            .catch(error => console.error('Error fetching solicitud data:', error));
        }));
        
    })
    .then(informeTecnicoDetails => {
        informeTecnicoDetails.forEach(({ informeTecnico, solicitudData }) => {
            const div = document.createElement('div');
            div.className = 'proyecto';
            const nroExpediente = solicitudData.NroExpediente ? String(solicitudData.NroExpediente).trim() : '';
            div.setAttribute("data-name", nroExpediente);
            div.innerHTML = `
                <p>Cliente: <span>${solicitudData.Cliente01.Nombre} ${solicitudData.Cliente01.Apellido}</span></p>
                <p>Nro Expediente: <span>${solicitudData.NroExpediente}</span></p>
                <p>Agrimensor: <span>${solicitudData.Agrimensor.Nombre} ${solicitudData.Agrimensor.Apellido}</span></p>
                <p>Notario: <span>${solicitudData.Notario.Nombre} ${solicitudData.Notario.Apellido}</span></p>
                <div>
                    <a href="/tercera_etapa_detallada/?id=${informeTecnico.IdInformeTecnico}" class="view-link" style="display:none">Ver</a>
                    <div>
                    <a href="${informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.EnlaceProrroga}">Prórroga</a>
                    </div>
                </div>
            `;
            informesTecnicosTable.appendChild(div);
        });
        
        const searchInput = document.getElementById('search-input');
        const items = informesTecnicosTable.getElementsByClassName('proyecto');

        searchInput.addEventListener('input', function() {
            const query = searchInput.value.trim().toLowerCase();
            
            for (let item of items) {
                const itemName = item.getAttribute('data-name') ? item.getAttribute('data-name').trim().toLowerCase() : '';
                
                if (itemName.includes(query)) {
                    item.classList.remove('hidden');
                } else {
                    item.classList.add('hidden');
                }
            }
        });
    })
    .catch(error => {
        document.getElementById('error-message').innerText = 'Error fetching informes técnicos: ' + error.message;
        console.error("Error fetching informes técnicos:", error);
    });

    fetch(avisosColindantesApiUrl, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => response.json())
    .then(data => {
        const filteredAvisosColindantes = data.filter(avisoColindante => avisoColindante.Estatus === 1);

        filteredAvisosColindantes.forEach(avisoColindante => {
            const div = document.createElement('div');
            div.className = 'proyecto';
            const nroExpediente = avisoColindante.SolicitudAutorizacion.NroExpediente ? String(avisoColindante.SolicitudAutorizacion.NroExpediente).trim() : '';
            div.setAttribute("data-name", nroExpediente);
            
            div.innerHTML = `
                <p>Cliente: <span>${avisoColindante.SolicitudAutorizacion.Cliente01.Nombre} ${avisoColindante.SolicitudAutorizacion.Cliente01.Apellido}</span></p>
                <p>Nro Expediente: <span>${avisoColindante.SolicitudAutorizacion.NroExpediente}</span></p>
                <p>Agrimensor: <span>${avisoColindante.SolicitudAutorizacion.Agrimensor.Nombre} ${avisoColindante.SolicitudAutorizacion.Agrimensor.Apellido}</span></p>
                <p>Notario: <span>${avisoColindante.SolicitudAutorizacion.Notario.Nombre} ${avisoColindante.SolicitudAutorizacion.Notario.Apellido}</span></p>
                <div>
                <a href="${avisoColindante.EnlaceProrroga}">Prórroga</a>
                </div>
            `;
            informesTecnicosTable.appendChild(div);
        });
    })
    .catch(error => {
        document.getElementById('error-message').innerText = 'Error fetching avisos colindantes: ' + error.message;
        console.error("Error fetching avisos colindantes:", error);
    });



    if (logoutButton) {
        logoutButton.addEventListener('click', function() {
            localStorage.removeItem('token');
            window.location.href = '/login/';
        });
    }

    function checkAuth() {
        const token = localStorage.getItem('token');
        if (!token) {
            if (!window.location.pathname.endsWith('/login/')) {
                window.location.href = '/login/';
            }
        } else {
            if (window.location.pathname.endsWith('/login/')) {
                window.location.href = '/tercera_etapa/';
            }
        }
    }

    checkAuth();
});
