const totalSlides = 10; 
const slideInicial = Math.floor(totalSlides / 2); 
const categoriesSwiper = new Swiper('.categories-slider', {
  autoplay: {
    delay: 0,
    disableOnInteraction: false, 
    pauseOnMouseEnter: true,    
  },
  speed: 5000,

  loop: true,

  centeredSlides: true,  
  initialSlide: slideInicial,

  
  slidesPerView: 6.5, 
  spaceBetween: 16,
  grabCursor: true,

  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
});