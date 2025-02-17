const mapContainer = document.getElementById("map-container");
const zoomSlider = document.getElementById("zoom-slider");
const zoomLevel = document.getElementById("zoom-level");

// Adjust zoom level
zoomSlider.addEventListener("input", () => {
  const zoomValue = zoomSlider.value;
  zoomLevel.textContent = `${zoomValue}%`;
  mapContainer.style.zoom = `${zoomValue / 100}`;
});
