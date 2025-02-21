document.addEventListener("DOMContentLoaded", () => {
  const mapContainer = document.getElementById("map-container");
  const tileContainer = document.querySelector(".tile-container");
  const layerToggles = document.querySelectorAll(".layer-toggle");
  const mapSelect = document.getElementById("map-select");
  const layerSelect = document.getElementById("layer-select");
  let selectedTile = null;
  let isDragging = false;

  // Map selection handler
  mapSelect.addEventListener("change", (event) => {
    // Reset layer selection to default
    layerSelect.value = "default";
    // Reset layer interactivity
    resetLayerInteractivity();
  });

  // Tile selection
  tileContainer.addEventListener("click", (event) => {
    const tile = event.target.closest(".tile");
    if (tile) {
      if (selectedTile) {
        selectedTile.classList.remove("selected-tile");
      }
      selectedTile = tile;
      selectedTile.classList.add("selected-tile");
    }
  });

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
      const parentLayer = cell.closest(".map-layer");
      if (parentLayer && parentLayer.style.pointerEvents === "none") {
        return; // Don't place tiles on inactive layers
      }

      const img = cell.querySelector("img");
      const newTileSrc = selectedTile.src;
      const newTileId = selectedTile.id;

      if (img) {
        img.src = newTileSrc;
        img.id = newTileId;
      } else {
        const newImg = document.createElement("img");
        newImg.src = newTileSrc;
        newImg.draggable = false;
        newImg.id = newTileId;
        cell.appendChild(newImg);
      }
    }
  }

  function deleteTile(target) {
    const cell = target.closest("td");
    if (cell) {
      const parentLayer = cell.closest(".map-layer");
      if (parentLayer && parentLayer.style.pointerEvents === "none") {
        return; // Don't delete tiles from inactive layers
      }

      const img = cell.querySelector("img");
      if (img) {
        cell.removeChild(img);
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
  layerSelect.addEventListener("change", (event) => {
    updateLayerInteractivity(event.target.value);
  });

  function updateLayerInteractivity(selectedOption) {
    document.querySelectorAll(".map-layer").forEach((layer) => {
      const layerIndex = parseInt(layer.getAttribute("data-layer"));

      if (selectedOption === "default") {
        layer.style.pointerEvents = "none";
        layer.style.opacity = "1";
      } else {
        const selectedLayer = parseInt(selectedOption) - 1;
        layer.style.pointerEvents =
          layerIndex === selectedLayer ? "auto" : "none";
        layer.style.opacity = layerIndex === selectedLayer ? "1" : "0.5";
      }
    });
  }

  function resetLayerInteractivity() {
    document.querySelectorAll(".map-layer").forEach((layer) => {
      layer.style.pointerEvents = "none";
      layer.style.opacity = "1";
    });
  }

  // Save map functionality
  function saveMapData() {
    const mapData = [];
    const layers = document.querySelectorAll(".map-layer");

    layers.forEach((layer, index) => {
      if (index >= 4) return;

      const layerData = [];
      layer.querySelectorAll("tr").forEach((row) => {
        const rowData = [];
        row.querySelectorAll("td").forEach((cell) => {
          const img = cell.querySelector("img");
          rowData.push(img ? img.id : "");
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
        map_name: document.querySelector("#map-select").value,
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
  mapContainer.addEventListener("contextmenu", (event) =>
    event.preventDefault(),
  );
});
