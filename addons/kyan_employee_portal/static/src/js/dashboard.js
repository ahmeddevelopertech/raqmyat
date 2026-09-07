document.addEventListener('DOMContentLoaded', function () {
    // Fetch chart data from the embedded JSON script
    var chartDataElement = document.getElementById('chart-data');
    var chartData = JSON.parse(chartDataElement.textContent);

    // Configuration for the Bar Chart
    var barCtx = document.getElementById('summaryChart').getContext('2d');

    // Add background color to the chart area
    barCtx.canvas.parentNode.style.backgroundColor = '#9EC7E3'; // Set background color for chart area

    var barChart = new Chart(barCtx, {
        type: 'bar',
        data: {
            labels: ['Remaining Leaves', 'Consumed Leaves', 'Total Expense', 'Salary Advance', 'Loan', 'Accident/Incident'],
            datasets: [{
                label: 'Employee Details',
                data: [
                    chartData.remainingLeaves,
                    chartData.consumedLeaves,
                    chartData.totalExpense,
                    chartData.totalSalary,
                    chartData.totalLoan,
                    chartData.totalAccidentIncident // Added accident/incident data
                ],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.7)', // Remaining Leaves
                    'rgba(255, 99, 132, 0.7)', // Consumed Leaves
                    'rgba(75, 192, 192, 0.7)',  // Total Expense
                    'rgba(153, 102, 255, 0.7)', // Salary Advance
                    'rgba(255, 159, 64, 0.7)',  // Loan
                    'rgba(255, 206, 86, 0.7)'   // Accident/Incident
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(255, 206, 86, 1)'  // Border color for Accident/Incident
                ],
                borderWidth: 2,
                barPercentage: 0.8,
                categoryPercentage: 0.6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function (value) {
                            return value.toLocaleString(); // Add thousands separators
                        }
                    }
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            let label = context.dataset.label || '';
                            if (label) label += ': ';
                            if (context.parsed.y !== null) label += context.parsed.y.toLocaleString();
                            return label;
                        }
                    }
                }
            },
            animation: {
                duration: 2000,
                easing: 'easeOutQuart'
            },
            onClick: (e, activeElements) => {
                if (activeElements.length > 0) {
                    const index = activeElements[0].index;
                    const label = barChart.data.labels[index];
                    const value = barChart.data.datasets[0].data[index];
                    alert(`${label}: ${value.toLocaleString()}`);
                }
            }
        }
    });

    // Pie Chart Configuration
    var pieCtx = document.getElementById('distributionChart').getContext('2d');

    var pieChart = new Chart(pieCtx, {
        type: 'pie',
        data: {
            labels: ['Remaining Leaves', 'Consumed Leaves', 'Total Expense', 'Salary Advance', 'Loan', 'Accident/Incident'],
            datasets: [{
                data: [
                    chartData.remainingLeaves,
                    chartData.consumedLeaves,
                    chartData.totalExpense,
                    chartData.totalSalary,
                    chartData.totalLoan,
                    chartData.totalAccidentIncident // Added accident/incident data
                ],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.7)', // Remaining Leaves
                    'rgba(255, 99, 132, 0.7)', // Consumed Leaves
                    'rgba(75, 192, 192, 0.7)',  // Total Expense
                    'rgba(153, 102, 255, 0.7)', // Salary Advance
                    'rgba(255, 159, 64, 0.7)',  // Loan
                    'rgba(255, 206, 86, 0.7)'   // Accident/Incident
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(255, 206, 86, 1)'   // Border color for Accident/Incident
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: true },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            let label = context.label || '';
                            if (label) label += ': ';
                            if (context.parsed !== null) label += context.parsed.toLocaleString();
                            return label;
                        }
                    }
                }
            },
            animation: {
                duration: 2000,
                easing: 'easeOutQuart'
            }
        }
    });

    // Adjust chart sizes
    function resizeCharts() {
        barChart.canvas.parentNode.style.height = window.innerHeight * 0.5 + 'px';
        pieChart.canvas.parentNode.style.height = window.innerHeight * 0.5 + 'px';
    }

    window.addEventListener('resize', resizeCharts);
    resizeCharts(); // Initial sizing
});


