document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("modal-avaliacao");
    const starsContainer = document.getElementById("stars-container");
    const hiddenStarsInput = document.getElementById("id_stars");
    const hiddenCouponInput = document.getElementById("id_coupon_id");
    const cancelarBtn = document.getElementById("cancelar-btn");
    const form = document.getElementById("evaluate-form");
    const formErrorsContainer = document.getElementById("form-errors");

    let selectedStars = 0;

    // Atualiza visualmente as estrelas
    function updateStars(value) {
        const stars = starsContainer.querySelectorAll("span");
        stars.forEach((star, index) => {
            if (index < value) star.classList.add("active");
            else star.classList.remove("active");
        });
    }

    // Clique em uma estrela
    starsContainer.addEventListener("click", (event) => {
        const star = event.target.closest("span");
        if (!star) return;

        selectedStars = parseInt(star.getAttribute("data-value"));
        hiddenStarsInput.value = selectedStars;
        updateStars(selectedStars);
    });

    // Abre o modal
    document.querySelectorAll(".open_modal").forEach(button => {
        button.addEventListener("click", () => {
            const couponId = button.getAttribute("data-coupon-id");
            hiddenCouponInput.value = couponId;
            modal.classList.add("show");
        });
    });

    // Fecha modal ao clicar em cancelar
    cancelarBtn.addEventListener("click", () => {
        closeModal();
    });

    // Fecha clicando fora do modal
    window.addEventListener("click", (event) => {
        if (event.target === modal) {
            closeModal();
        }
    });

    function closeModal() {
        modal.classList.remove("show");
        hiddenStarsInput.value = "";
        hiddenCouponInput.value = "";
        selectedStars = 0;
        updateStars(0);
        formErrorsContainer.innerHTML = "";
    }

    // Envio do formulário via AJAX
    form.addEventListener("submit", function (event) {
        event.preventDefault(); // previne envio padrão

        const formData = new FormData(form);

        fetch(form.action, {
            method: "POST",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": formData.get("csrfmiddlewaretoken")
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                closeModal();
                // opcional: mostrar mensagem de sucesso na tela
                alert("Avaliação registrada com sucesso!");
            } else if (data.errors) {
                // mostra os erros no modal
                formErrorsContainer.innerHTML = "";
                for (const [field, messages] of Object.entries(data.errors)) {
                    messages.forEach(msg => {
                        const li = document.createElement("li");
                        li.textContent = msg;
                        formErrorsContainer.appendChild(li);
                    });
                }
            }
        })
        .catch(error => {
            console.error("Erro ao enviar avaliação:", error);
        });
    });
});
