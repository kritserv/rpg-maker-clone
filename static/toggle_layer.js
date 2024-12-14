// Toggle layer visibility based on checkbox state
document.querySelectorAll(".layer-toggle").forEach((checkbox) => {
  checkbox.addEventListener("change", (event) => {
    const layerIndex = event.target.getAttribute("data-layer");
    const layerTable = document.querySelector(
      `.map-layer[data-layer="${layerIndex}"]`,
    );
    if (event.target.checked) {
      layerTable.style.display = "block";
    } else {
      layerTable.style.display = "none";
    }
  });
});
