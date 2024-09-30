document.getElementById('energyForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const formData = new FormData(this);
    
    fetch('/calcular', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(html => {
        document.body.innerHTML = html;
    })
    .catch(error => console.error('Error:', error));
});


/*
ESTE CÓDIGO
-Escucha el envío del formulario y previene el comportamiento por defecto.
-Recoge los datos del formulario y los envía asíncronamente a un endpoint específico (/calcular).
-Reemplaza el contenido de la página actual con la respuesta del servidor sin recargar la página.
-Maneja cualquier error que pueda ocurrir durante el proceso de envío.
 */