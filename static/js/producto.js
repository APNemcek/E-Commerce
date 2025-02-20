function cambiarImagen(src) {
    document.getElementById("imagen-principal").src = src;
}
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll(".precio_orig, .precio_desc").forEach(function (element) {
        
        const valor = parseInt(element.textContent.replace(/[^\d]/g, ''), 10);
        
        if (!isNaN(valor)) {
            element.textContent = `$${valor.toLocaleString('es-ES')}`;
        }
    });
});
