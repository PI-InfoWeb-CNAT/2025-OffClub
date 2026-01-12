/**
 * Filtro de ofertas com AJAX - sem recarregar a página
 */
document.addEventListener('DOMContentLoaded', () => {
    const filterForm = document.getElementById('filter-form');
    const offersContainer = document.getElementById('offer_filter_container');
    const resultsCount = document.getElementById('results-count');
    const paginationContainer = document.getElementById('pagination-container');
    const loadingIndicator = document.getElementById('loading-indicator');
    const applyFiltersBtn = document.getElementById('apply-filters');
    const clearFiltersBtn = document.getElementById('clear-filters');
    const searchBtn = document.getElementById('search-btn');
    const searchInput = document.getElementById('search-name');
    const slider = document.getElementById('min_discount');
    
    let currentPage = 1;
    let debounceTimer;
    let isLoading = false;

    // Inicializa o slider com visual feedback
    initSlider();

    /**
     * Coleta os valores atuais dos filtros
     */
    function getFilterValues() {
        const formData = new FormData(filterForm);
        const params = new URLSearchParams();
        
        const name = formData.get('name');
        if (name && name.trim()) params.append('name', name.trim());
        
        // Desconto mínimo (só envia se > 0)
        const minDiscount = formData.get('min_discount');
        if (minDiscount && parseInt(minDiscount) > 0) {
            params.append('min_discount', minDiscount);
        }
        
        const startDate = formData.get('start_date');
        const endDate = formData.get('end_date');
        if (startDate) params.append('start_date', startDate);
        if (endDate) params.append('end_date', endDate);
        
        const categories = formData.getAll('categories');
        categories.forEach(cat => params.append('categories', cat));
        
        params.append('page', currentPage);
        
        return params;
    }

    /**
     * Faz a requisição AJAX para filtrar ofertas
     */
    async function fetchOffers() {
        if (isLoading) return;
        isLoading = true;
        
        const params = getFilterValues();
        
        // Mostra loading
        loadingIndicator.style.display = 'flex';
        offersContainer.style.opacity = '0.4';
        offersContainer.style.pointerEvents = 'none';

        applyFiltersBtn.disabled = true;
        applyFiltersBtn.innerHTML = '<span class="btn-spinner"></span> Buscando...';
        
        try {
            const response = await fetch(`/offer/filter/?${params.toString()}`);
            if (!response.ok) throw new Error('Erro ao carregar ofertas');
            
            const data = await response.json();
            
            offersContainer.style.opacity = '0';
            
            setTimeout(() => {
                offersContainer.innerHTML = data.html;
                offersContainer.style.opacity = '1';
            }, 150);

            updateResultsCount(data);
            
            updatePagination(data);
            
        } catch (error) {
            console.error('Erro:', error);
            offersContainer.innerHTML = `
                <div class="nothing_found">
                    <svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" style="opacity: 0.5; color: var(--brand-orange);">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="8" x2="12" y2="12"></line>
                        <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                    <p>Erro ao carregar ofertas. Tente novamente.</p>
                </div>
            `;
        } finally {
            loadingIndicator.style.display = 'none';
            offersContainer.style.opacity = '1';
            offersContainer.style.pointerEvents = 'auto';
            
            applyFiltersBtn.disabled = false;
            applyFiltersBtn.innerHTML = 'Aplicar Filtros';
            
            isLoading = false;
        }
    }

    /**
     * Atualiza o contador de resultados
     */
    function updateResultsCount(data) {
        if (data.count > 0) {
            const start = (data.current_page - 1) * 8 + 1;
            const end = Math.min(data.current_page * 8, data.count);
            resultsCount.innerHTML = `Exibindo <span>${start} - ${end}</span> de <span>${data.count}</span> resultados`;
        } else {
            resultsCount.innerHTML = '<span>Nenhum</span> resultado encontrado';
        }
    }

    /**
     * Atualiza os botões de paginação
     */
    function updatePagination(data) {
        if (data.total_pages <= 1) {
            paginationContainer.innerHTML = '';
            return;
        }
        
        let paginationHTML = '';
        
        if (data.has_previous) {
            paginationHTML += `<button class="pagination-btn" data-page="${data.current_page - 1}">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="15 18 9 12 15 6"></polyline>
                </svg>
                Anterior
            </button>`;
        }
        
        paginationHTML += `<span class="pagination-info">Página <span>${data.current_page}</span> de <span>${data.total_pages}</span></span>`;
        
        if (data.has_next) {
            paginationHTML += `<button class="pagination-btn" data-page="${data.current_page + 1}">
                Próxima
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="9 18 15 12 9 6"></polyline>
                </svg>
            </button>`;
        }
        
        paginationContainer.innerHTML = paginationHTML;
        
        // Re-adiciona event listeners aos novos botões
        paginationContainer.querySelectorAll('.pagination-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                currentPage = parseInt(btn.dataset.page);
                fetchOffers();
                document.getElementById('offer_search').scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start'
                });
            });
        });
    }

    /**
     * Inicializa o slider de desconto com visual feedback
     */
    function initSlider() {
        if (!slider) return;
        
        const bubble = document.querySelector('.slider_bubble');
        
        function updateSlider() {
            const val = slider.value;
            const min = slider.min || 0;
            const max = slider.max || 100;
            const percentage = ((val - min) / (max - min)) * 100;
            
            if (bubble) {
                bubble.textContent = `${val}%`;
                bubble.style.left = `calc(${percentage}% + (${8 - percentage * 0.16}px))`;
            }

            slider.style.background = `linear-gradient(to right, var(--brand-orange) 0%, var(--brand-orange) ${percentage}%, #444 ${percentage}%, #444 100%)`;
        }
        
        slider.addEventListener('input', updateSlider);
        updateSlider();
    }

    /**
     * Limpa todos os filtros
     */
    function clearFilters() {
        clearFiltersBtn.style.transform = 'scale(0.95)';
        setTimeout(() => clearFiltersBtn.style.transform = '', 150);
        
        searchInput.value = '';
 
        slider.value = 0;
        initSlider();
        
        document.getElementById('start_date').value = '';
        document.getElementById('end_date').value = '';
        
        filterForm.querySelectorAll('input[type="checkbox"]').forEach(cb => {
            cb.checked = false;
        });
        
        currentPage = 1;
        fetchOffers();
    }

    /**
     * Conta filtros ativos para feedback visual
     */
    function getActiveFiltersCount() {
        let count = 0;
        
        if (searchInput.value.trim()) count++;
        if (parseInt(slider.value) > 0) count++;
        if (document.getElementById('start_date').value) count++;
        if (document.getElementById('end_date').value) count++;
        
        const checkedCategories = filterForm.querySelectorAll('input[name="categories"]:checked');
        count += checkedCategories.length;
        
        return count;
    }

    /**
     * Atualiza o texto do botão limpar
     */
    function updateClearButton() {
        const count = getActiveFiltersCount();
        if (count > 0) {
            clearFiltersBtn.textContent = `Limpar (${count})`;
            clearFiltersBtn.style.opacity = '1';
        } else {
            clearFiltersBtn.textContent = 'Limpar';
            clearFiltersBtn.style.opacity = '0.6';
        }
    }

    // ============================================
    // EVENT LISTENERS
    // ============================================

    applyFiltersBtn.addEventListener('click', () => {
        currentPage = 1;
        fetchOffers();
    });

    clearFiltersBtn.addEventListener('click', clearFilters);

    searchBtn.addEventListener('click', () => {
        currentPage = 1;
        fetchOffers();
    });

    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            currentPage = 1;
            fetchOffers();
        }
    });

    // Atualiza botão limpar quando inputs mudam
    searchInput.addEventListener('input', updateClearButton);
    slider.addEventListener('input', updateClearButton);
    document.getElementById('start_date').addEventListener('change', updateClearButton);
    document.getElementById('end_date').addEventListener('change', updateClearButton);

    filterForm.querySelectorAll('input[name="categories"]').forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            updateClearButton();
            currentPage = 1;
            // Debounce para evitar múltiplas requisições
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(fetchOffers, 400);
        });
    });

    slider.addEventListener('change', () => {
        currentPage = 1;
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(fetchOffers, 600);
    });

    document.getElementById('start_date').addEventListener('change', () => {
        currentPage = 1;
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(fetchOffers, 400);
    });
    
    document.getElementById('end_date').addEventListener('change', () => {
        currentPage = 1;
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(fetchOffers, 400);
    });

    paginationContainer.querySelectorAll('.pagination-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            currentPage = parseInt(btn.dataset.page);
            fetchOffers();
            document.getElementById('offer_search').scrollIntoView({ 
                behavior: 'smooth',
                block: 'start'
            });
        });
    });

    updateClearButton();
});
