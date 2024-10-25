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

document.getElementById("contact-button").addEventListener("click", function () {
    toggleMenu(); // Mostrar el menú si está oculto
    const contactButton = document.querySelector("nav #nav-menu .button:nth-child(6)"); // Selecciona el botón "Contáctenos"
    contactButton.click(); // Simula un clic en el botón "Contáctenos"
<<<<<<< HEAD
});
=======
});


        function toggleChat() {
            const chatPopup = document.getElementById('chat-popup');
            chatPopup.classList.toggle('show');
        }

        async function sendMessage() {
            const userInput = document.getElementById('user-input');
            const message = userInput.value.trim();

            if (message === "") return;

            addMessage("user-message", message);

            const response = await fetch("/send_message", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();
            addMessage("bot-message", data.response);

            userInput.value = "";
            userInput.focus();
        }

        function addMessage(className, text) {
            const chatBody = document.getElementById('chat-body');
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message', className);
            messageDiv.textContent = text;
            chatBody.appendChild(messageDiv);
            chatBody.scrollTop = chatBody.scrollHeight;
        }
>>>>>>> d52d94d54f871a13081af0fd617c3b9e7a83fd0c
