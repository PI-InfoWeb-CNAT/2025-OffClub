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

/* Página que abre depois do resgate do cupom*/
const LOGIN_URL_FALLBACK = "/coupon";

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
   AJAX Filter System
========================= */

document.addEventListener("DOMContentLoaded", () => {
  const filterForm = document.getElementById("offer-filter-form");
  const resultsContainer = document.getElementById("offer-results");
  const loadingSpinner = document.getElementById("loading-spinner");
  const clearFiltersBtn = document.getElementById("clear-filters-btn");
  
  if (!filterForm || !resultsContainer) return;
  
  let debounceTimer = null;
  let currentPage = 1;
  
  // Função para mostrar/esconder loading
  function setLoading(isLoading) {
    if (loadingSpinner) {
      loadingSpinner.style.display = isLoading ? "flex" : "none";
    }
    resultsContainer.classList.toggle("loading", isLoading);
  }
  
  // Função para buscar ofertas via AJAX
  async function fetchOffers(page = 1) {
    const formData = new FormData(filterForm);
    const params = new URLSearchParams();
    
    // Adiciona os parâmetros do formulário
    for (const [key, value] of formData.entries()) {
      if (value) params.append(key, value);
    }
    
    // Adiciona página
    params.append("page", page);
    currentPage = page;
    
    const url = `${filterForm.action}?${params.toString()}`;
    
    setLoading(true);
    
    try {
      const response = await fetch(url, {
        headers: {
          "X-Requested-With": "XMLHttpRequest"
        }
      });
      
      if (!response.ok) throw new Error("Erro ao carregar ofertas");
      
      const html = await response.text();
      
      // Atualiza o container de resultados
      resultsContainer.innerHTML = html;
      
      // Reativa os event listeners para paginação
      attachPaginationListeners();
      
      // Atualiza URL sem recarregar a página
      const newUrl = `${window.location.pathname}?${params.toString()}`;
      window.history.pushState({ page }, "", newUrl);
      
    } catch (error) {
      console.error("Erro ao filtrar ofertas:", error);
      resultsContainer.innerHTML = `
        <div class="nothing_found">
          <p>Erro ao carregar ofertas. Tente novamente.</p>
        </div>
      `;
    } finally {
      setLoading(false);
    }
  }
  
  // Função para adicionar listeners na paginação dinâmica
  function attachPaginationListeners() {
    const paginationBtns = resultsContainer.querySelectorAll(".pagination-btn");
    paginationBtns.forEach(btn => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        const page = btn.dataset.page;
        if (page) fetchOffers(parseInt(page));
      });
    });
  }
  
  // Debounce para input de texto
  function debounce(func, delay = 400) {
    return function (...args) {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => func.apply(this, args), delay);
    };
  }
  
  // Event listener para mudanças no formulário
  const debouncedFetch = debounce(() => fetchOffers(1));
  
  // Input de texto (com debounce)
  const nameInput = filterForm.querySelector("#filter-name");
  if (nameInput) {
    nameInput.addEventListener("input", debouncedFetch);
  }
  
  // Slider de desconto (com debounce)
  const discountSlider = filterForm.querySelector("#min_discount");
  if (discountSlider) {
    discountSlider.addEventListener("change", () => fetchOffers(1));
  }
  
  // Checkboxes de categorias (imediato)
  const categoryCheckboxes = filterForm.querySelectorAll('input[name="categories"]');
  categoryCheckboxes.forEach(checkbox => {
    checkbox.addEventListener("change", () => fetchOffers(1));
  });
  
  // Botão de submit do formulário
  filterForm.addEventListener("submit", (e) => {
    e.preventDefault();
    fetchOffers(1);
  });
  
  // Botão de limpar filtros
  if (clearFiltersBtn) {
    clearFiltersBtn.addEventListener("click", () => {
      // Reseta o formulário
      filterForm.reset();
      
      // Reseta o slider para 0
      if (discountSlider) {
        discountSlider.value = 0;
        // Atualiza o bubble
        const bubble = filterForm.querySelector(".slider_bubble");
        if (bubble) {
          bubble.innerHTML = "0%";
          bubble.style.left = "calc(0% + 8px)";
        }
      }
      
      // Busca sem filtros
      fetchOffers(1);
    });
  }
  
  // Suporte ao botão voltar do navegador
  window.addEventListener("popstate", (e) => {
    if (e.state && e.state.page) {
      fetchOffers(e.state.page);
    }
  });
  
  // Inicializa listeners de paginação
  attachPaginationListeners();
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
            ? staticImageUrl.replace("icons/discount.svg", "empty_enterprise.svg")
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
