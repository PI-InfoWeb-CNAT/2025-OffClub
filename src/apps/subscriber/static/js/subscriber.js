document.addEventListener('DOMContentLoaded', function() {
    const activeCouponsSection = document.querySelector('.active-coupons');
    if (!activeCouponsSection) return;

    const readMoreButton = activeCouponsSection.querySelector('.read-more');
    const extraCouponsWrapper = activeCouponsSection.querySelector('.extra-coupons-wrapper');

    if (readMoreButton && extraCouponsWrapper) {
        readMoreButton.addEventListener('click', function() {
            this.classList.toggle('expanded');
            const buttonText = this.querySelector('p');

            if (this.classList.contains('expanded')) {
                extraCouponsWrapper.style.maxHeight = extraCouponsWrapper.scrollHeight + 'px';
                buttonText.textContent = 'Ver menos';
            } else {
                extraCouponsWrapper.style.maxHeight = '0px';
                buttonText.textContent = 'Ver mais';
            }
        });
    }
    const usedCouponsSection = document.querySelector('.used-coupons');
    if (usedCouponsSection) {
        const yearSelect = document.getElementById('year');
        const monthSections = document.querySelectorAll('.month-section');

        if (yearSelect && monthSections.length > 0){
            function filterCoupons(){
                const selectedYear = yearSelect.value;
                monthSections.forEach(section => {
                    const sectionYear = section.dataset.year;
                    if (sectionYear == selectedYear){
                        section.style.display = 'block';
                    }
                    else{
                        section.style.display = 'none';
                    }
                })        
            }
            yearSelect.addEventListener('change', filterCoupons);
            filterCoupons();
        }
    }
});