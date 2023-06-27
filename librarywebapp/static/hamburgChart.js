// Get the data for the chart
var borrowers = [];
var loanCounts = [];

{% for b in borrowersummary %}
    borrowers.push("{{ b[0] }}");
    loanCounts.push({{ b[2] }});
{% endfor %}

// Create the chart
var ctx = document.getElementById('hamburgChart').getContext('2d');
var chart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: borrowers,
        datasets: [{
            label: 'Times of Loans',
            data: loanCounts,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
