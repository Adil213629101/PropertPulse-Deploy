document.addEventListener("DOMContentLoaded", async function () {
  const form = document.getElementById("scrape-form");
  const urlInput = document.getElementById("url-input");
  const loadingSpinner = document.getElementById("loading-spinner");
  const scrapeContainer = document.getElementById("scrape-container");
  const dataTableContainer = document.getElementById("data-table-container");

  // Hide scrape container initially
  scrapeContainer.style.display = "none";

  form.addEventListener("submit", handleSubmit);

  let dataTableInitialized = false; // Flag to track if DataTable is initialized

  async function handleSubmit(event) {
    event.preventDefault();
    const url = urlInput.value.trim();
    const apiUrl = "http://127.0.0.1:8000/realtor/properties/";
    const formData = {
      url: url,
    };

    loadingSpinner.style.display = "block";

    try {
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      const properties = data.properties;
      console.log("properties", properties);

      // Create DataTable if not initialized
      if (!dataTableInitialized) {
        const table = createDataTable(properties);
        dataTableContainer.appendChild(table);

        $("#data-table").DataTable({
          scrollX: true, // Enable horizontal scrolling
          layout: {
            topStart: {
              buttons: ["copy", "csv", "excel", "pdf", "print"],
            },
          },
        });

        dataTableInitialized = true; // Update flag
      }

      // Show scrape container after data is fetched and table is created
      scrapeContainer.style.display = "block";
    } catch (error) {
      console.error("Error:", error);
    } finally {
      loadingSpinner.style.display = "none";
    }
  }

  // Function to create data table
  function createDataTable(data) {
    const table = document.createElement("table");
    table.setAttribute("id", "data-table");
    table.classList.add("display");

    // Create table header
    const headerRow = table.createTHead().insertRow();
    for (let key in data[0]) {
      const headerCell = document.createElement("th");
      headerCell.textContent = key;
      headerRow.appendChild(headerCell);
    }

    // Create table body
    const tbody = table.createTBody();
    data.forEach((item) => {
      const row = tbody.insertRow();
      for (let key in item) {
        const cell = row.insertCell();
        cell.textContent = item[key];
      }
    });

    return table;
  }
});
