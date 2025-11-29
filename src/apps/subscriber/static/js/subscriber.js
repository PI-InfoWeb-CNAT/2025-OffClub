document.addEventListener('DOMContentLoaded', function() {
    const filterMonth = document.getElementById('filter-month');
    const filterYear = document.getElementById('filter-year');
    const filterOrder = document.getElementById('filter-order');
    
    const containerUsed = document.getElementById('container-used');
    const containerActive = document.getElementById('container-active');

    function applyFilters() {
        const selectedMonth = filterMonth.value;
        const selectedYear = filterYear.value;
        const noResultsMsg = document.getElementById('no-filter-results');

        const usedItems = containerUsed.querySelectorAll('.coupon-item');
        
        let visibleCount = 0; 

        usedItems.forEach(item => {
            const itemMonth = item.getAttribute('data-month');
            const itemYear = item.getAttribute('data-year');

            let matchMonth = (selectedMonth === 'all') || (selectedMonth === itemMonth);
            let matchYear = (selectedYear === 'all') || (selectedYear === itemYear);

            if (matchMonth && matchYear) {
                item.style.display = ''; 
                visibleCount++; 
            } else {
                item.style.display = 'none'; 
            }
        });

        if (visibleCount === 0) {
            if(noResultsMsg) noResultsMsg.style.display = 'block';
        } else {
            if(noResultsMsg) noResultsMsg.style.display = 'none';
        }
    }

    function applySort() {
        const order = filterOrder.value; 
        const sortContainer = (container) => {
            if (!container) return;

            const items = Array.from(container.querySelectorAll('.coupon-item'));

            items.sort((a, b) => {
                const timeA = parseInt(a.getAttribute('data-timestamp')) || 0;
                const timeB = parseInt(b.getAttribute('data-timestamp')) || 0;

                if (order === 'recent') {
                    return timeB - timeA; 
                } else {
                    return timeA - timeB; 
                }
            });
            items.forEach(item => container.appendChild(item));
        };
        sortContainer(containerUsed);
        sortContainer(containerActive);
    }
    if(filterMonth) {
        filterMonth.addEventListener('change', applyFilters);
    }
    if(filterYear) {
        filterYear.addEventListener('change', applyFilters);
    }
    if(filterOrder) {
        filterOrder.addEventListener('change', applySort);
    }
});