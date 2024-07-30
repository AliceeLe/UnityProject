// Define the data ranges corresponding to colors
var data = [80, 90, 100]; // Red for 1-80%, Yellow for 80-90%, Green for 90-100%
var value = 85; // Initial value within the red range (1-80%)

var config = {
    type: 'gauge',
    data: {
        datasets: [{
            data: data,
            value: value,
            backgroundColor: ['red', 'yellow', 'green'],
            borderWidth: 2
        }]
    },
    options: {
        responsive: true,
        title: {
            display: true,
            text: 'Gauge chart'
        },
        layout: {
            padding: {
                bottom: 30
            }
        },
        needle: {
            // Needle circle radius as the percentage of the chart area width
            radiusPercentage: 2,
            // Needle width as the percentage of the chart area width
            widthPercentage: 3.2,
            // Needle length as the percentage of the interval between inner radius (0%) and outer radius (100%) of the arc
            lengthPercentage: 80,
            // The color of the needle
            color: 'rgba(0, 0, 0, 1)'
        },
        valueLabel: {
            formatter: Math.round
        }
    }
};

window.onload = function() {
    var ctx = document.getElementById('chart').getContext('2d');
    window.myGauge = new Chart(ctx, config);
};

// Update button event listener to use parameterized data
document.getElementById('updateData').addEventListener('click', function() {
    var newData = [80, 90, 100]; // Keep the same ranges
    var newValue = 85; // New value within the yellow range (80-90%)

    config.data.datasets.forEach(function(dataset) {
        dataset.data = newData;
        dataset.value = newValue;
    });

    window.myGauge.update();
});
