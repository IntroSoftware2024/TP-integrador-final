document.addEventListener("DOMContentLoaded", function() {

    document.getElementById("search-form").addEventListener("submit", function(event) {
        event.preventDefault(); // Evita que el formulario se envíe automáticamente

        const categoria = document.getElementById("categoria").value;
        if (categoria !== "Categorías") {
            const categoria_min = categoria.charAt(0).toLowerCase() + categoria.slice(1);
            const url = "/emprendimientos/" + categoria_min + "#altura";
            window.location.href = url; // Redirige a la URL construida con la categoría seleccionada
        }
    });
});