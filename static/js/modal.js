// Función para abrir el tab
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

// Mostrar el modal cuando se carga la página
window.onload = function() {
    var modal = document.getElementById("modal");
    modal.style.display = "block";
    document.querySelector('.tablinks').click(); 
}

// Inicio de sesion (sin validacion)
document.getElementById('ingresarLogin').addEventListener('click', function(event) {
    event.preventDefault();
    var modal = document.getElementById('modal');
    modal.style.display = 'none'; // Cerrar el modal
});

// Registro (sin validación)
document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var modal = document.getElementById('modal');
    modal.style.display = 'none'; // Cerrar el modal
});




