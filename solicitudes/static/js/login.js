console.log(API_URL)
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async function(event) {
            event.preventDefault();

            const usuario = document.getElementById('username').value;
            const contraseña = document.getElementById('password').value;

            const apiUrl = API_URL + '/login';

            try {
                const response = await fetch(apiUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ usuario, contraseña })
                });

                const responseBody = await response.text();
                console.log('Response body:', responseBody);  // Depuración

                let result;
                try {
                    result = JSON.parse(responseBody);
                } catch (e) {
                    throw new Error('Invalid JSON response: ' + responseBody);
                }

                if (!response.ok) {
                    throw new Error(result.message || 'Usuario o Password incorrecto');
                }

                if (result.message === "Login exitoso") {
                    localStorage.setItem('userId', result.IdUsuario);
                    localStorage.setItem('rol', result.Rol);
                    localStorage.setItem('token', result.token || 'some-fake-token'); 
                    window.location.href = '/primera_etapa/';
                } else {
                    throw new Error(result.message || 'Login failed');
                }
            } catch (error) {
                document.getElementById('error-message').innerText = error.message;
            }
        });
    }

    const logoutButton = document.getElementById('logout');
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
