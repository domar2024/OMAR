document.addEventListener('DOMContentLoaded', function() {
    const rol = localStorage.getItem('rol');


    const boton = document.getElementById('crud_usuarios_btn');

    if (rol === 'Agrimensor') {

        if (boton) {
            boton.style.display = 'none';
        }
    } else if (rol === 'Administrador') {

        if (boton) {
            boton.style.display = 'inline-block'; 
        }
    }
});
