const allRanges = document.querySelectorAll(".slider-wrap");
allRanges.forEach(wrap => {
    const range = wrap.querySelector(".slider");
    const bubble = wrap.querySelector(".slider_bubble");
    range.addEventListener("input", () => {
        setBubble(range, bubble);
    });
    setBubble(range, bubble);
});
function setBubble(range, bubble) {
    const val = range.value;
    const min = range.min ? range.min : 0;
    const max = range.max ? range.max : 100;
    const newVal = Number(((val - min) * 100) / (max - min));
    bubble.innerHTML = val;
    // Sorta magic numbers based on size of the native UI thumb
    bubble.style.left = `calc(${newVal}% + (${8 - newVal * 0.15}px))`;
}

var swiper = new Swiper(".cheapSwiper", {
  slidesPerView: 4,
  spaceBetween: 4,
  slidesPerGroup: 4,
  loop: true,
  loopFillGroupWithBlank: true,
  pagination: {
    el: ".cheap-swiper-pagination",
    clickable: true,
  },
  navigation: {
    nextEl: ".cheap-swiper-button-next",
    prevEl: ".cheap-swiper-button-prev",
  },
});

var swiper = new Swiper(".nearSwiper", {
  slidesPerView: 4,
  spaceBetween: 4,
  slidesPerGroup: 4,
  loop: true,
  loopFillGroupWithBlank: true,
  pagination: {
    el: ".near-swiper-pagination",
    clickable: true,
  },
  navigation: {
    nextEl: ".near-swiper-button-next",
    prevEl: ".near-swiper-button-prev",
  },
});