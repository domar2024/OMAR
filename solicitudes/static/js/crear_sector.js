console.log(API_URL)
document.addEventListener('DOMContentLoaded', function() {
    const sectoresForm = document.getElementById('sectores-form');
    const sectoresTable = document.getElementById('sectores-table');
    const logoutButton = document.getElementById('logout');
    const deleteButtonDesplegar = document.getElementById('delete-btn');
    const deleteButtonTotal = document.getElementById('delete-button-total');
    const salirVentanaButton = document.getElementById('boton-salir-ventana');
    const clearButton = document.getElementById('clear-btn');
    const paisSelect = document.getElementById('pais');
    const provinciaSelect = document.getElementById('provincia');
    const municipioSelect = document.getElementById('municipio');
    ventana_confirmar = document.getElementById("ventana_confirmar");

    if (!localStorage.getItem('token')) {
        document.getElementById('error-message').innerText = 'You must be logged in to view this page';
        window.location.href = '/login/';
        return;
    }

    const token = localStorage.getItem('token');
    const sectoresApiUrl = API_URL + '/sectores';
    const sectorApiUrl = API_URL + '/sector';

    //Eliminar notificacion
    function dezplegar_ventana_eliminar(){
        ventana_confirmar = document.getElementById("ventana_confirmar");
        ventana_confirmar.style.display = "flex";
    }

    function ocultar_ventana_eliminar(){
        ventana_confirmar = document.getElementById("ventana_confirmar");
        ventana_confirmar.style.display = "none";
    }


    let sectoresData = [];

    // Cargar lista de sectores y filtrar paises
    fetch(sectoresApiUrl, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch sectors');
        }
        return response.json();
    })
    .then(data => {
        sectoresData = data.filter(sector => sector.Estatus === 1);  // Filtrar los sectores con Estatus 1

        // Filtrar países únicos
        const paisesUnicos = [...new Set(sectoresData.map(sector => sector.Pais))];
        paisesUnicos.forEach(pais => {
            const option = document.createElement('option');
            option.value = pais;
            option.textContent = pais;
            paisSelect.appendChild(option);
        });

        const paisSeleccionado = "Republica Dominicana";
        paisSelect.value = paisSeleccionado;
        paisSelect.disabled = true;

        // Event listener para seleccionar un país y cargar provincias
        //paisSelect.addEventListener('change', function() {
        //    const paisSeleccionado = paisSelect.value;
            provinciaSelect.innerHTML = '<option value="">Seleccione una provincia</option>'; // Limpiar provincias
            municipioSelect.innerHTML = '<option value="">Seleccione un municipio</option>'; // Limpiar municipios

            const provinciasUnicas = [...new Set(sectoresData
                .filter(s => s.Pais === paisSeleccionado)
                .map(s => s.Provincia))];

            provinciasUnicas.forEach(provincia => {
                const option = document.createElement('option');
                option.value = provincia;
                option.textContent = provincia;
                provinciaSelect.appendChild(option);
            });
        //});

        // Event listener para seleccionar una provincia y cargar municipios
        provinciaSelect.addEventListener('change', function() {
            const paisSeleccionado = paisSelect.value;
            const provinciaSeleccionada = provinciaSelect.value;
            municipioSelect.innerHTML = '<option value="">Seleccione un municipio</option>'; // Limpiar municipios

            const municipiosUnicos = [...new Set(sectoresData
                .filter(s => s.Pais === paisSeleccionado && s.Provincia === provinciaSeleccionada)
                .map(s => s.Municipio))];

            municipiosUnicos.forEach(municipio => {
                const option = document.createElement('option');
                option.value = municipio;
                option.textContent = municipio;
                municipioSelect.appendChild(option);
            });
        });

        // Resto del código original para cargar y manejar los sectores en la tabla

        const button = document.createElement('button');
                button.type = 'button';
                button.innerHTML = `
                    <p>Sector</p>
                    <p>Municipio</p>
                    <p>Provincia</p>
                `;
        sectoresTable.appendChild(button);

        sectoresData.forEach(sector => {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'edit-btn';
            button.dataset.id = sector.IdSector;
            button.innerHTML = `
                <p>${sector.Sector}</p>
                <p>${sector.Municipio}</p>
                <p>${sector.Provincia}</p>
            `;
            sectoresTable.appendChild(button);
        });

        // Agregar event listeners a los botones de edición
        const editButtons = document.querySelectorAll('.edit-btn');
        editButtons.forEach(button => {
            button.addEventListener('click', function() {
                const sectorId = this.getAttribute('data-id');
                const sector = sectoresData.find(s => s.IdSector == sectorId);

                if (sector) {
                    document.getElementById('sector').value = sector.Sector;
                    document.getElementById('estatus').value = sector.Estatus;
                    document.getElementById('pais').value = sector.Pais;

                    const result = `a el sector ${sector.Sector}`;
                    console.log(result);
                    document.getElementById('span-resto-mensaje-confirmacion').textContent = result;

                    document.querySelector('.boton_normal[type="submit"]').innerText = 'Actualizar';
                    document.getElementById('delete-btn').style.display = 'inline-block'; // Mostrar el botón de eliminar

                    // Rellenar provincias basadas en el país seleccionado
                    const provinciasUnicas = [...new Set(sectoresData
                        .filter(s => s.Pais === sector.Pais)
                        .map(s => s.Provincia))];
                    
                    provinciaSelect.innerHTML = '<option value="">Seleccione una provincia</option>'; // Limpiar provincias
                    provinciasUnicas.forEach(provincia => {
                        const option = document.createElement('option');
                        option.value = provincia;
                        option.textContent = provincia;
                        provinciaSelect.appendChild(option);
                    });
                    
                    // Seleccionar la provincia guardada
                    provinciaSelect.value = sector.Provincia;

                    // Rellenar municipios basados en la provincia seleccionada
                    const municipiosUnicos = [...new Set(sectoresData
                        .filter(s => s.Pais === sector.Pais && s.Provincia === sector.Provincia)
                        .map(s => s.Municipio))];

                    municipioSelect.innerHTML = '<option value="">Seleccione un municipio</option>'; // Limpiar municipios
                    municipiosUnicos.forEach(municipio => {
                        const option = document.createElement('option');
                        option.value = municipio;
                        option.textContent = municipio;
                        municipioSelect.appendChild(option);
                    });

                    // Seleccionar el municipio guardado
                    municipioSelect.value = sector.Municipio;

                    // Establecer el ID del sector en el formulario para editar
                    sectoresForm.setAttribute('data-sector-id', sector.IdSector);
                }
            });
        });
    })
    .catch(error => {
        document.getElementById('error-message').innerText = 'Error fetching sectors: ' + error.message;
        console.error("Error fetching sectors:", error);
    });
    // Manejar la creación o edición de un sector
    sectoresForm.addEventListener('submit', async function(event) {
        event.preventDefault();

        const sectorId = sectoresForm.getAttribute('data-sector-id');
        const method = sectorId ? 'PUT' : 'POST';
        const apiUrl = sectorId ? `${sectorApiUrl}/${sectorId}` : sectorApiUrl;

        const sector = document.getElementById('sector').value;
        const municipio = document.getElementById('municipio').value;
        const provincia = document.getElementById('provincia').value;
        const pais = document.getElementById('pais').value;
        const estatus = parseInt(document.getElementById('estatus').value);

        const datosSector = {
            Sector: sector,
            Municipio: municipio,
            Provincia: provincia,
            Pais: pais,
            Estatus: estatus
        };

        try {
            const response = await fetch(apiUrl, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(datosSector)
            });

            const responseBody = await response.text();
            console.log('Response body:', responseBody);

            let result;
            try {
                result = JSON.parse(responseBody);
            } catch (e) {
                throw new Error('Invalid JSON response: ' + responseBody);
            }

            if (!response.ok) {
                throw new Error(result.message || 'Error saving sector');
            }

            document.getElementById('success-message').innerText = 'Sector guardado exitosamente';

            const successMessage = sectorId ? 'Sector actualizado exitosamente' : 'Sector creado exitosamente';
            const successMessageElement = document.getElementById('success-message');
            successMessageElement.innerText = successMessage;

            setTimeout(() => {
                successMessageElement.innerText = '';
            }, 3000);

            if (!sectorId) {
                const button = document.createElement('button');
                button.type = 'button';
                button.className = 'edit-btn';
                button.dataset.id = result.IdSector;
                button.innerHTML = `
                    <p>${result.Sector}</p>
                    <p>${result.Municipio}</p>
                    <p>${result.Provincia}</p>
                `;
                sectoresTable.appendChild(button);
                addEditButtonEvent(button);
            } else {
                const buttonToUpdate = document.querySelector(`button[data-id="${sectorId}"]`);
                const newButton = document.createElement('button');
                newButton.type = 'button';
                newButton.className = 'edit-btn';
                newButton.dataset.id = result.IdSector;

                const sectorP = document.createElement('p');
                sectorP.textContent = result.Sector;
                const ciudadP = document.createElement('p');
                ciudadP.textContent = result.Ciudad;
                const municipioP = document.createElement('p');
                municipioP.textContent = result.Municipio;
                const provinciaP = document.createElement('p');
                provinciaP.textContent = result.Provincia;
                const paisP = document.createElement('p');
                paisP.textContent = result.Pais;
                newButton.appendChild(sectorP);
                newButton.appendChild(municipioP);

                buttonToUpdate.replaceWith(newButton);
                addEditButtonEvent(newButton);
            }
        } catch (error) {
            document.getElementById('error-message').innerText = error.message;
            console.error("Error saving sector:", error);
        }
    });

    deleteButtonDesplegar.addEventListener('click', dezplegar_ventana_eliminar);
    salirVentanaButton.addEventListener('click', ocultar_ventana_eliminar);

    // Manejar la eliminación de un sector
    deleteButtonTotal.addEventListener('click', async function() {
        const sectorId = sectoresForm.getAttribute('data-sector-id');
        if (!sectorId) {
            document.getElementById('error-message').innerText = 'No sector selected for deletion';
            return;
        }

        try {
            const response = await fetch(`${sectorApiUrl}/${sectorId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error('Failed to delete sector');
            }

            const successMessageElement = document.getElementById('success-message');
            successMessageElement.innerText = 'Sector eliminado exitosamente';

            setTimeout(() => {
                successMessageElement.innerText = '';
                location.reload(); // Recargar la página después de que el mensaje desaparezca
            }, 3000);

            document.getElementById('sector').value = '';
            document.getElementById('municipio').value = '';
            document.getElementById('provincia').value = '';
            //document.getElementById('pais').value = '';
            document.getElementById('estatus').value = '1'; // restablece estatus a 1

            // Cambiar el texto del botón de guardar y ocultar el botón de eliminar
            document.querySelector('.boton_normal[type="submit"]').innerText = 'Guardar';
            document.getElementById('delete-btn').style.display = 'none';

        } catch (error) {
            document.getElementById('error-message').innerText = 'Error deleting sector: ' + error.message;
            console.error("Error deleting sector:", error);
        }
    });

    // Manejar el vaciado del formulario para crear un nuevo sector
    clearButton.addEventListener('click', function() {
        // Limpiar todos los campos del formulario
        document.getElementById('sector').value = '';
        document.getElementById('municipio').value = '';
        document.getElementById('provincia').value = '';
        //document.getElementById('pais').value = '';
        document.getElementById('estatus').value = '1'; // restablece estatus a 1

        document.querySelector('.boton_normal[type="submit"]').innerText = 'Guardar';
        document.getElementById('delete-btn').style.display = 'none'; // Ocultar el botón de eliminar

        // Eliminar el atributo data-sector-id para que el formulario se considere en modo "crear"
        sectoresForm.removeAttribute('data-sector-id');

        // Borrar mensajes de éxito/error si existen
        document.getElementById('error-message').innerText = '';
        document.getElementById('success-message').innerText = '';
    });

    function addEditButtonEvent(button) {
        button.addEventListener('click', function() {
            const sectorId = this.getAttribute('data-id');
            const sector = sectoresData.find(s => s.IdSector == sectorId);

            if (sector) {
                document.getElementById('sector').value = sector.Sector;
                document.getElementById('estatus').value = sector.Estatus;
                document.getElementById('pais').value = sector.Pais;

                document.querySelector('.boton_normal[type="submit"]').innerText = 'Actualizar';
                document.getElementById('delete-btn').style.display = 'inline-block'; // Mostrar el botón de eliminar

                // Rellenar provincias basadas en el país seleccionado
                const provinciasUnicas = [...new Set(sectoresData
                    .filter(s => s.Pais === sector.Pais)
                    .map(s => s.Provincia))];
                
                provinciaSelect.innerHTML = '<option value="">Seleccione una provincia</option>'; // Limpiar provincias
                provinciasUnicas.forEach(provincia => {
                    const option = document.createElement('option');
                    option.value = provincia;
                    option.textContent = provincia;
                    provinciaSelect.appendChild(option);
                });
                
                // Seleccionar la provincia guardada
                provinciaSelect.value = sector.Provincia;

                // Rellenar municipios basados en la provincia seleccionada
                const municipiosUnicos = [...new Set(sectoresData
                    .filter(s => s.Pais === sector.Pais && s.Provincia === sector.Provincia)
                    .map(s => s.Municipio))];

                municipioSelect.innerHTML = '<option value="">Seleccione un municipio</option>'; // Limpiar municipios
                municipiosUnicos.forEach(municipio => {
                    const option = document.createElement('option');
                    option.value = municipio;
                    option.textContent = municipio;
                    municipioSelect.appendChild(option);
                });

                // Seleccionar el municipio guardado
                municipioSelect.value = sector.Municipio;

                // Establecer el ID del sector en el formulario para editar
                sectoresForm.setAttribute('data-sector-id', sector.IdSector);
            }
        });
    }


    const searchInput = document.getElementById('search-input');
    const itemList = document.getElementById('sectores-table');
    const items = itemList.getElementsByTagName('button');

    searchInput.addEventListener('input', function() {
        const query = searchInput.value.toLowerCase();

        for (let i = 1; i < items.length; i++) { // Comenzar el bucle desde el segundo botón
            const item = items[i];
            const firstP = item.getElementsByTagName('p')[0];
            const itemName = firstP ? firstP.textContent.toLowerCase() : '';

            if (itemName.includes(query)) {
                item.classList.remove('hidden');
            } else {
                item.classList.add('hidden');
            }
        }
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
                window.location.href = '/sector/';
            }
        }
    }

    checkAuth();
});
