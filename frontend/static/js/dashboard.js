const ctx = document.getElementById('graficoFaturamento');

new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai'],
        datasets: [{
            label: 'Faturamento',
            data: [1200, 1900, 3000, 500, 2000],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true
    }
});