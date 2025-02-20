function mostrarPopup(id) {
    document.getElementById('popup' + id).style.display = 'block';
}

function cerrarPopup(id) {
    document.getElementById('popup' + id).style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll(".precio_js").forEach(function (element) {
        
        const valor = parseInt(element.textContent.replace(/[^\d]/g, ''), 10);
        
        if (!isNaN(valor)) {
            element.textContent = `$${valor.toLocaleString('es-ES')}`;
        }
    });
});