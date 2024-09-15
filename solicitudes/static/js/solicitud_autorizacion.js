console.log(API_URL)
document.addEventListener('DOMContentLoaded', function() {
    const solicitudForm = document.getElementById('solicitud-form');
    const logoutButton = document.getElementById('logout');
    const paisSelect = document.getElementById('pais');
    const provinciaSelect = document.getElementById('provincia');
    const municipioSelect = document.getElementById('municipio');
    const idSectorSelect = document.getElementById('idSector');
    const idCliente02Select = document.getElementById('idCliente02');

    // Función para obtener el valor de idCliente02 dependiendo de si está deshabilitado
    function getIdCliente02() {
        return idCliente02Select.disabled ? 1 : parseInt(idCliente02Select.value) || null;
    }


    function checkAuth() {
        const token = localStorage.getItem('token');
        if (!token) {
            if (!window.location.pathname.endsWith('/login/')) {
                window.location.href = '/login/';
            }
        } else {
            if (window.location.pathname.endsWith('/login/')) {
                window.location.href = '/solicitud_autorizacion/';
            }
        }
    }

    checkAuth();

    if (logoutButton) {
        logoutButton.addEventListener('click', function() {
            localStorage.removeItem('token');
            window.location.href = '/login/';
        });
    }

    const token = localStorage.getItem('token');
    const apiUrls = {
        clientes: API_URL + '/clientes',
        agrimensores: API_URL + '/agrimensores',
        notarios: API_URL + '/notarios',
        sectores: API_URL + '/sectores',
        departamentos: API_URL + '/departamentos'
    };

    // Cargar datos para selects
    const loadDataForSelect = (url, selectElementId, idField, textField, textconc2 = "", textconc3 = "") => {
        fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => response.json())
        .then(data => {
            const selectElement = document.getElementById(selectElementId);
            data.filter(item => item.Estatus === 1).forEach(item => {
                const option = document.createElement('option');
                option.value = item[idField];
                if(textconc2){
                    option.text = item[textField] + " / " + item[textconc2] + " / " + item[textconc3];
                }else{
                    option.text = item[textField];
                }
    
                selectElement.appendChild(option);
            });
        })
        .catch(error => {
            document.getElementById('error-message').innerText = `Error fetching ${selectElementId}: ` + error.message;
        });
    };

    const loadOptions = (url, selectElementId, idField, textField) => {
        fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
            .then(response => response.json())
            .then(data => {
                const selectElement = document.getElementById(selectElementId);
                data.forEach(item => {
                    const option = document.createElement('option');
                    option.value = item[idField];
                    option.textContent = item[textField];
                    selectElement.appendChild(option);
                });
            })
            .catch(error => {
                document.getElementById('error-message').innerText = `Error fetching ${selectElementId}: ` + error.message;
            });
    };

    loadOptions(API_URL + '/derechos_sustentados', 'derecho-sustentado', 'IdDerechoSustentado', 'DerechoSustentado');

    loadDataForSelect(apiUrls.clientes, 'idCliente01', 'IdCliente', 'Nombre','Apellido','CedulaPasaporte');
    loadDataForSelect(apiUrls.clientes, 'idCliente02', 'IdCliente', 'Nombre','Apellido','CedulaPasaporte');
    loadDataForSelect(apiUrls.agrimensores, 'idAgrimensor', 'IdAgrimensor', 'Nombre','Apellido','CODIA');
    loadDataForSelect(apiUrls.notarios, 'idNotario', 'IdNotario', 'Nombre','Apellido', 'NroColegiatura');
    loadDataForSelect(apiUrls.departamentos, 'idDepartamentoOficina', 'IdDepartamentoOficina', 'DepartamentoOficina');

    // Filtrado de País, Provincia, Municipio y Sector
    let sectoresData = [];

    fetch(apiUrls.sectores, {
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

        // Event listener para seleccionar un país y cargar provincias
        const paisSeleccionado = "Republica Dominicana";
        paisSelect.value = paisSeleccionado;
        paisSelect.disabled = true;

        //paisSelect.addEventListener('change', function() {
        //    const paisSeleccionado = paisSelect.value;
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
        //});

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
    })
    .catch(error => {
        document.getElementById('error-message').innerText = 'Error fetching sectors: ' + error.message;
        console.error("Error fetching sectors:", error);
    });

    // Manejar la creación o edición de una solicitud de autorización
    solicitudForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        
        const solicitudData = {
            IdCliente01: parseInt(document.getElementById('idCliente01').value),
            IdCliente02: getIdCliente02(),
            IdAgrimensor: parseInt(document.getElementById('idAgrimensor').value),
            IdNotario: parseInt(document.getElementById('idNotario').value),
            FechaAutorizacion: document.getElementById('fechaAutorizacion').value,
            ActuacionTecnica: document.getElementById('actuacionTecnica').value,
            Parcela: document.getElementById('parcela').value,
            DistritoCatrastal: document.getElementById('distritoCatrastal').value,
            Calle: document.getElementById('calle').value,
            IdSector: parseInt(document.getElementById('idSector').value),
            Area: document.getElementById('area').value,
            CoordLatitud: document.getElementById('coordLatitud').value,
            CoordLongitud: document.getElementById('coordLongitud').value,
            CoordX: document.getElementById('coordX').value,
            CoordY: document.getElementById('coordY').value,
            FechaContratoVenta: document.getElementById('fechaContratoVenta').value,
            IdDepartamentoOficina: parseInt(document.getElementById('idDepartamentoOficina').value),
            NroExpediente: document.getElementById('nroExpediente').value,
            Estatus: 1,  // Valor por defecto
            Enlace: "", // Se envía el campo "Enlace" como vacío
            IdDerechoSustentado: parseInt(document.getElementById('derecho-sustentado').value),
        };

        console.log(solicitudData);
        try {
            const response = await fetch(API_URL + '/solicitud', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(solicitudData)
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.message || 'Error al enviar la solicitud');
            }

            const idSolicitud = result.IdSolicitud;

            alert('Solicitud creada exitosamente');
            
            // Segundo POST a Django
            const djangoResponse = await fetch('/procesar_formulario_solicitudes/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({"IdSolicitud": idSolicitud})
            });


            const djangoResult = await djangoResponse.json();

            if (!djangoResponse.ok) {
                throw new Error(djangoResult.message || 'Error al procesar los datos en Django');
            }

            console.log('Datos enviados a Django exitosamente');
            // Puedes realizar alguna acción adicional después de que Django haya procesado los datos

            window.location.href = '/primera_etapa/'
        } catch (error) {
            //document.getElementById('error-message').innerText = error.message;
        }
    });

    document.getElementById('idCheckboxConyugue').addEventListener('click', function() {
        const selectCliente2 = document.getElementById('idCliente02');

        if (this.checked) {
            selectCliente2.disabled = false;
        } else {
            selectCliente2.disabled = true;
            selectCliente2.value = '';  // Resetea el valor del select
        }
    });
});