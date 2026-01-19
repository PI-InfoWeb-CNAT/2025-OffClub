document.addEventListener('DOMContentLoaded', function () {
    const tabs = document.querySelectorAll('.how-it-works .tab-link');
    const contents = document.querySelectorAll('.how-it-works .tab-content');
    const sliderLines = document.querySelectorAll('.how-it-works .slider-line');

    function showTab(targetId) {
        contents.forEach(c => {
            if (c.id === targetId) {
                c.style.display = 'flex';
            } else {
                c.style.display = 'none';
            }
        });

        tabs.forEach((t) => {
            if (t.dataset.target === targetId) t.classList.add('active'); else t.classList.remove('active');
        });

        sliderLines.forEach((s, idx) => {
            if (s.id === 'slider-' + targetId.split('-')[1]) s.classList.add('active'); else s.classList.remove('active');
        });
    }

    // Inicialização: mostra a primeira aba
    if (tabs.length) {
        const initial = Array.from(tabs).find(t => t.classList.contains('active')) || tabs[0];
        showTab(initial.dataset.target || 'tab-1');

        tabs.forEach(t => {
            t.addEventListener('click', (e) => {
                const target = t.dataset.target;
                if (target) showTab(target);
            });
        });
    }
});