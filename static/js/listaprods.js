document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll(".precio_orig, .precio_desc").forEach(function (element) {
        // extraigo el valor
        const valor = parseInt(element.textContent.replace(/[^\d]/g, ''), 10);
        // me aseguro que sea un numero
        if (!isNaN(valor)) {
            element.textContent = `$${valor.toLocaleString('es-ES')}`;
        }
    });
});
