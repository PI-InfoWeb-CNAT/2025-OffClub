document.addEventListener('DOMContentLoaded', () => {
    const allRanges = document.querySelectorAll(".slider-wrap");
    allRanges.forEach(wrap => {
        const range = wrap.querySelector(".slider");
        const bubble = wrap.querySelector(".slider_bubble");

        function setBubble() {
            const val = range.value;
            const min = range.min || 0;
            const max = range.max || 100;
            const newVal = Number(((val - min) * 100) / (max - min));
            bubble.innerHTML = `${val}%`;
            bubble.style.left = `calc(${newVal}% + (${8 - newVal * 0.16}px))`;
        }
        
        range.addEventListener("input", setBubble);
        setBubble();
    });
});


var swiperCheap = new Swiper(".cheapSwiper", {
    slidesPerView: 'auto', 
    loop: true,             
    
    spaceBetween: 24,        
    grabCursor: true,        
    
    pagination: {
        el: ".cheap-swiper-pagination",
        clickable: true,
    },
    navigation: {
        nextEl: ".cheap-swiper-button-next",
        prevEl: ".cheap-swiper-button-prev",
    },
});


var swiperNear = new Swiper(".nearSwiper", {
    slidesPerView: 'auto',
    loop: true,
    spaceBetween: 24, 
    grabCursor: true,
    pagination: {
        el: ".near-swiper-pagination",
        clickable: true,
    },
    navigation: {
        nextEl: ".near-swiper-button-next",
        prevEl: ".near-swiper-button-prev",
    },
});

document.addEventListener('DOMContentLoaded', () => {
    const modalContainer = document.getElementById('transparent-bg');
    const closeModalButton = document.getElementById('close-button-modal');
    const redeemButton = document.getElementById('redeem-button');
    const successToast = document.getElementById('success-toast');
    const closeToastButton = document.getElementById('close-toast');

    if (!modalContainer) return;

    async function populateAndShowModal(offerId) {
        try {
            const response = await fetch(`/offer/json/${offerId}/`);
            if (!response.ok) throw new Error('Falha ao carregar dados da oferta.');
            
            const offer = await response.json();
            const modal = document.getElementById('offer-modal');

            // Imagem padrão para ofertas sem imagem
            const defaultOfferImage = '/static/imgs/default.png';
            const defaultEnterpriseImage = '/static/imgs/default.png';

            modal.querySelector('.offer-image img').src = offer.image_url || defaultOfferImage;
            const priceInfo = modal.querySelector('.price-info');
            priceInfo.children[1].textContent = `R$ ${offer.price}`;
            priceInfo.children[3].textContent = `-${offer.discount}% (R$ ${offer.discount_value})`;
            priceInfo.children[5].textContent = `R$ ${offer.final_price}`;
            redeemButton.dataset.offerId = offer.id;
            // desabilita botão se já resgatado ou sem unidades
            redeemButton.disabled = offer.already_redeemed || (offer.remaining_coupons <= 0);
            redeemButton.textContent = offer.already_redeemed ? 'RESGATADO' : 'RESGATAR';

            modal.querySelector('.offer-content h2').textContent = offer.title;
            modal.querySelector('.shop-info .enterprise-image').src = offer.enterprise.logo_url || defaultEnterpriseImage;
            modal.querySelector('.shop-info p').textContent = offer.enterprise.trade_name;
            
            modal.querySelector('.units p').textContent = `${offer.remaining_coupons} / ${offer.max_coupons}`;
            const progressBar = modal.querySelector('#coupon-progress');
            progressBar.value = offer.remaining_coupons;
            progressBar.max = offer.max_coupons;

            modal.querySelector('.details p').textContent = offer.description;
            modal.querySelector('.tag-category p').textContent = offer.category.name;
            const offerInfo = modal.querySelector('.offer-info');
            offerInfo.children[0].querySelector('p').textContent = `${offer.start_date} a ${offer.end_date}`;
            offerInfo.children[1].querySelector('p').textContent = `${offer.redemption_period_days} ${offer.redemption_period_days > 1 ? 'dias' : 'dia'}`;

            modalContainer.style.display = 'flex';
            document.body.classList.add('modal-opened');  
        } catch (error) {
            console.error("Erro:", error);
            alert("Não foi possível carregar os detalhes da oferta. Tente novamente.");
        }
    }

    const closeModal = () => {
        modalContainer.style.display = 'none';
        document.body.classList.remove('modal-opened');
    };

    document.body.addEventListener('click', (event) => {
        const offerCard = event.target.closest('.offer-card[data-offer-id]');
        if (offerCard) {
            event.preventDefault();
            const offerId = offerCard.dataset.offerId;
            populateAndShowModal(offerId);
        }
    });

    closeModalButton.addEventListener('click', closeModal);
    modalContainer.addEventListener('click', (event) => {
        if (event.target === modalContainer) {
            closeModal();
        }
    });

    // Helper para ler cookie (CSRF)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    redeemButton.addEventListener('click', async (event) => {
        const offerId = event.currentTarget.dataset.offerId;
        const csrftoken = getCookie('csrftoken');
        const modal = document.getElementById('offer-modal');
        const unitsP = modal.querySelector('.units p');
        const progressBar = modal.querySelector('#coupon-progress');

        // UI: disable button while processando
        redeemButton.disabled = true;
        redeemButton.classList.add('loading');

        try {
            const response = await fetch(`/offer/redeem/${offerId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json',
                },
            });

            const data = await response.json();

            if (response.ok && data.success) {
                // Toast com código do cupom
                const toastTitle = successToast.querySelector('div p:first-child');
                const toastBody = successToast.querySelector('div p:last-child');
                toastTitle.textContent = `Cupom ${data.coupon.code} resgatado com sucesso!`;
                const expDate = new Date(data.coupon.expiration_date).toLocaleDateString();
                toastBody.innerHTML = `Válido até ${expDate}. Acesse <a href=\"/profile/coupons/\">Meus Cupons</a> para utilizá-lo`;

                successToast.style.display = 'flex';
                successToast.style.bottom = '20px';
                setTimeout(() => {
                    successToast.style.bottom = '-100px';
                }, 4000);

                // Atualiza botão e barras
                redeemButton.textContent = 'RESGATADO';
                redeemButton.disabled = true;

                if (progressBar && !isNaN(progressBar.value)) {
                    progressBar.value = Math.max(0, Number(progressBar.value) - 1);
                }
                if (unitsP) {
                    // atualiza contador mostrado (ex: "10 / 100")
                    const parts = unitsP.textContent.split('/').map(s => s.trim());
                    if (parts.length === 2) {
                        const current = Number(parts[0]) - 1;
                        unitsP.textContent = `${Math.max(0, current)} / ${parts[1]}`;
                    }
                }
            } else {
                alert(data.error || 'Erro ao resgatar cupom.');
                redeemButton.disabled = false;
            }
        } catch (error) {
            console.error('Erro no resgate:', error);
            alert('Erro ao resgatar cupom. Tente novamente.');
            redeemButton.disabled = false;
        } finally {
            redeemButton.classList.remove('loading');
        }
    });

    closeToastButton.addEventListener('click', () => {
        successToast.style.bottom = '-100px';
    });
});