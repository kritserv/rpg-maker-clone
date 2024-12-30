document.getElementById("saveMainTitle").addEventListener("click", function () {
  const mainTitle = document.getElementById("main_title").value;

  fetch("/database", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ main_title: mainTitle }),
  })
    .then((response) => {
      if (response.ok) {
      } else {
        alert("Failed to save data.");
      }
    })
    .catch((error) => console.error("Error:", error));
});
