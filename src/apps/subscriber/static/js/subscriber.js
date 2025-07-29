document.addEventListener('DOMContentLoaded', function() {
    const activeCouponsSection = document.querySelector('.active-coupons');
    if (!activeCouponsSection) return;

    const readMoreButton = activeCouponsSection.querySelector('.read-more');
    const extraCouponsWrapper = activeCouponsSection.querySelector('.extra-coupons-wrapper');

    if (readMoreButton && extraCouponsWrapper) {
        readMoreButton.addEventListener('click', function() {
            // Adiciona/remove a classe no botão (para a seta e para guardar o estado)
            this.classList.toggle('expanded');
            const buttonText = this.querySelector('p');

            // Verifica se o botão está no estado "expandido"
            if (this.classList.contains('expanded')) {
                // EXPANDE: Define a altura máxima para a altura EXATA do conteúdo
                extraCouponsWrapper.style.maxHeight = extraCouponsWrapper.scrollHeight + 'px';
                buttonText.textContent = 'Ver menos';
            } else {
                // RECOLHE: Define a altura máxima de volta para 0
                extraCouponsWrapper.style.maxHeight = '0px';
                buttonText.textContent = 'Ver mais';
            }
        });
    }
});