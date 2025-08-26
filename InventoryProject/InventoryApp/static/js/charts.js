


const ctx = document.getElementById('salesChart').getContext('2d');

new Chart(ctx, {
    type: 'pie',
    data: {
        labels:{{ labels|safe }},
        datasets: [{
            label: 'Quantity',
            data: {{ data|safe }},
            backgroundColor: [
                'rgba(255, 99, 132, 0.6)',
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)'
            ]
        }]
    }
});