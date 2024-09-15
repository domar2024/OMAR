console.log(API_URL)
document.addEventListener('DOMContentLoaded', function() {
    const clientesForm = document.getElementById('clientes-form');
    const clientesTable = document.getElementById('clientes-table');
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
    const clientesApiUrl = API_URL + '/clientes';
    const clienteApiUrl = API_URL + '/cliente';
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

        // Cargar clientes y mostrar solo aquellos con Estatus 1
        fetch(clientesApiUrl, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => response.json())
        .then(clientes => {
            const clientesFiltrados = clientes.filter(cliente => cliente.Estatus === 1);


            const button = document.createElement('button');
                    button.type = 'button';
                    button.innerHTML = `
                        <p>Cliente</p>
                        <p>Cedula</p>
                    `;
            clientesTable.appendChild(button);

            clientesFiltrados.forEach(cliente => {
                const button = document.createElement('button');
                button.type = 'button';
                button.className = 'edit-btn';
                button.dataset.id = cliente.IdCliente;
                button.innerHTML = `
                    <p>${cliente.Nombre} ${cliente.Apellido}</p>
                    <p>${cliente.CedulaPasaporte}</p>
                `;
                clientesTable.appendChild(button);
            });

            // Agregar event listeners a los botones de edición
            const editButtons = document.querySelectorAll('.edit-btn');
            editButtons.forEach(button => {
                button.addEventListener('click', function() {
                    const clienteId = this.getAttribute('data-id');
                    const cliente = clientesFiltrados.find(c => c.IdCliente == clienteId);

                    if (cliente) {
                        document.getElementById('nombre').value = cliente.Nombre;
                        document.getElementById('apellido').value = cliente.Apellido;
                        document.getElementById('sexo').value = cliente.Sexo;
                        document.getElementById('cedulaPasaporte').value = cliente.CedulaPasaporte;
                        document.getElementById('nacionalidad').value = cliente.Nacionalidad;
                        document.getElementById('estadoCivil').value = cliente.EstadoCivil;
                        document.getElementById('ocupacion').value = cliente.Ocupacion;
                        document.getElementById('celular').value = cliente.Celular;
                        document.getElementById('correo').value = cliente.Correo;
                        document.getElementById('calle').value = cliente.Calle;
                        document.getElementById('estatus').value = cliente.Estatus;

                        const result = `a el cliente ${cliente.Nombre} ${cliente.Apellido}`;
                        console.log(result);
                        document.getElementById('span-resto-mensaje-confirmacion').textContent = result;

                        document.querySelector('.boton_normal[type="submit"]').innerText = 'Actualizar';
                        document.getElementById('delete-btn').style.display = 'inline-block'; // Mostrar el botón de eliminar


                        // Rellenar los selectores de país, provincia y municipio con los valores actuales del cliente
                        const sectorSeleccionado = sectoresData.find(s => s.IdSector == cliente.IdSector);
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
                        idSectorSelect.value = cliente.IdSector;

                        // Establecer el ID del cliente en el formulario para editar
                        clientesForm.setAttribute('data-cliente-id', cliente.IdCliente);
                    }
                });
            });
        })
        .catch(error => {
            document.getElementById('error-message').innerText = 'Error fetching clients: ' + error.message;
            console.error("Error fetching clients:", error);
        });
    })
    .catch(error => {
        document.getElementById('error-message').innerText = 'Error fetching sectors: ' + error.message;
        console.error("Error fetching sectors:", error);
    });

    clientesForm.addEventListener('submit', async function(event) {
        event.preventDefault();
    
        const clienteId = clientesForm.getAttribute('data-cliente-id');
        const method = clienteId ? 'PUT' : 'POST';
        const apiUrl = clienteId ? `${clienteApiUrl}/${clienteId}` : clienteApiUrl;
    
        const nombre = document.getElementById('nombre').value;
        const apellido = document.getElementById('apellido').value;
        const cedulaPasaporte = document.getElementById('cedulaPasaporte').value;
        const nacionalidad = document.getElementById('nacionalidad').value;
        const estadoCivil = document.getElementById('estadoCivil').value;
        const ocupacion = document.getElementById('ocupacion').value;
        const celular = document.getElementById('celular').value;
        const correo = document.getElementById('correo').value;
        const calle = document.getElementById('calle').value;
        const sexo = document.getElementById('sexo').value;
        const idSector = parseInt(document.getElementById('idSector').value);
        const estatus = parseInt(document.getElementById('estatus').value);
    
        if (sexo !== 'M' && sexo !== 'F') {
            document.getElementById('error-message').innerText = 'Invalid role selected';
            return;
        }

        if (isNaN(idSector)) {
            document.getElementById('error-message').innerText = 'Invalid sector selected';
            return;
        }
    
        const datosCliente = {
            Nombre: nombre,
            Apellido: apellido,
            Sexo: sexo,
            CedulaPasaporte: cedulaPasaporte,
            Nacionalidad: nacionalidad,
            EstadoCivil: estadoCivil,
            Ocupacion: ocupacion,
            Celular: celular,
            Correo: correo,
            Calle: calle,
            IdSector: idSector,
            Estatus: estatus
        };
    
        try {
            const response = await fetch(apiUrl, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(datosCliente)
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
                throw new Error(result.message || 'Error saving client');
            }
    
            // Modificación del mensaje de éxito
            const successMessage = clienteId ? 'Cliente actualizado exitosamente' : 'Cliente creado exitosamente';
            const successMessageElement = document.getElementById('success-message');
            successMessageElement.innerText = successMessage;
    
            // Hacer que el mensaje desaparezca después de 5 segundos
            setTimeout(() => {
                successMessageElement.innerText = '';
            }, 3000);
    
            if (!clienteId) {
                const button = document.createElement('button');
                button.type = 'button';
                button.className = 'edit-btn';
                button.dataset.id = result.IdCliente;
                button.innerHTML = `
                    <p>${result.Nombre} ${result.Apellido}</p>
                    <p>${result.CedulaPasaporte}</p>
                `;
                clientesTable.appendChild(button);
                addEditButtonEvent(button);
            } else {
                // Actualizar la fila existente en la tabla
                const buttonToUpdate = document.querySelector(`button[data-id="${clienteId}"]`);
                const newButton = document.createElement('button');
                newButton.type = 'button';
                newButton.className = 'edit-btn';
                newButton.dataset.id = result.IdCliente;
                newButton.innerHTML = `
                    <p>${result.Nombre}</p>
                    <p>${result.Apellido}</p>
                `;
                buttonToUpdate.replaceWith(newButton);
                addEditButtonEvent(newButton);
            }
        } catch (error) {
            document.getElementById('error-message').innerText = error.message;
            console.error("Error saving client:", error);
        }
    });
    
    deleteButtonDesplegar.addEventListener('click', dezplegar_ventana_eliminar);
    salirVentanaButton.addEventListener('click', ocultar_ventana_eliminar);

    // Manejar la eliminación de un cliente
    deleteButtonTotal.addEventListener('click', async function() {
        const clienteId = clientesForm.getAttribute('data-cliente-id');
        if (!clienteId) {
            document.getElementById('error-message').innerText = 'No client selected for deletion';
            return;
        }

        try {
            const response = await fetch(`${clienteApiUrl}/${clienteId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error('Failed to delete client');
            }

            
                    // Mostrar el mensaje de éxito inmediatamente
        const successMessageElement = document.getElementById('success-message');
        successMessageElement.innerText = 'Cliente eliminado exitosamente';

        ocultar_ventana_eliminar();
        // Hacer que el mensaje desaparezca después de 5 segundos y luego recargar la página
        setTimeout(() => {
            successMessageElement.innerText = '';
            location.reload(); // Recargar la página después de que el mensaje desaparezca
        }, 3000);

        document.getElementById('nombre').value = '';
        document.getElementById('apellido').value = '';
        document.getElementById('sexo').value = '';
        document.getElementById('cedulaPasaporte').value = '';
        document.getElementById('nacionalidad').value = '';
        document.getElementById('estadoCivil').value = '';
        document.getElementById('ocupacion').value = '';
        document.getElementById('celular').value = '';
        document.getElementById('correo').value = '';
        document.getElementById('calle').value = '';
        document.getElementById('idSector').value = '';
        document.getElementById('estatus').value = '1';

        //document.getElementById('pais').value = '';
        document.getElementById('provincia').innerHTML = '<option value="">Seleccione una provincia</option>';
        document.getElementById('municipio').innerHTML = '<option value="">Seleccione un municipio</option>';
        document.getElementById('idSector').innerHTML = '<option value="">Seleccione un sector</option>';

        // Cambiar el texto del botón de guardar y ocultar el botón de eliminar
        document.querySelector('.boton_normal[type="submit"]').innerText = 'Guardar';
        document.getElementById('delete-btn').style.display = 'none';
            
    
        } catch (error) {
            document.getElementById('error-message').innerText = 'Error deleting client: ' + error.message;
            console.error("Error deleting client:", error);
        }
    });

    // Manejar el vaciado del formulario para crear un nuevo cliente
    clearButton.addEventListener('click', function() {
        // Limpiar todos los campos del formulario
        document.getElementById('nombre').value = '';
        document.getElementById('apellido').value = '';
        document.getElementById('sexo').value = '';
        document.getElementById('cedulaPasaporte').value = '';
        document.getElementById('nacionalidad').value = '';
        document.getElementById('estadoCivil').value = '';
        document.getElementById('ocupacion').value = '';
        document.getElementById('celular').value = '';
        document.getElementById('correo').value = '';
        document.getElementById('calle').value = '';
        document.getElementById('idSector').value = '';
        document.getElementById('estatus').value = '1'; // restablece estatus a 1

        // Resetear selectores
        //document.getElementById('pais').value = '';
        document.getElementById('provincia').innerHTML = '<option value="">Seleccione una provincia</option>';
        document.getElementById('municipio').innerHTML = '<option value="">Seleccione un municipio</option>';
        document.getElementById('idSector').innerHTML = '<option value="">Seleccione un sector</option>';


        document.querySelector('.boton_normal[type="submit"]').innerText = 'Guardar';
        document.getElementById('delete-btn').style.display = 'none'; // Ocultar el botón de eliminar

        // Eliminar el atributo data-cliente-id para que el formulario se considere en modo "crear"
        clientesForm.removeAttribute('data-cliente-id');

        // Borrar mensajes de éxito/error si existen
        document.getElementById('error-message').innerText = '';
        document.getElementById('success-message').innerText = '';
    });

    function addEditButtonEvent(button) {
        button.addEventListener('click', function() {
            const clienteId = this.getAttribute('data-id');
            fetch(`${clienteApiUrl}/${clienteId}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Client not found');
                }
                return response.json();
            })
            .then(cliente => {
                document.getElementById('nombre').value = cliente.Nombre;
                document.getElementById('apellido').value = cliente.Apellido;
                document.getElementById('sexo').value = cliente.Sexo;
                document.getElementById('cedulaPasaporte').value = cliente.CedulaPasaporte;
                document.getElementById('nacionalidad').value = cliente.Nacionalidad;
                document.getElementById('estadoCivil').value = cliente.EstadoCivil;
                document.getElementById('ocupacion').value = cliente.Ocupacion;
                document.getElementById('celular').value = cliente.Celular;
                document.getElementById('correo').value = cliente.Correo;
                document.getElementById('calle').value = cliente.Calle;
                document.getElementById('estatus').value = cliente.Estatus;

                document.querySelector('.boton_normal[type="submit"]').innerText = 'Actualizar';
                document.getElementById('delete-btn').style.display = 'inline-block'; // Mostrar el botón de eliminar

                // Rellenar los selectores de país, provincia y municipio con los valores actuales del cliente
                const sectorSeleccionado = sectoresData.find(s => s.IdSector == cliente.IdSector);
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
                idSectorSelect.value = cliente.IdSector;

                // Establecer el ID del cliente en el formulario para editar
                clientesForm.setAttribute('data-cliente-id', cliente.IdCliente);
            })
            .catch(error => {
                document.getElementById('error-message').innerText = 'Error fetching client details: ' + error.message;
                console.error("Error fetching client details:", error);
            });
        });
    }

    const searchInput = document.getElementById('search-input');
    const itemList = document.getElementById('clientes-table');
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
            window.location.href = 'LOGIN.html';
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
                window.location.href = '/cliente/';
            }
        }
    }

    checkAuth();
});
