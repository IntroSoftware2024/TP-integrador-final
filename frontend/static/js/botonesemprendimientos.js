document.addEventListener("DOMContentLoaded", function() {
    // Obtener todos los elementos con la clase "thumb"
    var elementos = document.querySelectorAll(".thumb");
  
    // Iterar sobre cada elemento y agregar evento de clic
    elementos.forEach(function(elemento) {
      elemento.addEventListener("click", function(event) {
        // Obtener la URL con el ancla deseado desde el atributo href del enlace dentro del elemento clicado
        var url = elemento.querySelector("a").getAttribute("href");
        
        // Redirigir a la URL especificada
        window.location.href = url;
        
        // Prevenir el comportamiento predeterminado del enlace
        event.preventDefault();
      });
    });
  });