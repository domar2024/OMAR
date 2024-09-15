let pageName = window.location.pathname.split('/')[1];
console.log(pageName);

const primeraEtapaEnlace = document.getElementById('enlace_nav_primera_etapa');
const segundaEtapaEnlace = document.getElementById('enlace_nav_segunda_etapa');
const terceraEtapaEnlace = document.getElementById('enlace_nav_tercera_etapa');
const prorrogaEnlace = document.getElementById('enlace_nav_prorroga');
const agrimensorEnlace = document.getElementById('enlace_nav_agrimensor');
const clienteEnlace = document.getElementById('enlace_nav_cliente');
const notarioEnlace = document.getElementById('enlace_nav_notario');
const departamentoEnlace = document.getElementById('enlace_nav_departamento');
const sectorEnlace = document.getElementById('enlace_nav_sector');
const usuarioEnlace = document.getElementById('crud_usuarios_btn');

switch (pageName) {
    case 'primera_etapa':
    case 'primera_etapa_detallada':
    case 'form_segunda_etapa':
    case 'solicitud_autorizacion':
        primeraEtapaEnlace.className = 'selected';
        break;
    case 'segunda_etapa':
    case 'segunda_etapa_detallada':
    case 'form_tercera_etapa':
        segundaEtapaEnlace.className = 'selected';
        break;
    case 'tercera_etapa':
    case 'tercera_etapa_detallada':
        terceraEtapaEnlace.className = 'selected';
        break;
    case 'prorroga':
        prorrogaEnlace.className = 'selected';
        break;
    case 'agrimensor':
        agrimensorEnlace.className = 'selected';
        break;
    case 'cliente':
        clienteEnlace.className = 'selected';
        break;
    case 'notario':
        notarioEnlace.className = 'selected';
        break;
    case 'departamento':
        departamentoEnlace.className = 'selected';
        break;
    case 'sector':
        sectorEnlace.className = 'selected';
        break;
    case 'usuario':
        usuarioEnlace.className = 'al_final selected';
        break;
}

const boton = document.getElementById('uña_barra_lateral');
const elemento = document.getElementById('barra_lateral');

boton.addEventListener('click', () => {
    if (elemento.style.display === 'none') {
            elemento.style.display = 'flex';
            boton.style.marginLeft = '277px';
    } else {
            elemento.style.display = 'none';
            boton.style.marginLeft = '0';
    }
});