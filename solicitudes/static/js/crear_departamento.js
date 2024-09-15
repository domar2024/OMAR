console.log(API_URL)
document.addEventListener('DOMContentLoaded', function() {
    const departamentosForm = document.getElementById('departamentos-form');
    const departamentosTable = document.getElementById('departamentos-table');
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
    const departamentosApiUrl = API_URL + '/departamentos';
    const departamentoApiUrl = API_URL + '/departamento';

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

        // Cargar departamentos y mostrar solo aquellos con Estatus 1
        fetch(departamentosApiUrl, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => response.json())
        .then(departamentos => {
            const departamentosFiltrados = departamentos.filter(departamento => departamento.Estatus === 1);

            const button = document.createElement('button');
                    button.type = 'button';
                    button.innerHTML = `
                        <p>Departamento</p>
                        <p>Sector</p>
                    `;
            departamentosTable.appendChild(button);

            departamentosFiltrados.forEach(departamento => {
                const button = document.createElement('button');
                button.type = 'button';
                button.className = 'edit-btn';
                button.dataset.id = departamento.IdDepartamentoOficina;
                button.innerHTML = `
                    <p>${departamento.DepartamentoOficina}</p>
                    <p>${departamento.sector.Sector}</p>
                `;
                departamentosTable.appendChild(button);
            });

            // Agregar event listeners a los botones de edición
            const editButtons = document.querySelectorAll('.edit-btn');
            editButtons.forEach(button => {
                button.addEventListener('click', function() {
                    const departamentoId = this.getAttribute('data-id');
                    const departamento = departamentosFiltrados.find(d => d.IdDepartamentoOficina == departamentoId);
                
                    if (departamento) {
                        document.getElementById('departamentoOficina').value = departamento.DepartamentoOficina;
                        document.getElementById('encargado').value = departamento.Encargado;
                
                        const result = `a el departamento ${departamento.DepartamentoOficina}`;
                        console.log(result);
                        document.getElementById('span-resto-mensaje-confirmacion').textContent = result;

                        document.querySelector('.boton_normal[type="submit"]').innerText = 'Actualizar';
                        document.getElementById('delete-btn').style.display = 'inline-block'; // Mostrar el botón de eliminar
                
                        // Rellenar los selectores de país, provincia y municipio con los valores actuales del departamento
                        const sectorSeleccionado = sectoresData.find(s => s.IdSector == departamento.IdSector);
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
                        idSectorSelect.value = departamento.IdSector;
                
                        document.getElementById('estatus').value = departamento.Estatus;
                        departamentosForm.setAttribute('data-departamento-id', departamento.IdDepartamentoOficina);
                    }
                });
                
            });
        })
        .catch(error => {
            document.getElementById('error-message').innerText = 'Error fetching departments: ' + error.message;
            console.error("Error fetching departments:", error);
        });
    })
    .catch(error => {
        document.getElementById('error-message').innerText = 'Error fetching sectors: ' + error.message;
        console.error("Error fetching sectors:", error);
    });

    // Manejar la creación o edición de un departamento
    departamentosForm.addEventListener('submit', async function(event) {
        event.preventDefault();

        const departamentoId = departamentosForm.getAttribute('data-departamento-id');
        const method = departamentoId ? 'PUT' : 'POST';
        const apiUrl = departamentoId ? `${departamentoApiUrl}/${departamentoId}` : departamentoApiUrl;

        const departamentoOficina = document.getElementById('departamentoOficina').value;
        const encargado = document.getElementById('encargado').value;
        const idSector = parseInt(document.getElementById('idSector').value);
        const estatus = parseInt(document.getElementById('estatus').value);

        if (isNaN(idSector)) {
            document.getElementById('error-message').innerText = 'Invalid sector selected';
            return;
        }

        const datosDepartamento = {
            DepartamentoOficina: departamentoOficina,
            Encargado: encargado,
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
                body: JSON.stringify(datosDepartamento)
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
                throw new Error(result.message || 'Error saving department');
            }

            const successMessage = departamentoId ? 'Departamento actualizado exitosamente' : 'Departamento creado exitosamente';
            const successMessageElement = document.getElementById('success-message')
            successMessageElement.innerText = successMessage;


            setTimeout(() => {
                successMessageElement.innerText = '';
            }, 3000);

            if (!departamentoId) {
                const button = document.createElement('button');
                button.type = 'button';
                button.className = 'edit-btn';
                button.dataset.id = result.IdDepartamentoOficina;
                button.innerHTML = `
                    <p>${result.DepartamentoOficina}</p>
                    <p>${result.Encargado}</p>
                `;
                departamentosTable.appendChild(button);
                addEditButtonEvent(button);
            } else {
                const buttonToUpdate = document.querySelector(`button[data-id="${departamentoId}"]`);
                const newButton = document.createElement('button');
                newButton.type = 'button';
                newButton.className = 'edit-btn';
                newButton.dataset.id = result.IdDepartamentoOficina;
                newButton.innerHTML = `
                    <p>${result.DepartamentoOficina}</p>
                    <p>${result.Encargado}</p>
                `;
                buttonToUpdate.replaceWith(newButton);
                addEditButtonEvent(newButton);
            }
        } catch (error) {
            document.getElementById('error-message').innerText = error.message;
            console.error("Error saving department:", error);
        }
    });

    deleteButtonDesplegar.addEventListener('click', dezplegar_ventana_eliminar);
    salirVentanaButton.addEventListener('click', ocultar_ventana_eliminar);

    // Manejar la eliminación de un departamento
    deleteButtonTotal.addEventListener('click', async function() {
        const departamentoId = departamentosForm.getAttribute('data-departamento-id');
        if (!departamentoId) {
            document.getElementById('error-message').innerText = 'No department selected for deletion';
            return;
        }

        try {
            const response = await fetch(`${departamentoApiUrl}/${departamentoId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error('Failed to delete department');
            }

        const successMessageElement = document.getElementById('success-message');
        successMessageElement.innerText = 'Departamento eliminado exitosamente';

        ocultar_ventana_eliminar();
        // Hacer que el mensaje desaparezca después de 5 segundos y luego recargar la página
        setTimeout(() => {
            successMessageElement.innerText = '';
            location.reload(); // Recargar la página después de que el mensaje desaparezca
        }, 3000);

        document.getElementById('departamentoOficina').value = '';
        document.getElementById('encargado').value = '';
        document.getElementById('idSector').value = '';
        document.getElementById('estatus').value = '1'; // restablece estatus a 1

        //document.getElementById('pais').value = '';
        document.getElementById('provincia').innerHTML = '<option value="">Seleccione una provincia</option>';
        document.getElementById('municipio').innerHTML = '<option value="">Seleccione un municipio</option>';
        document.getElementById('idSector').innerHTML = '<option value="">Seleccione un sector</option>';


        } catch (error) {
            document.getElementById('error-message').innerText = 'Error deleting department: ' + error.message;
            console.error("Error deleting department:", error);
        }
    });

    // Manejar el vaciado del formulario para crear un nuevo departamento
    clearButton.addEventListener('click', function() {
        // Limpiar todos los campos del formulario
        document.getElementById('departamentoOficina').value = '';
        document.getElementById('encargado').value = '';
        document.getElementById('idSector').value = '';
        document.getElementById('estatus').value = '1'; // restablece estatus a 1


        //document.getElementById('pais').value = '';
        document.getElementById('provincia').innerHTML = '<option value="">Seleccione una provincia</option>';
        document.getElementById('municipio').innerHTML = '<option value="">Seleccione un municipio</option>';
        document.getElementById('idSector').innerHTML = '<option value="">Seleccione un sector</option>';


        document.querySelector('.boton_normal[type="submit"]').innerText = 'Guardar';
        document.getElementById('delete-btn').style.display = 'none'; // Ocultar el botón de eliminar

        // Eliminar el atributo data-departamento-id para que el formulario se considere en modo "crear"
        departamentosForm.removeAttribute('data-departamento-id');

        // Borrar mensajes de éxito/error si existen
        document.getElementById('error-message').innerText = '';
        document.getElementById('success-message').innerText = '';
    });

    function addEditButtonEvent(button) {
        button.addEventListener('click', function() {
            const departamentoId = this.getAttribute('data-id');
            fetch(`${departamentoApiUrl}/${departamentoId}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Department not found');
                }
                return response.json();
            })
            .then(departamento => {
                document.getElementById('departamentoOficina').value = departamento.DepartamentoOficina;
                document.getElementById('encargado').value = departamento.Encargado;
                document.getElementById('idSector').value = departamento.IdSector;
                document.getElementById('estatus').value = departamento.Estatus;
                document.getElementById('departamentos-form').setAttribute('data-departamento-id', departamento.IdDepartamentoOficina);
            
                document.querySelector('.boton_normal[type="submit"]').innerText = 'Actualizar';
                document.getElementById('delete-btn').style.display = 'inline-block'; // Mostrar el botón de eliminar
            
            })
            .catch(error => {
                document.getElementById('error-message').innerText = 'Error fetching department details: ' + error.message;
                console.error("Error fetching department details:", error);
            });
        });
    }


    const searchInput = document.getElementById('search-input');
    const itemList = document.getElementById('departamentos-table');
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
                window.location.href = '/departamento/';
            }
        }
    }

    checkAuth();
});
