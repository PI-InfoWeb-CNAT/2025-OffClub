document.addEventListener('DOMContentLoaded', function () {
    const redeemButton = document.getElementById('redeem-button');
    const accessCouponsButton = document.getElementById('ascess-coupons-button');
    const successToast = document.getElementById('success-toast');
    const closeToast = document.getElementById('close-toast');
    const closeModalButton = document.getElementById('close-button-modal');
    const transparentBg = document.getElementById('transparent-bg');
    const offerModal = document.getElementById('offer-modal');

    // Evento para esconder o modal
    closeModalButton.addEventListener('click', function () {
        offerModal.style.display = 'none';
        transparentBg.style.display = 'none';
    });

    // Evento para fechar a notificação de sucesso
    closeToast.addEventListener('click', function () {
        successToast.style.display = 'none';
    });

    // Evento de clique no botão "RESGATAR"
    redeemButton.addEventListener('click', function () {
        // Mostra notificação de sucesso e botão de acessar cupons
        accessCouponsButton.style.display = 'flex';
        successToast.style.display = 'flex';

        // Desativa botão visualmente e funcionalmente
        redeemButton.classList.add('disabled');
        redeemButton.disabled = true;

        // Oculta notificação de sucesso após 5 segundos
        setTimeout(() => {
            successToast.style.display = 'none';
        }, 5000);
    });
});
