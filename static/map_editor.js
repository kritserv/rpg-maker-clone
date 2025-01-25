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
      const newTileId = selectedTile.id;

      if (img) {
        img.src = newTileSrc; // Update existing image
        img.id = newTileId;
      } else {
        const newImg = document.createElement("img");
        newImg.src = newTileSrc;
        newImg.draggable = false;
        newImg.id = newTileId;
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
  function saveMapData() {
    const mapData = [];
    const layers = document.querySelectorAll(".map-layer");

    layers.forEach((layer, index) => {
      // Skip the last iteration
      if (index === layers.length - 1) return;

      const layerData = [];
      layer.querySelectorAll("tr").forEach((row) => {
        const rowData = [];
        row.querySelectorAll("td").forEach((cell) => {
          const img = cell.querySelector("img");
          rowData.push(img ? img.id : ""); // Store id
        });
        layerData.push(rowData);
      });
      mapData.push(layerData);
    });

    fetch("save_map", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        map_name: document.querySelector("#map-select").value, // Map name
        layers: mapData,
      }),
    })
      .then((response) => {
        if (response.ok) {
          alert("Map saved successfully!");
        } else {
          alert("Failed to save map!");
        }
      })
      .catch((error) => {
        console.error("Error saving map:", error);
      });
  }
  document.getElementById("save-button").addEventListener("click", saveMapData);

  // Prevent context menu on map container (useful for right-click functionality in future)
  mapContainer.addEventListener("contextmenu", (event) =>
    event.preventDefault(),
  );
});
