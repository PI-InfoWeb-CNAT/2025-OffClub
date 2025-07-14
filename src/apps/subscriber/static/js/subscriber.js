var button = document.querySelector('.read-more');
var text = button.querySelector('p');
var moreCoupons = document.querySelector('.more-coupons');

button.addEventListener('click', function () {
    const isExpanded = moreCoupons.classList.toggle('show');

    if (isExpanded) {
        moreCoupons.style.maxHeight = moreCoupons.scrollHeight + 'px';
        text.textContent = 'Ver menos';
        button.classList.add('expanded');
    } else {
        moreCoupons.style.maxHeight = '0';
        text.textContent = 'Ver mais';
        button.classList.remove('expanded');
    }
});

const select = document.getElementById('year');
const coupons = document.querySelectorAll('.months .coupon');

select.addEventListener('change', () => {
  const selected = select.value;

  coupons.forEach(coupon => {
    if (selected === 'todos' || coupon.dataset.year === selected) {
      coupon.style.display = '';
    } else {
      coupon.style.display = 'none';
    }
  });
});
