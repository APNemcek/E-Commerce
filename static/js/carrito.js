document.addEventListener("DOMContentLoaded", function() {
    const tipoEnvioSelect = document.getElementById("tipoenvio");
    const costoEnvioSpan = document.getElementById("costo_envio");
    const totalFinalSpan = document.getElementById("total_final");
    const finalizarCompraBtn = document.getElementById("finalizarCompraBtn");
    const compraForm = document.getElementById("compraForm");

    const popupConfirm = document.getElementById("popupConfirm");
    const popupConfirmYes = document.getElementById("popupConfirmYes");
    const popupConfirmNo = document.getElementById("popupConfirmNo");

    const envioCostos = {
        "envio": 6500,
        "retiro": 0
    };

    function confirmarCompra() {
        popupConfirm.classList.add("active");
    }

    function closePopup() {
        popupConfirm.classList.remove("active");
    }

    finalizarCompraBtn.addEventListener("click", confirmarCompra);

    popupConfirmYes.addEventListener("click", function() {
        compraForm.submit();
    });

    popupConfirmNo.addEventListener("click", closePopup);

    function actualizarTotal() {
        const selectedEnvio = tipoEnvioSelect.value;
        const costoEnvio = envioCostos[selectedEnvio];
        const totalCompra = parseInt(totalFinalSpan.getAttribute("data-total"), 10); 

        costoEnvioSpan.textContent = `$${costoEnvio.toLocaleString()}`;
        totalFinalSpan.textContent = `$${(totalCompra + costoEnvio).toLocaleString()}`;
    }

    tipoEnvioSelect.addEventListener("change", actualizarTotal);
    actualizarTotal();  // Actualizo total al cargar la página

    document.querySelectorAll(".numero").forEach(function(element) {
        const valor = parseInt(element.textContent.replace('$', '').replace(/\./g, ''), 10);
        element.textContent = `$${valor.toLocaleString()}`;
    });
});