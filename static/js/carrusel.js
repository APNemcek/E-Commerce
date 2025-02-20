document.addEventListener('DOMContentLoaded', function () {
    const prevButton = document.querySelector('.boton_prev');
    const nextButton = document.querySelector('.boton_sig');
    const container = document.querySelector('.carrusel_container');
    const totalSlides = document.querySelectorAll('.carrusel_prod').length;
    let currentIndex = 0;

    function moverCarrusel() {
        container.style.transform = `translateX(-${currentIndex * 100}%)`;
    }

    prevButton.addEventListener('click', function () {
        currentIndex = (currentIndex === 0) ? totalSlides - 1 : currentIndex - 1;
        moverCarrusel();
    });

    nextButton.addEventListener('click', function () {
        currentIndex = (currentIndex === totalSlides - 1) ? 0 : currentIndex + 1;
        moverCarrusel();
    });

    setInterval(function () {
        currentIndex = (currentIndex === totalSlides - 1) ? 0 : currentIndex + 1;
        moverCarrusel();
    }, 10000);

    document.querySelectorAll(".precio_orig, .precio_desc").forEach(function(element) {
        const valor = parseInt(element.textContent.replace('$', '').replace(/\./g, ''), 10);
        element.textContent = `$${valor.toLocaleString('es-ES')}`;
    });
});