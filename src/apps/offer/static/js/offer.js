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

            const staticImageUrl = modal.querySelector('.tag-category img').src;

            modal.querySelector('.offer-image img').src = offer.image_url || staticImageUrl.replace('icons/discount.svg', 'offer_detail/offer-image.png');
            const priceInfo = modal.querySelector('.price-info');
            priceInfo.children[1].textContent = `R$ ${offer.price}`;
            priceInfo.children[3].textContent = `-${offer.discount}% (R$ ${offer.discount_value})`;
            priceInfo.children[5].textContent = `R$ ${offer.final_price}`;
            redeemButton.dataset.offerId = offer.id;

            modal.querySelector('.offer-content h2').textContent = offer.title;
            modal.querySelector('.shop-info .enterprise-image').src = offer.enterprise.logo_url || staticImageUrl.replace('icons/discount.svg', 'offer_detail/default_store.png');
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

    redeemButton.addEventListener('click', async (event) => {
        const offerId = event.currentTarget.dataset.offerId;
        console.log(`Simulando resgate para a oferta ${offerId}`);
        successToast.style.display = 'flex';
        successToast.style.bottom = '20px';
        setTimeout(() => {
           successToast.style.bottom = '-100px';
        }, 4000);
    });

    closeToastButton.addEventListener('click', () => {
        successToast.style.bottom = '-100px';
    });
});