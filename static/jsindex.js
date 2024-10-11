document.addEventListener('DOMContentLoaded', function () {
    // Gráfico de Barras
    var ctxBarras = document.getElementById('graficoBarras').getContext('2d');
    var graficoBarras = new Chart(ctxBarras, {
        type: 'bar',
        data: {
            labels: ['Solar', 'Eólica', 'Hidroeléctrica'],
            datasets: [{
                label: 'Producción (GWh)',
                data: [120, 150, 100],
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false // Permite que el gráfico ajuste su altura
        }
    });

    // Gráfico de Torta
    var ctxTorta = document.getElementById('graficoTorta').getContext('2d');
    var graficoTorta = new Chart(ctxTorta, {
        type: 'pie',
        data: {
            labels: ['Solar', 'Eólica', 'Hidroeléctrica'],
            datasets: [{
                data: [120, 150, 100],
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false // Permite que el gráfico ajuste su altura
        }
    });

    // Gráfico de Líneas
    var ctxLineas = document.getElementById('graficoLineas').getContext('2d');
    var graficoLineas = new Chart(ctxLineas, {
        type: 'line',
        data: {
            labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo'],
            datasets: [{
                label: 'Producción (GWh)',
                data: [100, 120, 150, 130, 170],
                borderColor: '#36A2EB',
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false // Permite que el gráfico ajuste su altura
        }
    });
});

