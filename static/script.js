var relayState = {
    18: false,
    23: false,
    24: false,
    25: false
};

function setRelay(channel, state) {
    relayState[channel] = (state === 'on');
    console.log('Setting relay', channel, 'to', state);
    fetch('/set-relay', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            channel: channel,
            state: state
        })
    })
}

// Fetch sensor data and update display elements
function updateSensorData() {
    fetch('/static/data.json')
        .then(response => response.json())
        .then(data => {
            document.getElementById('temperature').innerHTML = data.temperature.toFixed(1);
            temperatureGauge.setValueAnimated(data.temperature);

            document.getElementById('humidity').innerHTML = data.humidity.toFixed(1);
            humidityGauge.setValueAnimated(data.humidity);

            document.getElementById('moisture').innerHTML = data.moisture.toFixed(1);
            moistureGauge.setValueAnimated(data.moisture);
        })
        .catch(error => console.error(error));
}

// Fetch plant care advice and update display elements
function updatePlantCareAdvice() {
    fetch('/plant-care-advice')
        .then(response => response.json())
        .then(data => {
            // Update plant care advice section here
            console.log(data);
        })
        .catch(error => console.error(error));
}

// Fetch plant health data and update display elements
function updatePlantHealthData() {
    fetch('/plant-health-data')
        .then(response => response.json())
        .then(data => {
            // Update plant health monitoring section here
            console.log(data);
        })
        .catch(error => console.error(error));
}

// Update gauge value when sensor data is fetched
function updateGaugeValue(value, type) {
    switch(type) {
        case 'temperature':
            temperatureGauge.setValueAnimated(value);
            break;
        case 'humidity':
            humidityGauge.setValueAnimated(value);
            break;
        case 'moisture':
            moistureGauge.setValueAnimated(value);
            break;
        default:
            break;
    }
}

// Create the gauges instances
var temperatureGauge, humidityGauge, moistureGauge;

document.addEventListener("DOMContentLoaded", function() {
    temperatureGauge = Gauge(
        document.getElementById("gauge-temperature"),
        {
            max: 150,
            value: 0,
            label: 'Temperature (°C)',
            color: '#FF7F50'
        }
    );

    humidityGauge = Gauge(
        document.getElementById("gauge-humidity"),
        {
            max: 100,
            value: 0,
            label: 'Humidity (%)',
            color: '#00BFFF'
        }
    );

    moistureGauge = Gauge(
        document.getElementById("gauge-moisture"),
        {
            max: 2000,
            value: 0,
            label: 'Moisture',
            color: '#3CB371'
        }
    );

    // Fetch initial sensor data, plant care advice and health data
    updateSensorData();
    updatePlantCareAdvice();
    updatePlantHealthData();
});

// Set up event listeners for relay switches
document.querySelectorAll('.relay-control input[type="checkbox"]').forEach(function(checkbox) {
    checkbox.addEventListener('change', function(event) {
        var channel = parseInt(event.target.closest('.relay-control').id.replace('relay-', ''));
        var state = event.target.checked ? 'on' : 'off';
        setRelay(channel, state);
    });
});

// Periodically update sensor data, plant
// Periodically update sensor data, plant care advice and health data
setInterval(updateSensorData, 5000);
setInterval(updatePlantCareAdvice, 5000);
setInterval(updatePlantHealthData, 5000);
