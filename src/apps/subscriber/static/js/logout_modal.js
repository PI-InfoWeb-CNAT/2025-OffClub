document.addEventListener('DOMContentLoaded', function() {
    const logoutButton = document.getElementById('logout-button');

    if (logoutButton) {
        logoutButton.addEventListener('click', function(event) {
            event.preventDefault(); 
            const userConfirmed = confirm('Tem certeza que deseja sair?');
            if (userConfirmed) {
                window.location.href = this.href; 
            }
        });
    }
});