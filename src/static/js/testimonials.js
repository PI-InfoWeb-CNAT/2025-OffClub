document.addEventListener('DOMContentLoaded', function () {
    try {
        new Swiper('.reviews', {
            slidesPerView: 1,
            spaceBetween: 20,
            loop: true,
            autoplay: {
                delay: 5000,
                disableOnInteraction: false
            },
            pagination: {
                el: '.reviews-pagination',
                clickable: true
            },
            breakpoints: {
                640: { slidesPerView: 2, spaceBetween: 20 },
                900: { slidesPerView: 3, spaceBetween: 24 }
            }
        });
    } catch (e) {
        console.warn('Swiper testimonials init failed', e);
    }
});