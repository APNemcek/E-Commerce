document.addEventListener("DOMContentLoaded", () => {
    const popupContainer = document.getElementById("popupContainer");
    popupContainer.style.display = "none";

    // Validaciones del formulario
    const emailInputs = document.querySelectorAll("input[type='email']");
    const phoneInputs = document.querySelectorAll("input[name='Teléfono']");
    const addressInputs = document.querySelectorAll("input[name='Dirección']");
    const nameInputs = document.querySelectorAll("input[name='Name']");
    const passwordInputs = document.querySelectorAll("input[type='password']");

    emailInputs.forEach(input => input.addEventListener("input", validarCampos));
    phoneInputs.forEach(input => input.addEventListener("input", validarCampos));
    addressInputs.forEach(input => input.addEventListener("input", validarCampos));
    nameInputs.forEach(input => input.addEventListener("input", validarCampos));
    passwordInputs.forEach(input => input.addEventListener("input", validarCampos));
    
    validarErroresIniciales();
});

function loadTemplate(type) {
    fetch(`/${type}`)
        .then(response => response.text())
        .then(html => {
            const popupContent = document.getElementById("popupContent");
            popupContent.innerHTML = html;
            const popupContainer = document.getElementById("popupContainer");
            popupContainer.style.display = "flex";
            popupContainer.classList.add('show');

            // Valido los campos del formulario
            const emailInputs = popupContent.querySelectorAll("input[type='email']");
            const phoneInputs = popupContent.querySelectorAll("input[name='Teléfono']");
            const addressInputs = popupContent.querySelectorAll("input[name='Dirección']");
            const nameInputs = popupContent.querySelectorAll("input[name='Name']");
            const passwordInputs = popupContent.querySelectorAll("input[type='password']");

            emailInputs.forEach(input => input.addEventListener("input", validarCampos));
            phoneInputs.forEach(input => input.addEventListener("input", validarCampos));
            addressInputs.forEach(input => input.addEventListener("input", validarCampos));
            nameInputs.forEach(input => input.addEventListener("input", validarCampos));
            passwordInputs.forEach(input => input.addEventListener("input", validarCampos));

            const form = popupContent.querySelector("form");
            form.addEventListener("submit", (event) => {
                event.preventDefault();

                if (validarFormulario(form)) {
                    form.submit();
                }
            });
        })
        .catch(error => console.error('Error al cargar la plantilla:', error));
}

function closePopup() {
    document.getElementById("popupContainer").classList.remove('show');
    setTimeout(() => {
        document.getElementById("popupContainer").style.display = "none";
    }, 300);
}

function validarCampos() {
    const form = this.closest('form');
    validarFormulario(form);
}

function validarFormulario(form) {
    const mailInput = form.querySelector("input[type='email']");
    const phoneInput = form.querySelector("input[name='Teléfono']");
    const addressInput = form.querySelector("input[name='Dirección']");
    const nameInput = form.querySelector("input[name='Name']");
    const passwordInput = form.querySelector("input[name='password']");
    const repasswordInput = form.querySelector("input[name='Repassword']");
    let errores = [];
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const phonePattern = /^[0-9]{1,10}$/;
    const addressPattern = /^[A-Za-z0-9\s]+$/;
    const namePattern = /^[A-Za-z\s]+$/;

    if (mailInput && !emailPattern.test(mailInput.value)) {
        errores.push("Por favor, ingresa un correo válido.");
    }

    if (phoneInput && !phonePattern.test(phoneInput.value)) {
        errores.push("El teléfono debe contener solo números y hasta 15 dígitos.");
    }

    if (addressInput && !addressPattern.test(addressInput.value)) {
        errores.push("La dirección no debe contener caracteres especiales.");
    }

    if (nameInput && !namePattern.test(nameInput.value)) {
        errores.push("El nombre debe contener solo letras.");
    }

    if (passwordInput && passwordInput.value.length < 4) {
        errores.push("La contraseña debe tener al menos 4 caracteres.");
    }

    if (repasswordInput && passwordInput.value !== repasswordInput.value) {
        errores.push("Las contraseñas no coinciden.");
    }

    mostrarErrores(errores);
    return errores.length === 0;
}

function mostrarErrores(errores) {
    let erroresDiv = document.getElementById("errores");
    if (!erroresDiv) {
        erroresDiv = document.createElement("div");
        erroresDiv.id = "errores";
        document.body.appendChild(erroresDiv);
    }
    erroresDiv.innerHTML = errores.join("<br>");
    erroresDiv.classList.toggle("oculto", errores.length === 0);

    if (errores.length > 0) {
        setTimeout(() => {
            erroresDiv.classList.add("oculto");
        }, 7000);
    }
}

function validarErroresIniciales() {
    const errores = document.getElementById("errores");
    if (errores && errores.textContent.trim()) {
        errores.classList.remove("oculto");
        setTimeout(() => {
            errores.classList.add("oculto");
        }, 7000);
    }
}
