document.getElementById("map-select").addEventListener("change", function () {
  const selectedMap = this.value;
  window.location.href = `/?map_name=${selectedMap}`;
});
