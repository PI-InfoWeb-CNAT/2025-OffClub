/* =========================
   Helpers
========================= */

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

/* Ajuste se sua URL de login não for essa */
const LOGIN_URL_FALLBACK = "/subscriber/login/";

/* =========================
   Slider bubble
========================= */

document.addEventListener("DOMContentLoaded", () => {
  const allRanges = document.querySelectorAll(".slider-wrap");
  allRanges.forEach((wrap) => {
    const range = wrap.querySelector(".slider");
    const bubble = wrap.querySelector(".slider_bubble");
    if (!range || !bubble) return;

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

/* =========================
   Swipers
========================= */

var swiperCheap = new Swiper(".cheapSwiper", {
  slidesPerView: "auto",
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
  slidesPerView: "auto",
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

/* =========================
   Modal + Offer Detail + Redeem
========================= */

document.addEventListener("DOMContentLoaded", () => {
  const modalContainer = document.getElementById("transparent-bg");
  const closeModalButton = document.getElementById("close-button-modal");
  const redeemButton = document.getElementById("redeem-button");
  const successToast = document.getElementById("success-toast");
  const closeToastButton = document.getElementById("close-toast");
  const accessCouponsButton = document.getElementById("ascess-coupons-button");

  if (!modalContainer) return;

  const csrftoken = getCookie("csrftoken");

  function showToast() {
    if (!successToast) return;
    successToast.style.display = "flex";
    successToast.style.bottom = "20px";
    setTimeout(() => {
      successToast.style.bottom = "-100px";
    }, 4000);
  }

  function hideToast() {
    if (!successToast) return;
    successToast.style.bottom = "-100px";
  }

  async function populateAndShowModal(offerId) {
    try {
      const response = await fetch(`/offer/json/${offerId}/`, {
        headers: { "X-Requested-With": "XMLHttpRequest" },
      });

      if (!response.ok) throw new Error("Falha ao carregar dados da oferta.");

      const offer = await response.json();
      const modal = document.getElementById("offer-modal");
      if (!modal) throw new Error("Modal não encontrado.");

      const staticImageUrl = modal.querySelector(".tag-category img")?.src || "";

      // Imagem da oferta
      const offerImg = modal.querySelector(".offer-image img");
      if (offerImg) {
        offerImg.src =
          offer.image_url ||
          (staticImageUrl
            ? staticImageUrl.replace("icons/discount.svg", "offer_detail/offer-image.png")
            : offerImg.src);
      }

      // Preços
      const priceInfo = modal.querySelector(".price-info");
      if (priceInfo && priceInfo.children.length >= 6) {
        priceInfo.children[1].textContent = `R$ ${offer.price}`;
        priceInfo.children[3].textContent = `-${offer.discount}% (R$ ${offer.discount_value})`;
        priceInfo.children[5].textContent = `R$ ${offer.final_price}`;
      }

      // Guarda offerId no botão (para resgate)
      if (redeemButton) {
        redeemButton.dataset.offerId = offer.id;

        // Se o template tiver data-redeem-url, mantém.
        // Se não tiver (modal dinâmico), definimos pelo padrão:
        // /offer/<uuid>/redeem/
        if (!redeemButton.dataset.redeemUrl) {
          redeemButton.dataset.redeemUrl = `/offer/${offer.id}/redeem/`;
        }
      }

      // Título
      const titleEl = modal.querySelector(".offer-content h2");
      if (titleEl) titleEl.textContent = offer.title;

      // Logo e nome empresa
      const enterpriseImg = modal.querySelector(".shop-info .enterprise-image");
      if (enterpriseImg) {
        enterpriseImg.src =
          offer.enterprise?.logo_url ||
          (staticImageUrl
            ? staticImageUrl.replace("icons/discount.svg", "offer_detail/default_store.png")
            : enterpriseImg.src);
      }
      const enterpriseName = modal.querySelector(".shop-info p");
      if (enterpriseName) enterpriseName.textContent = offer.enterprise?.trade_name || "";

      // Unidades restantes + progress
      const unitsP = modal.querySelector(".units p");
      if (unitsP) unitsP.textContent = `${offer.remaining_coupons} / ${offer.max_coupons}`;

      const progressBar = modal.querySelector("#coupon-progress");
      if (progressBar) {
        progressBar.value = offer.remaining_coupons;
        progressBar.max = offer.max_coupons;
      }

      // Descrição
      const descP = modal.querySelector(".details p");
      if (descP) descP.textContent = offer.description || "";

      // Categoria
      const catP = modal.querySelector(".tag-category p");
      if (catP) catP.textContent = offer.category?.name || "Sem Categoria";

      // Datas / período
      const offerInfo = modal.querySelector(".offer-info");
      if (offerInfo && offerInfo.children.length >= 2) {
        const p1 = offerInfo.children[0].querySelector("p");
        const p2 = offerInfo.children[1].querySelector("p");
        if (p1) p1.textContent = `${offer.start_date} a ${offer.end_date}`;
        if (p2) {
          const days = offer.redemption_period_days || 0;
          p2.textContent = `${days} ${days > 1 ? "dias" : "dia"}`;
        }
      }

      // Exibe modal
      modalContainer.style.display = "flex";
      document.body.classList.add("modal-opened");
    } catch (error) {
      console.error("Erro:", error);
      alert("Não foi possível carregar os detalhes da oferta. Tente novamente.");
    }
  }

  const closeModal = () => {
    modalContainer.style.display = "none";
    document.body.classList.remove("modal-opened");
  };

  // Abre modal ao clicar no card (mantido)
  document.body.addEventListener("click", (event) => {
    const offerCard = event.target.closest(".offer-card[data-offer-id]");
    if (offerCard) {
      event.preventDefault();
      const offerId = offerCard.dataset.offerId;
      populateAndShowModal(offerId);
    }
  });

  // Fecha modal
  if (closeModalButton) closeModalButton.addEventListener("click", closeModal);
  modalContainer.addEventListener("click", (event) => {
    if (event.target === modalContainer) closeModal();
  });

  // Fecha toast
  if (closeToastButton) closeToastButton.addEventListener("click", hideToast);

  // =========================
  // Resgatar cupom (POST real)
  // =========================
  if (redeemButton) {
    redeemButton.addEventListener("click", async (event) => {
      event.preventDefault();

      const offerId = redeemButton.dataset.offerId;
      const redeemUrl = redeemButton.dataset.redeemUrl;

      if (!offerId || !redeemUrl) {
        alert("Não foi possível identificar a oferta para resgate (faltou offerId/redeemUrl).");
        return;
      }

      redeemButton.disabled = true;

      try {
        const response = await fetch(redeemUrl, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
            "X-Requested-With": "XMLHttpRequest",
          },
          body: JSON.stringify({}),
        });

        // Se não retornar JSON: normalmente redirect para login
        const contentType = response.headers.get("content-type") || "";
        if (!contentType.includes("application/json")) {
          window.location.href = LOGIN_URL_FALLBACK;
          return;
        }

        const data = await response.json();

        if (!response.ok || !data.ok) {
          alert(data.error || "Não foi possível resgatar o cupom.");
          redeemButton.disabled = false;
          return;
        }

        // Atualiza unidades + progressbar
        const unitsP = document.querySelector(".units p");
        const progressBar = document.querySelector("#coupon-progress");
        if (unitsP && progressBar) {
          unitsP.textContent = `${data.remaining_coupons} / ${data.max_coupons}`;
          progressBar.max = data.max_coupons;
          progressBar.value = data.remaining_coupons;
        }

        // UI: esconder resgatar / mostrar acessar cupons
        redeemButton.style.display = "none";
        if (accessCouponsButton) {
          accessCouponsButton.style.display = "inline-flex";
        }

        showToast();
      } catch (err) {
        console.error(err);
        alert("Erro inesperado ao resgatar o cupom.");
        redeemButton.disabled = false;
      }
    });
  }
});
