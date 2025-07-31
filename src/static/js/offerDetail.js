document.addEventListener('DOMContentLoaded', function () {
    const redeemButton = document.getElementById('redeem-button');
    const accessCouponsButton = document.getElementById('ascess-coupons-button');
    const successToast = document.getElementById('success-toast');
    const closeToast = document.getElementById('close-toast');
    const closeModalButton = document.getElementById('close-button-modal');
    const transparentBg = document.getElementById('transparent-bg');
    const offerModal = document.getElementById('offer-modal');

    closeModalButton.addEventListener('click', function () {
        offerModal.style.display = 'none';
        transparentBg.style.display = 'none';
    });

    closeToast.addEventListener('click', function () {
        successToast.style.display = 'none';
    });

    redeemButton.addEventListener('click', function () {
        accessCouponsButton.style.display = 'flex';
        successToast.style.display = 'flex';

        redeemButton.classList.add('disabled');
        redeemButton.disabled = true;

        setTimeout(() => {
            successToast.style.display = 'none';
        }, 5000);
    });
});
