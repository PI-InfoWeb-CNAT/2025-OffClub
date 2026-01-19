// Inicializa o slider de categorias usando Swiper
document.addEventListener('DOMContentLoaded', function () {
    try {
        new Swiper('.categories-slider', {
            slidesPerView: 'auto',
            spaceBetween: 12,
            freeMode: true,
            grabCursor: true,
            // small responsive tweaks
            breakpoints: {
                640: { slidesPerView: 3 },
                900: { slidesPerView: 5 }
            }
        });
    } catch (e) {
        // Swiper não disponível ou erro de inicialização
        console.warn('Swiper categories init failed', e);
    }
});