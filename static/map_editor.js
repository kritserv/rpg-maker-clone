document.addEventListener("DOMContentLoaded", () => {
  const mapContainer = document.getElementById("map-container");
  const tileContainer = document.querySelector(".tile-container");
  const layerToggles = document.querySelectorAll(".layer-toggle");
  let selectedTile = null;

  // Tile selection
  tileContainer.addEventListener("click", (event) => {
    const tile = event.target.closest(".tile");
    if (tile) {
      // Highlight selected tile
      if (selectedTile) {
        selectedTile.classList.remove("selected-tile");
      }
      selectedTile = tile;
      selectedTile.classList.add("selected-tile");
    }
  });

  // Map tile placement
  mapContainer.addEventListener("click", (event) => {
    if (!selectedTile) return;

    const cell = event.target.closest("td");
    if (cell) {
      const img = cell.querySelector("img");
      const newTileSrc = selectedTile.src;

      if (img) {
        img.src = newTileSrc; // Update existing image
      } else {
        const newImg = document.createElement("img");
        newImg.src = newTileSrc;
        cell.appendChild(newImg); // Add new image
      }
    }
  });

  let isDragging = false;

  mapContainer.addEventListener("mousedown", (event) => {
    if (event.button === 0) {
      isDragging = true;
      placeTile(event.target);
    } else if (event.button === 2) {
      isDragging = true;
      deleteTile(event.target);
    }
  });

  mapContainer.addEventListener("mousemove", (event) => {
    if (isDragging && event.buttons === 1) {
      placeTile(event.target);
    } else if (isDragging && event.buttons === 2) {
      deleteTile(event.target);
    }
  });

  mapContainer.addEventListener("mouseup", () => {
    isDragging = false;
  });

  function placeTile(target) {
    const cell = target.closest("td");
    if (cell && selectedTile) {
      const img = cell.querySelector("img");
      const newTileSrc = selectedTile.src;

      if (img) {
        img.src = newTileSrc; // Update existing image
      } else {
        const newImg = document.createElement("img");
        newImg.src = newTileSrc;
        newImg.draggable = false;
        cell.appendChild(newImg); // Add new image
      }
    }
  }

  function deleteTile(target) {
    const cell = target.closest("td");
    if (cell) {
      const img = cell.querySelector("img");
      if (img) {
        cell.removeChild(img); // Remove the image
      }
    }
  }

  // Layer toggles
  layerToggles.forEach((toggle) => {
    toggle.addEventListener("change", (event) => {
      const layerIndex = event.target.dataset.layer;
      const layer = mapContainer.querySelector(
        `.map-layer[data-layer="${layerIndex}"]`,
      );
      if (layer) {
        layer.style.display = event.target.checked ? "table" : "none";
      }
    });
  });

  // Layer interactivity control
  const layerSelect = document.getElementById("layer-select");

  layerSelect.addEventListener("change", (event) => {
    const selectedOption = event.target.value;

    document.querySelectorAll(".map-layer").forEach((layer) => {
      if (selectedOption === "default") {
        // Default view: all layers visible but uninteractable
        layer.style.pointerEvents = "none"; // Disable interactivity
        layer.style.opacity = "1"; // Fully visible
      } else {
        const layerIndex = parseInt(layer.getAttribute("data-layer"));
        const selectedLayer = parseInt(selectedOption) - 1;

        if (layerIndex === selectedLayer) {
          layer.style.pointerEvents = "auto"; // Enable interactivity
          layer.style.opacity = "1"; // Fully visible
        } else {
          layer.style.pointerEvents = "none"; // Disable interactivity
          layer.style.opacity = "0.5"; // Make less visible
        }
      }
    });
  });

  // Prevent context menu on map container (useful for right-click functionality in future)
  mapContainer.addEventListener("contextmenu", (event) =>
    event.preventDefault(),
  );
});
