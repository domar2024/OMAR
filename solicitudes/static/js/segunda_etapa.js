console.log(API_URL)
document.addEventListener('DOMContentLoaded', function() {
    const avisomensurasTable = document.getElementById('avisomensuras-table');
    const logoutButton = document.getElementById('logout');

    if (!localStorage.getItem('token')) {
        document.getElementById('error-message').innerText = 'You must be logged in to view this page';
        window.location.href = '/login/';
        return;
    }

    const token = localStorage.getItem('token');
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

    // Cargar lista de avisos colindantes
    fetch(avisosColindantesApiUrl, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })

    .then(response => response.json())
    .then(data => {
        const filteredData = data.filter(avisoColindante => avisoColindante.Estatus === 1); // Añadir filtro por estatus
        filteredData.forEach((avisoColindante) => {
            const div = document.createElement('div');
            div.className = 'proyecto';
            const nroExpediente = avisoColindante.SolicitudAutorizacion.NroExpediente ? String(avisoColindante.SolicitudAutorizacion.NroExpediente).trim() : '';
            div.setAttribute("data-name", nroExpediente);

            checked_mensura_class = ""
            checked_periodico_class = ""
            checked_colindante_class = ""

            if(avisoColindante.checkMensura){
                checked_mensura_class = 'class="checked_doc"'
            }

            if(avisoColindante.checkPeriodico){
                checked_periodico_class = 'class="checked_doc"'
            }

            if(avisoColindante.checkColindantes){
                checked_colindante_class = 'class="checked_doc"'
            }

            div.innerHTML = `
                <p>Cliente: <span>${avisoColindante.SolicitudAutorizacion.Cliente01.Nombre} ${avisoColindante.SolicitudAutorizacion.Cliente01.Apellido}</span></p>
                <p>Nro Expediente: <span>${avisoColindante.SolicitudAutorizacion.NroExpediente}</span></p>
                <p>Agrimensor: <span>${avisoColindante.SolicitudAutorizacion.Agrimensor.Nombre} ${avisoColindante.SolicitudAutorizacion.Agrimensor.Apellido}</span></p>
                <p>Notario: <span>${avisoColindante.SolicitudAutorizacion.Notario.Nombre} ${avisoColindante.SolicitudAutorizacion.Notario.Apellido}</span></p>
                <div>
                    <div>
                        <p style="text-decoration: none !important;">${calcularDiasRestantes(avisoColindante.FechaVencimiento)} días</p>
                        <a href="/segunda_etapa_detallada/?id=${avisoColindante.IdAvisoColindantes}" class="view-link">Ver</a>
                    </div>
                    <div>
                        <a href="${avisoColindante.AvisoMensura.Enlace}" ${checked_mensura_class}>Mensura</a>
                        <a href="${avisoColindante.AvisoPeriodico.Enlace}" ${checked_periodico_class}>Periódico</a>
                        <a href="${avisoColindante.Enlace}" ${checked_colindante_class}>Colindante</a>
                    </div>
                </div>
            `;
            avisomensurasTable.appendChild(div);
        });
        
        const searchInput = document.getElementById('search-input');
        const items = avisomensurasTable.getElementsByClassName('proyecto');

        searchInput.addEventListener('input', function() {
            const query = searchInput.value.trim().toLowerCase();
            console.log('Search query:', query); 
            
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
                window.location.href = '/segunda_etapa/';
            }
        }
    }

    checkAuth();
});
