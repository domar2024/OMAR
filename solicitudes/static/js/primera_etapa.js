console.log(API_URL)
document.addEventListener('DOMContentLoaded', function() {
    const solicitudesTable = document.getElementById('solicitudes-table');
    const logoutButton = document.getElementById('logout');

    if (!localStorage.getItem('token')) {
        document.getElementById('error-message').innerText = 'No está logueado';
        window.location.href = '/login/';
        return;
    }

    const token = localStorage.getItem('token');
    const solicitudesApiUrl = API_URL + '/solicitudes';

    // Cargar lista de solicitudes
    fetch(solicitudesApiUrl, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => response.json())
    .then(data => {
        data.filter(solicitud => solicitud.Estatus === 1).forEach(solicitud => {
            const div = document.createElement('div');
            div.classList.add('solicitud-item', 'proyecto');
            
            // Convertir NroExpediente a string y aplicar trim
            const nombreCliente = solicitud.Cliente01.Nombre ? String(solicitud.Cliente01.Nombre).trim() : '';
            div.setAttribute("data-name", nombreCliente);
            
            NroExpediente = solicitud.NroExpediente
            if (NroExpediente == 0){
                NroExpediente = ""
            }

            checked_solicitud_class = ""


            if(solicitud.checkSolicitud){
                checked_solicitud_class = 'class="checked_doc"'
            }


            div.innerHTML = `
                <p>Cliente: <span>${solicitud.Cliente01.Nombre} ${solicitud.Cliente01.Apellido}</span></p>
                <p>Nro Expediente: <span>${NroExpediente}</span></p>
                <p>Agrimensor: <span>${solicitud.Agrimensor.Nombre} ${solicitud.Agrimensor.Apellido}</span></p>
                <p>Notario: <span>${solicitud.Notario.Nombre} ${solicitud.Notario.Apellido}</span></p>
                <div>
                <a href="/primera_etapa_detallada/?id=${solicitud.IdSolicitud}" class="view-link">Ver</a>
                <div><a href="${solicitud.Enlace}" ${checked_solicitud_class}>Documento</a></div>
                </div>
                `;
            solicitudesTable.appendChild(div);
        });

        const searchInput = document.getElementById('search-input');
        const items = solicitudesTable.getElementsByClassName('proyecto');

        searchInput.addEventListener('input', function() {
            const query = searchInput.value.trim().toLowerCase();
            console.log('Search query:', query); // Verificar la entrada del usuario
            
            for (let item of items) {
                const itemName = item.getAttribute('data-name') ? item.getAttribute('data-name').trim().toLowerCase() : '';
                //console.log('Comparing with data-name:', itemName); // Verificar data-name

                if (itemName.includes(query)) {
                    //console.log(`Match found: ${itemName}`); // Log cuando hay una coincidencia
                    item.classList.remove('hidden');
                } else {
                    //console.log(`No match: ${itemName}`); // Log cuando no hay coincidencia
                    item.classList.add('hidden');
                }
            }
        });
    })
    .catch(error => {
        document.getElementById('error-message').innerText = 'Error fetching solicitudes: ' + error.message;
        console.error("Error fetching solicitudes:", error);
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
                window.location.href = '/primera_etapa/';
            }
        }
    }

    checkAuth();
});
