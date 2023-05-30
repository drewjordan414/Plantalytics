const urlParams = new URLSearchParams(window.location.search);
const searchTerm = urlParams.get('q');

const apiKEY = "mr_oVBJyJU8T8JhSYfsR1bligkBN0gIq7cva_2tMX1E"
const url = `https://trefle.io/api/v1/plants/search?token=${apiKEY}&q=${searchTerm}`;

fetch(url)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    // Assuming data is the array of plants
    const plant = data.data[0];
    const plantDetails = document.querySelector('#plant-details'); // this is the element where you want to display the details
    plantDetails.innerHTML = `
        <h2>${plant.common_name}</h2>
        <h3>Growth Conditions</h3>
        <p>Optimal temperature: ${plant.growth.temperature_minimum.deg_c}°C</p>
        <p>Optimal soil pH: ${plant.growth.ph_minimum} - ${plant.growth.ph_maximum}</p>
        <h3>About the Plant</h3>
        <p>${plant.bibliography}</p>
    `;
  })
  .catch(error => {
    console.error('There has been a problem with your fetch operation:', error);
  });