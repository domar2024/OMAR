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

            checked_carta_class = ""
            checked_declaracion_class = ""
            checked_informe_class = ""

            if(informeTecnico.checkCarta){
                checked_carta_class = 'class="checked_doc"'
            }

            if(informeTecnico.checkDeclaracion){
                checked_declaracion_class = 'class="checked_doc"'
            }

            if(informeTecnico.checkInforme ){
                checked_informe_class = 'class="checked_doc"'
            }
 

            div.innerHTML = `
                <p>Cliente: <span>${solicitudData.Cliente01.Nombre} ${solicitudData.Cliente01.Apellido}</span></p>
                <p>Nro Expediente: <span>${solicitudData.NroExpediente}</span></p>
                <p>Agrimensor: <span>${solicitudData.Agrimensor.Nombre} ${solicitudData.Agrimensor.Apellido}</span></p>
                <p>Notario: <span>${solicitudData.Notario.Nombre} ${solicitudData.Notario.Apellido}</span></p>
                <div>
                    <div>
                        <p style="text-decoration: none !important;">${calcularDiasRestantes(informeTecnico.DeclaracionPosesion.CartaConformidad.AvisoColindantes.FechaVencimiento)} días</p>
                        <a href="/tercera_etapa_detallada/?id=${informeTecnico.IdInformeTecnico}" class="view-link">Ver</a>
                    </div>
                    <div>
                        <a href="${informeTecnico.DeclaracionPosesion.CartaConformidad.Enlace}" ${checked_carta_class}>Carta Conformidad</a>
                        <a href="${informeTecnico.DeclaracionPosesion.Enlace}"  ${checked_declaracion_class}>Declaración Posesión</a>
                        <a href="${informeTecnico.Enlace}"  ${checked_informe_class}>Informe Tecnico</a>
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
