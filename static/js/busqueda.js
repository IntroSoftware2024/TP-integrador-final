document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("search-form").addEventListener("submit", function(event) {
        event.preventDefault();

        const categoria = document.getElementById("categoria").value;
        const provincia = document.getElementById("provincia").value;
        const palabra = document.getElementById("buscarPalabra").value;

        if (categoria === "Categorías" && provincia === "Provincia" && palabra === "") {
            event.preventDefault();
            return;
        }

        let url = "/emprendimientos/busqueda#altura"; 

        if (categoria !== "Categorías") {
            const categoria_min = categoria.charAt(0).toLowerCase() + categoria.slice(1);
            url = "/emprendimientos/" + categoria_min + "#altura";
        } else if (provincia !== "Provincia") {
            // url += "/" + provincia;
        } else if (palabra !== "") {
            // url += "/" + palabra;
        }

        window.location.href = url;
    });
});