//document.addEventListener('DOMContentLoaded', function () {
//    // Fetch chart data from the embedded JSON script
//    var chartDataElement = document.getElementById('chart-data');
//    var chartData = JSON.parse(chartDataElement.textContent);
//
//    // Configuration for the Bar Chart
//    var barCtx = document.getElementById('summaryChart').getContext('2d');
//
//    // Add background color to the chart area
//    barCtx.canvas.parentNode.style.backgroundColor = '#9EC7E3'; // Set background color for chart area
//
//    var barChart = new Chart(barCtx, {
//        type: 'bar',
//        data: {
//            labels: ['Remaining Leaves', 'Consumed Leaves', 'Total Expense', 'Salary Advance', 'Loan'],
//            datasets: [{
//                label: 'Employee Details',
//                data: [
//                    chartData.remainingLeaves,
//                    chartData.consumedLeaves,
//                    chartData.totalExpense,
//                    chartData.totalSalary,
//                    chartData.totalLoan
//                ],
//                backgroundColor: [
//                    'rgba(54, 162, 235, 0.7)',
//                    'rgba(255, 99, 132, 0.7)',
//                    'rgba(75, 192, 192, 0.7)',
//                    'rgba(153, 102, 255, 0.7)',
//                    'rgba(255, 159, 64, 0.7)'
//                ],
//                borderColor: [
//                    'rgba(54, 162, 235, 1)',
//                    'rgba(255, 99, 132, 1)',
//                    'rgba(75, 192, 192, 1)',
//                    'rgba(153, 102, 255, 1)',
//                    'rgba(255, 159, 64, 1)'
//                ],
//                borderWidth: 2,
//                barPercentage: 0.8,
//                categoryPercentage: 0.6
//            }]
//        },
//        options: {
//            responsive: true,
//            maintainAspectRatio: false,
//            scales: {
//                y: {
//                    beginAtZero: true,
//                    ticks: {
//                        callback: function (value) {
//                            return value.toLocaleString(); // Add thousands separators
//                        }
//                    }
//                }
//            },
//            plugins: {
//                legend: { display: false },
//                tooltip: {
//                    callbacks: {
//                        label: function (context) {
//                            let label = context.dataset.label || '';
//                            if (label) label += ': ';
//                            if (context.parsed.y !== null) label += context.parsed.y.toLocaleString();
//                            return label;
//                        }
//                    }
//                }
//            },
//            animation: {
//                duration: 2000,
//                easing: 'easeOutQuart'
//            },
//            onClick: (e, activeElements) => {
//                if (activeElements.length > 0) {
//                    const index = activeElements[0].index;
//                    const label = barChart.data.labels[index];
//                    const value = barChart.data.datasets[0].data[index];
//                    alert(`${label}: ${value.toLocaleString()}`);
//                }
//            }
//        }
//    });
//
//    // Pie Chart Configuration
//    var pieCtx = document.getElementById('distributionChart').getContext('2d');
//
//    var pieChart = new Chart(pieCtx, {
//        type: 'pie',
//        data: {
//            labels: ['Remaining Leaves', 'Consumed Leaves', 'Total Expense'],
//            datasets: [{
//                data: [
//                    chartData.remainingLeaves,
//                    chartData.consumedLeaves,
//                    chartData.totalExpense
//                ],
//                backgroundColor: [
//                    'rgba(54, 162, 235, 0.7)',
//                    'rgba(255, 99, 132, 0.7)',
//                    'rgba(75, 192, 192, 0.7)'
//                ],
//                borderColor: [
//                    'rgba(54, 162, 235, 1)',
//                    'rgba(255, 99, 132, 1)',
//                    'rgba(75, 192, 192, 1)'
//                ],
//                borderWidth: 2
//            }]
//        },
//        options: {
//            responsive: true,
//            maintainAspectRatio: false,
//            plugins: {
//                legend: { display: true },
//                tooltip: {
//                    callbacks: {
//                        label: function (context) {
//                            let label = context.label || '';
//                            if (label) label += ': ';
//                            if (context.parsed !== null) label += context.parsed.toLocaleString();
//                            return label;
//                        }
//                    }
//                }
//            },
//            animation: {
//                duration: 2000,
//                easing: 'easeOutQuart'
//            }
//        }
//    });
//
//    // Adjust chart sizes
//    function resizeCharts() {
//        barChart.canvas.parentNode.style.height = window.innerHeight * 0.5 + 'px';
//        pieChart.canvas.parentNode.style.height = window.innerHeight * 0.5 + 'px';
//    }
//
//    window.addEventListener('resize', resizeCharts);
//    resizeCharts(); // Initial sizing
//});
