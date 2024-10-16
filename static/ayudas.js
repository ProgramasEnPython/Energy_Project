// script.js
document.querySelectorAll('.provider').forEach(item => {
    item.addEventListener('click', event => {
        // Cambiar color del texto al hacer clic
        item.style.color = item.style.color === 'blue' ? 'black' : 'blue';
    });
});

// Cambiar el color del título al hacer scroll
window.addEventListener('scroll', () => {
    const providerTitle = document.querySelector('.provider-title');
    if (window.scrollY > 100) {
        providerTitle.style.color = 'green'; // Cambiar color cuando se hace scroll
    } else {
        providerTitle.style.color = 'black'; // Color original
    }
});