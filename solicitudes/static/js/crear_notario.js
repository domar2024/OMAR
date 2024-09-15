console.log(API_URL)
document.addEventListener('DOMContentLoaded', function() {
    const notariosForm = document.getElementById('notarios-form');
    const notariosTable = document.getElementById('notarios-table');
    const logoutButton = document.getElementById('logout');
    const deleteButtonDesplegar = document.getElementById('delete-btn');
    const deleteButtonTotal = document.getElementById('delete-button-total');
    const salirVentanaButton = document.getElementById('boton-salir-ventana');
    const clearButton = document.getElementById('clear-btn');
    const paisSelect = document.getElementById('pais');
    const provinciaSelect = document.getElementById('provincia');
    const municipioSelect = document.getElementById('municipio');
    const idSectorSelect = document.getElementById('idSector');
    ventana_confirmar = document.getElementById("ventana_confirmar");

    if (!localStorage.getItem('token')) {
        document.getElementById('error-message').innerText = 'You must be logged in to view this page';
        window.location.href = '/login/';
        return;
    }

    const token = localStorage.getItem('token');
    const sectoresApiUrl = API_URL + '/sectores';
    const notariosApiUrl = API_URL + '/notarios';
    const notarioApiUrl = API_URL + '/notario';
    const sexos = [
        { letra: 'M', nombre: 'Masculino' },
        { letra: 'F', nombre: 'Femenino' }
    ];

    // Cargar lista de sexos
    const SexoSelect = document.getElementById('sexo');
    sexos.forEach(sexo => {
        const option = document.createElement('option');
        option.value = sexo.letra;
        option.text = sexo.nombre;
        SexoSelect.appendChild(option);
    });

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
    .then(response => response.json())
    .then(data => {
        sectoresData = data.filter(sector => sector.Estatus === 1);  // Filtrar sectores con Estatus 1

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

            provinciaSelect.innerHTML = '<option value="">Seleccione una provincia</option>'; // Limpiar provincias
            municipioSelect.innerHTML = '<option value="">Seleccione un municipio</option>'; // Limpiar municipios
            idSectorSelect.innerHTML = '<option value="">Seleccione un sector</option>'; // Limpiar sectores

            const provinciasUnicas = [...new Set(sectoresData
                .filter(s => s.Pais === paisSeleccionado)
                .map(s => s.Provincia))];

            provinciasUnicas.forEach(provincia => {
                const option = document.createElement('option');
                option.value = provincia;
                option.textContent = provincia;
                provinciaSelect.appendChild(option);
            });

        // Event listener para seleccionar una provincia y cargar municipios
        provinciaSelect.addEventListener('change', function() {
            const paisSeleccionado = paisSelect.value;
            const provinciaSeleccionada = provinciaSelect.value;
            municipioSelect.innerHTML = '<option value="">Seleccione un municipio</option>'; // Limpiar municipios
            idSectorSelect.innerHTML = '<option value="">Seleccione un sector</option>'; // Limpiar sectores

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

        // Event listener para seleccionar un municipio y cargar sectores
        municipioSelect.addEventListener('change', function() {
            const paisSeleccionado = paisSelect.value;
            const provinciaSeleccionada = provinciaSelect.value;
            const municipioSeleccionado = municipioSelect.value;
            idSectorSelect.innerHTML = '<option value="">Seleccione un sector</option>'; // Limpiar sectores

            const sectoresFiltrados = sectoresData
                .filter(s => s.Pais === paisSeleccionado && s.Provincia === provinciaSeleccionada && s.Municipio === municipioSeleccionado);

            sectoresFiltrados.forEach(sector => {
                const option = document.createElement('option');
                option.value = sector.IdSector;
                option.textContent = sector.Sector;
                idSectorSelect.appendChild(option);
            });
        });

        // Cargar notarios y mostrar solo aquellos con Estatus 1
        fetch(notariosApiUrl, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => response.json())
        .then(notarios => {
            const notariosFiltrados = notarios.filter(notario => notario.Estatus === 1);

            const button = document.createElement('button');
                button.type = 'button';
                button.innerHTML = `
                    <p>Nombres</p>
                    <p>Apellidos</p>
                    <p>Nro. Colegiatura</p>
                `;
            notariosTable.appendChild(button);
            

            notariosFiltrados.forEach(notario => {
                const button = document.createElement('button');
                button.type = 'button';
                button.className = 'edit-btn';
                button.dataset.id = notario.IdNotario;
                button.innerHTML = `
                    <p>${notario.Nombre}</p>
                    <p>${notario.Apellido}</p>
                    <p>${notario.NroColegiatura}</p>
                `;
                notariosTable.appendChild(button);
            });

            // Agregar event listeners a los botones de edición
            const editButtons = document.querySelectorAll('.edit-btn');
            editButtons.forEach(button => {
                button.addEventListener('click', function() {
                    const notarioId = this.getAttribute('data-id');
                    const notario = notariosFiltrados.find(n => n.IdNotario == notarioId);

                    if (notario) {
                        document.getElementById('nombre').value = notario.Nombre;
                        document.getElementById('apellido').value = notario.Apellido;
                        document.getElementById('sexo').value = notario.Sexo;
                        document.getElementById('nroColegiatura').value = notario.NroColegiatura;
                        document.getElementById('estatus').value = notario.Estatus;

                        const result = `a el notario ${notario.Nombre} ${notario.Apellido}`;
                        console.log(result);
                        document.getElementById('span-resto-mensaje-confirmacion').textContent = result;

                        document.querySelector('.boton_normal[type="submit"]').innerText = 'Actualizar';
                        document.getElementById('delete-btn').style.display = 'inline-block'; // Mostrar el botón de eliminar

                        // Rellenar los selectores de país, provincia y municipio con los valores actuales del notario
                        const sectorSeleccionado = sectoresData.find(s => s.IdSector == notario.IdSector);
                        const paisSeleccionado = sectorSeleccionado.Pais;
                        const provinciaSeleccionada = sectorSeleccionado.Provincia;
                        const municipioSeleccionado = sectorSeleccionado.Municipio;

                        document.getElementById('pais').value = paisSeleccionado;

                        // Rellenar provincias basadas en el país seleccionado
                        const provinciasUnicas = [...new Set(sectoresData
                            .filter(s => s.Pais === paisSeleccionado)
                            .map(s => s.Provincia))];
                        
                        provinciaSelect.innerHTML = '<option value="">Seleccione una provincia</option>'; // Limpiar provincias
                        provinciasUnicas.forEach(provincia => {
                            const option = document.createElement('option');
                            option.value = provincia;
                            option.textContent = provincia;
                            provinciaSelect.appendChild(option);
                        });

                        document.getElementById('provincia').value = provinciaSeleccionada;

                        // Rellenar municipios basados en la provincia seleccionada
                        const municipiosUnicos = [...new Set(sectoresData
                            .filter(s => s.Pais === paisSeleccionado && s.Provincia === provinciaSeleccionada)
                            .map(s => s.Municipio))];

                        municipioSelect.innerHTML = '<option value="">Seleccione un municipio</option>'; // Limpiar municipios
                        municipiosUnicos.forEach(municipio => {
                            const option = document.createElement('option');
                            option.value = municipio;
                            option.textContent = municipio;
                            municipioSelect.appendChild(option);
                        });

                        document.getElementById('municipio').value = municipioSeleccionado;

                        // Rellenar sectores basados en el municipio seleccionado
                        const sectoresFiltrados = sectoresData
                            .filter(s => s.Pais === paisSeleccionado && s.Provincia === provinciaSeleccionada && s.Municipio === municipioSeleccionado);

                        idSectorSelect.innerHTML = '<option value="">Seleccione un sector</option>'; // Limpiar sectores
                        sectoresFiltrados.forEach(sector => {
                            const option = document.createElement('option');
                            option.value = sector.IdSector;
                            option.textContent = sector.Sector;
                            idSectorSelect.appendChild(option);
                        });

                        // Seleccionar el sector guardado
                        idSectorSelect.value = notario.IdSector;

                        // Establecer el ID del notario en el formulario para editar
                        notariosForm.setAttribute('data-notario-id', notario.IdNotario);
                    }
                });
            });
        })
        .catch(error => {
            document.getElementById('error-message').innerText = 'Error fetching notaries: ' + error.message;
            console.error("Error fetching notaries:", error);
        });
    })
    .catch(error => {
        document.getElementById('error-message').innerText = 'Error fetching sectors: ' + error.message;
        console.error("Error fetching sectors:", error);
    });

    // Manejar la creación o edición de un notario
    notariosForm.addEventListener('submit', async function(event) {
        event.preventDefault();

        const notarioId = notariosForm.getAttribute('data-notario-id');
        const method = notarioId ? 'PUT' : 'POST';
        const apiUrl = notarioId ? `${notarioApiUrl}/${notarioId}` : notarioApiUrl;

        const nombre = document.getElementById('nombre').value;
        const apellido = document.getElementById('apellido').value;
        const idSector = parseInt(document.getElementById('idSector').value);
        const nroColegiatura = document.getElementById('nroColegiatura').value;
        const sexo = document.getElementById('sexo').value;
        const estatus = parseInt(document.getElementById('estatus').value);

        if (sexo !== 'M' && sexo !== 'F') {
            document.getElementById('error-message').innerText = 'Invalid sector selected';
            return;
        }

        const datosNotario = {
            Nombre: nombre,
            Apellido: apellido,
            Sexo: sexo,
            IdSector: idSector,
            NroColegiatura: nroColegiatura,
            Estatus: estatus
        };

        try {
            const response = await fetch(apiUrl, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(datosNotario)
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
                throw new Error(result.message || 'Error saving notary');
            }

            const successMessage = notarioId ? 'Notario actualizado exitosamente' : 'Notario creado exitosamente';
            const successMessageElement = document.getElementById('success-message');
            successMessageElement.innerText = successMessage;

            setTimeout(() => {
                successMessageElement.innerText = '';
            }, 3000);
    

            if (!notarioId) {
                const button = document.createElement('button');
                button.type = 'button';
                button.className = 'edit-btn';
                button.dataset.id = result.IdNotario;
                button.innerHTML = `
                    <p>${result.Nombre}</p>
                    <p>${result.Apellido}</p>
                    <p>${result.NroColegiatura}</p>
                `;
                notariosTable.appendChild(button);
                addEditButtonEvent(button);
            } else {
                // Actualizar la fila existente en la tabla
                const buttonToUpdate = document.querySelector(`button[data-id="${notarioId}"]`);
                const newButton = document.createElement('button');
                newButton.type = 'button';
                newButton.className = 'edit-btn';
                newButton.dataset.id = result.IdNotario;
                newButton.innerHTML = `
                    <p>${result.Nombre}</p>
                    <p>${result.Apellido}</p>
                    <p>${result.NroColegiatura}</p>
                `;
                buttonToUpdate.replaceWith(newButton);
                addEditButtonEvent(newButton);
            }
        } catch (error) {
            document.getElementById('error-message').innerText = error.message;
            console.error("Error saving notary:", error);
        }
    });

    deleteButtonDesplegar.addEventListener('click', dezplegar_ventana_eliminar);
    salirVentanaButton.addEventListener('click', ocultar_ventana_eliminar);

    // Manejar la eliminación de un notario
    deleteButtonTotal.addEventListener('click', async function() {
        const notarioId = notariosForm.getAttribute('data-notario-id');
        if (!notarioId) {
            document.getElementById('error-message').innerText = 'No notary selected for deletion';
            return;
        }

        try {
            const response = await fetch(`${notarioApiUrl}/${notarioId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error('Failed to delete notary');
            }

            const successMessageElement = document.getElementById('success-message');
            successMessageElement.innerText = 'Notario eliminado exitosamente';
    
            ocultar_ventana_eliminar();
            
            setTimeout(() => {
                successMessageElement.innerText = '';
                location.reload(); // Recargar la página después de que el mensaje desaparezca
            }, 3000);

            document.getElementById('nombre').value = '';
            document.getElementById('apellido').value = '';
            document.getElementById('sexo').value = '';
            document.getElementById('idSector').value = '';
            document.getElementById('nroColegiatura').value = '';
            document.getElementById('estatus').value = '1'; // restablece estatus a 1

            //document.getElementById('pais').value = '';
            document.getElementById('provincia').innerHTML = '<option value="">Seleccione una provincia</option>';
            document.getElementById('municipio').innerHTML = '<option value="">Seleccione un municipio</option>';
            document.getElementById('idSector').innerHTML = '<option value="">Seleccione un sector</option>';

            document.querySelector('.boton_normal[type="submit"]').innerText = 'Guardar';
            document.getElementById('delete-btn').style.display = 'none';

        } catch (error) {
            document.getElementById('error-message').innerText = 'Error deleting notary: ' + error.message;
            console.error("Error deleting notary:", error);
        }
    });

    // Manejar el vaciado del formulario para crear un nuevo notario
    clearButton.addEventListener('click', function() {
        // Limpiar todos los campos del formulario
        document.getElementById('nombre').value = '';
        document.getElementById('apellido').value = '';
        document.getElementById('sexo').value = '';
        document.getElementById('idSector').value = '';
        document.getElementById('nroColegiatura').value = '';
        document.getElementById('estatus').value = '1'; // restablece estatus a 1

        //document.getElementById('pais').value = '';
        document.getElementById('provincia').innerHTML = '<option value="">Seleccione una provincia</option>';
        document.getElementById('municipio').innerHTML = '<option value="">Seleccione un municipio</option>';
        document.getElementById('idSector').innerHTML = '<option value="">Seleccione un sector</option>';


        document.querySelector('.boton_normal[type="submit"]').innerText = 'Guardar';
        document.getElementById('delete-btn').style.display = 'none'; // Ocultar el botón de eliminar


        // Eliminar el atributo data-notario-id para que el formulario se considere en modo "crear"
        notariosForm.removeAttribute('data-notario-id');

        // Borrar mensajes de éxito/error si existen
        document.getElementById('error-message').innerText = '';
        document.getElementById('success-message').innerText = '';
    });

    function addEditButtonEvent(button) {
        button.addEventListener('click', function() {
            const notarioId = this.getAttribute('data-id');
            fetch(`${notarioApiUrl}/${notarioId}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Notary not found');
                }
                return response.json();
            })
            .then(notario => {
                document.getElementById('nombre').value = notario.Nombre;
                document.getElementById('apellido').value = notario.Apellido;
                document.getElementById('sexo').value = notario.Sexo;
                document.getElementById('nroColegiatura').value = notario.NroColegiatura;
                document.getElementById('estatus').value = notario.Estatus;

                document.querySelector('.boton_normal[type="submit"]').innerText = 'Actualizar';
                document.getElementById('delete-btn').style.display = 'inline-block'; // Mostrar el botón de eliminar

                // Rellenar los selectores de país, provincia y municipio con los valores actuales del notario
                const sectorSeleccionado = sectoresData.find(s => s.IdSector == notario.IdSector);
                const paisSeleccionado = sectorSeleccionado.Pais;
                const provinciaSeleccionada = sectorSeleccionado.Provincia;
                const municipioSeleccionado = sectorSeleccionado.Municipio;

                document.getElementById('pais').value = paisSeleccionado;

                // Rellenar provincias basadas en el país seleccionado
                const provinciasUnicas = [...new Set(sectoresData
                    .filter(s => s.Pais === paisSeleccionado)
                    .map(s => s.Provincia))];
                
                provinciaSelect.innerHTML = '<option value="">Seleccione una provincia</option>'; // Limpiar provincias
                provinciasUnicas.forEach(provincia => {
                    const option = document.createElement('option');
                    option.value = provincia;
                    option.textContent = provincia;
                    provinciaSelect.appendChild(option);
                });

                document.getElementById('provincia').value = provinciaSeleccionada;

                // Rellenar municipios basados en la provincia seleccionada
                const municipiosUnicos = [...new Set(sectoresData
                    .filter(s => s.Pais === paisSeleccionado && s.Provincia === provinciaSeleccionada)
                    .map(s => s.Municipio))];

                municipioSelect.innerHTML = '<option value="">Seleccione un municipio</option>'; // Limpiar municipios
                municipiosUnicos.forEach(municipio => {
                    const option = document.createElement('option');
                    option.value = municipio;
                    option.textContent = municipio;
                    municipioSelect.appendChild(option);
                });

                document.getElementById('municipio').value = municipioSeleccionado;

                // Rellenar sectores basados en el municipio seleccionado
                const sectoresFiltrados = sectoresData
                    .filter(s => s.Pais === paisSeleccionado && s.Provincia === provinciaSeleccionada && s.Municipio === municipioSeleccionado);

                idSectorSelect.innerHTML = '<option value="">Seleccione un sector</option>'; // Limpiar sectores
                sectoresFiltrados.forEach(sector => {
                    const option = document.createElement('option');
                    option.value = sector.IdSector;
                    option.textContent = sector.Sector;
                    idSectorSelect.appendChild(option);
                });

                // Seleccionar el sector guardado
                idSectorSelect.value = notario.IdSector;

                // Establecer el ID del notario en el formulario para editar
                notariosForm.setAttribute('data-notario-id', notario.IdNotario);
            })
            .catch(error => {
                document.getElementById('error-message').innerText = 'Error fetching notary details: ' + error.message;
                console.error("Error fetching notary details:", error);
            });
        });
    }

    const searchInput = document.getElementById('search-input');
    const itemList = document.getElementById('notarios-table');
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
                window.location.href = '/notario/';
            }
        }
    }

    checkAuth();
});
