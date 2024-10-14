// Agregamos interacción básica para mejorar la experiencia
document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('.nav-link');

    // Efecto de resaltar el enlace activo en el header
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navLinks.forEach(lnk => lnk.classList.remove('active'));
            link.classList.add('active');
        });
    });
});

function toggleMenu() {
    const navMenu = document.getElementById('nav-menu');
    if (navMenu.style.display === 'none' || navMenu.style.display === '') {
        navMenu.style.display = 'flex'; // Muestra el menú
    } else {
        navMenu.style.display = 'none'; // Oculta el menú
    }
}

document.getElementById("contact-button").addEventListener("click", function() {
    toggleMenu(); // Mostrar el menú si está oculto
    const contactButton = document.querySelector("nav #nav-menu .button:nth-child(6)"); // Selecciona el botón "Contáctenos"
    contactButton.click(); // Simula un clic en el botón "Contáctenos"
});