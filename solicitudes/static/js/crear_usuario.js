console.log(API_URL)
document.addEventListener('DOMContentLoaded', function() {
    const usuariosForm = document.getElementById('usuarios-form');
    const usuariosTable = document.getElementById('usuarios-table');
    const logoutButton = document.getElementById('logout');
    const deleteButtonDesplegar = document.getElementById('delete-btn');
    const deleteButtonTotal = document.getElementById('delete-button-total');
    const salirVentanaButton = document.getElementById('boton-salir-ventana');
    const clearButton = document.getElementById('clear-btn');
    ventana_confirmar = document.getElementById("ventana_confirmar");

    // Verificar si hay un token almacenado
    if (!localStorage.getItem('token')) {
        document.getElementById('error-message').innerText = 'You must be logged in to view this page';
        window.location.href = '/login/';
        return;
    }

    // Obtener el rol del usuario del localStorage
    const rol = localStorage.getItem('rol');
    if (rol === 'Agrimensor') {
        window.location.href = 'PRIMERA_ETAPA.html';
        return;
    }

    // Resto del código para cargar la página si el rol es "Administrador"
    const token = localStorage.getItem('token');
    const usuariosApiUrl = API_URL + '/usuarios';
    const usuarioApiUrl = API_URL + '/usuario';
    const roles = [
        { id: 1, nombre: 'Administrador' },
        { id: 2, nombre: 'Agrimensor' }
    ];

    // Cargar lista de roles
    const idRolSelect = document.getElementById('idRol');
    roles.forEach(rol => {
        const option = document.createElement('option');
        option.value = rol.id;
        option.text = rol.nombre;
        idRolSelect.appendChild(option);
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

    // Cargar lista de usuarios
    fetch(usuariosApiUrl, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => response.json())
    .then(data => {

        const data2 = data.filter(data => data.Estatus === 1);

        const button = document.createElement('button');
        button.type = 'button';
        button.innerHTML = `
            <p>Nombre</p>
            <p>Usuario</p>
        `;
        usuariosTable.appendChild(button);

        data2.forEach(usuario => {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'edit-btn';
            button.dataset.id = usuario.IdUsuario;
            button.innerHTML = `
                <p>${usuario.Nombre}</p>
                <p>${usuario.Usuario}</p>
            `;

            usuariosTable.appendChild(button); 
        });

        // Agregar event listeners a los botones de edición
        const editButtons = document.querySelectorAll('.edit-btn');
        editButtons.forEach(button => {
            button.addEventListener('click', function() {
                const usuarioId = this.getAttribute('data-id');
                fetch(`${usuarioApiUrl}/${usuarioId}`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('User not found');
                    }
                    return response.json();
                })
                .then(usuario => {
                    document.getElementById('usuario').value = usuario.Usuario;
                    document.getElementById('email').value = usuario.Email;
                    document.getElementById('nombre').value = usuario.Nombre;
                    document.getElementById('idRol').value = usuario.IdRol;
                    document.getElementById('estatus').value = usuario.Estatus;
                    document.getElementById('contraseña').value = usuario.Contraseña;
                    usuariosForm.setAttribute('data-usuario-id', usuario.IdUsuario);

                    const result = `a el usuario ${usuario.Usuario}`;
                    console.log(result);
                    document.getElementById('span-resto-mensaje-confirmacion').textContent = result;

                    document.querySelector('.boton_normal[type="submit"]').innerText = 'Actualizar';
                    document.getElementById('delete-btn').style.display = 'inline-block'; // Mostrar el botón de eliminar
                })
                .catch(error => {
                    document.getElementById('error-message').innerText = 'Error fetching user details: ' + error.message;
                    console.error("Error fetching user details:", error);
                });
            });
        });
    })
    .catch(error => {
        document.getElementById('error-message').innerText = 'Error fetching users: ' + error.message;
        console.error("Error fetching users:", error);
    });

    // Manejar la creación o edición de un usuario
    usuariosForm.addEventListener('submit', async function(event) {
        event.preventDefault();

        const usuarioId = usuariosForm.getAttribute('data-usuario-id');
        const method = usuarioId ? 'PUT' : 'POST';
        const apiUrl = usuarioId ? `${usuarioApiUrl}/${usuarioId}` : usuarioApiUrl;

        const usuario = document.getElementById('usuario').value;
        const email = document.getElementById('email').value;
        const contraseña = document.getElementById('contraseña').value;
        const nombre = document.getElementById('nombre').value;
        const idRol = parseInt(document.getElementById('idRol').value);
        const estatus = parseInt(document.getElementById('estatus').value);

        if (isNaN(idRol)) {
            document.getElementById('error-message').innerText = 'Invalid role selected';
            return;
        }

        const datosUsuario = {
            Usuario: usuario,
            Email: email,
            Contraseña: contraseña,
            Nombre: nombre,
            IdRol: idRol,
            Estatus: estatus
        };

        try {
            const response = await fetch(apiUrl, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(datosUsuario)
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
                throw new Error(result.message || 'Error saving user');
            }


            const successMessage = usuarioId ? 'Usuario actualizado exitosamente' : 'Usuario creado exitosamente';
            const successMessageElement = document.getElementById('success-message');
            successMessageElement.innerText = successMessage;

            setTimeout(() => {
                successMessageElement.innerText = '';
            }, 3000);

            if (!usuarioId) {
                const button = document.createElement('button');
                button.type = 'button';
                button.className = 'edit-btn';
                button.dataset.id = result.IdUsuario;
                button.innerHTML = `
                    <p>${result.Nombre}</p>
                    <p>${result.Usuario}</p>
                `;
                usuariosTable.appendChild(button);
                addEditButtonEvent(button);
            } else {
                // Actualizar la fila existente en la tabla
                const buttonToUpdate = document.querySelector(`button[data-id="${usuarioId}"]`);
                const newButton = document.createElement('button');
                newButton.type = 'button';
                newButton.className = 'edit-btn';
                newButton.dataset.id = result.IdUsuario;

                const usuarioP = document.createElement('p');
                usuarioP.textContent = result.Usuario;
                const nombreP = document.createElement('p');
                nombreP.textContent = result.Nombre;

                newButton.appendChild(usuarioP);
                newButton.appendChild(nombreP);

                buttonToUpdate.replaceWith(newButton);
                addEditButtonEvent(newButton);
            }
        } catch (error) {
            document.getElementById('error-message').innerText = error.message;
            console.error("Error saving user:", error);
        }
    });

    deleteButtonDesplegar.addEventListener('click', dezplegar_ventana_eliminar);
    salirVentanaButton.addEventListener('click', ocultar_ventana_eliminar);

    // Manejar la eliminación de un usuario
    deleteButtonTotal.addEventListener('click', async function() {
        const usuarioId = usuariosForm.getAttribute('data-usuario-id');
        if (!usuarioId) {
            document.getElementById('error-message').innerText = 'No user selected for deletion';
            return;
        }

        try {
            const response = await fetch(`${usuarioApiUrl}/${usuarioId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error('Failed to delete user');
            }

            ocultar_ventana_eliminar();

            const successMessageElement = document.getElementById('success-message');
            successMessageElement.innerText = 'Usuario eliminado exitosamente';

            setTimeout(() => {
                successMessageElement.innerText = '';
                location.reload(); // Recargar la página después de que el mensaje desaparezca
            }, 3000);

            document.getElementById('usuario').value = '';
            document.getElementById('email').value = '';
            document.getElementById('contraseña').value = '';
            document.getElementById('nombre').value = '';
            document.getElementById('idRol').value = '';
            document.getElementById('estatus').value = '1'; // restablece estatus a 1

            document.querySelector('.boton_normal[type="submit"]').innerText = 'Guardar';
            document.getElementById('delete-btn').style.display = 'none'; // Ocultar el botón de eliminar

        } catch (error) {
            document.getElementById('error-message').innerText = 'Error deleting user: ' + error.message;
            console.error("Error deleting user:", error);
        }
    });

    // Manejar el vaciado del formulario para crear un nuevo usuario
    clearButton.addEventListener('click', function() {
        // Limpiar todos los campos del formulario
        document.getElementById('usuario').value = '';
        document.getElementById('email').value = '';
        document.getElementById('contraseña').value = '';
        document.getElementById('nombre').value = '';
        document.getElementById('idRol').value = '';
        document.getElementById('estatus').value = '1'; // restablece estatus a 1

        document.querySelector('.boton_normal[type="submit"]').innerText = 'Guardar';
        document.getElementById('delete-btn').style.display = 'none'; // Ocultar el botón de eliminar

        // Eliminar el atributo data-usuario-id para que el formulario se considere en modo "crear"
        usuariosForm.removeAttribute('data-usuario-id');

        // Borrar mensajes de éxito/error si existen
        document.getElementById('error-message').innerText = '';
        document.getElementById('success-message').innerText = '';
    });

    function addEditButtonEvent(button) {
        button.addEventListener('click', function() {
            const usuarioId = this.getAttribute('data-id');
            fetch(`${usuarioApiUrl}/${usuarioId}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('User not found');
                }
                return response.json();
            })
            .then(usuario => {
                document.getElementById('usuario').value = usuario.Usuario;
                document.getElementById('email').value = usuario.Email;
                document.getElementById('nombre').value = usuario.Nombre;
                document.getElementById('idRol').value = usuario.IdRol;
                document.getElementById('estatus').value = usuario.Estatus;
                document.getElementById('contraseña').value = usuario.Contraseña;
                document.getElementById('usuarios-form').setAttribute('data-usuario-id', usuario.IdUsuario);
            
                document.querySelector('.boton_normal[type="submit"]').innerText = 'Actualizar';
                document.getElementById('delete-btn').style.display = 'inline-block'; // Mostrar el botón de eliminar
            })
            .catch(error => {
                document.getElementById('error-message').innerText = 'Error fetching user details: ' + error.message;
                console.error("Error fetching user details:", error);
            });
        });
    }

    const searchInput = document.getElementById('search-input');
    const itemList = document.getElementById('usuarios-table');
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
                window.location.href = '/usuario/';
            }
        }
    }

    
    checkAuth();
});
