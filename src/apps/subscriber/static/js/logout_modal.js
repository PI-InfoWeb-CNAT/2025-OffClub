document.addEventListener('DOMContentLoaded', function() {
    const logoutForm = document.getElementById('logout-button');

    if (logoutForm) {
        logoutForm.addEventListener('submit', function(event) {
            event.preventDefault(); 
            
            const userConfirmed = confirm('Tem certeza que deseja sair?');

            if (userConfirmed) {
                this.submit(); 
            }
        });
    }
});