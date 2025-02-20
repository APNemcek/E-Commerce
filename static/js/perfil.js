function confirmarModificacion() {
    document.getElementById("popup").style.display = "block";
    document.getElementById("popup-overlay").style.display = "block";
}

function cancelarModificacion() {
    document.getElementById("popup").style.display = "none";
    document.getElementById("popup-overlay").style.display = "none";
}

function enviarFormulario() {
    document.getElementById("perfilForm").submit();
}