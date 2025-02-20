document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll(".precio_js").forEach(function (element) {

        const valor = parseInt(element.textContent.replace(/[^\d]/g, ''), 10);

        if (!isNaN(valor)) {
            element.textContent = `$${valor.toLocaleString('es-ES')}`;
        }
        
    });
});