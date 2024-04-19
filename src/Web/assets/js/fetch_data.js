document.addEventListener("DOMContentLoaded", function () {
  // Get the current URL's hostname and set port
  const hostname = window.location.hostname;
  const port = 80;

  // Define form and input elements
  const form = document.getElementById("scrape-form");
  const urlInput = document.getElementById("url-input");

  // Define UI components
  const loadingSpinner = document.getElementById("loading-spinner");
  const scrapeContainer = document.getElementById("scrape-container");
  const dataTableContainer = document.getElementById("data-table-container");

  // Initialize state flag for data table
  let dataTableInitialized = false;

  // Initialize scrape container visibility
  initializeScrapeContainer(scrapeContainer);

  // Attach event handler for form submission
  form.addEventListener("submit", (event) =>
    handleSubmit(event, hostname, port)
  );

  function initializeScrapeContainer(container) {
    // Hide scrape container initially
    container.style.display = "none";
  }

  async function handleSubmit(event, hostname, port) {
    event.preventDefault();

    // Get user input URL
    const url = urlInput.value.trim();

    // Define API endpoint and full URL
    const endpoint = "/realtor/properties/";
    const apiUrl = `http://${hostname}:${port}${endpoint}`;

    // Prepare form data
    const formData = { url: url };

    // Show loading spinner
    setElementVisibility(loadingSpinner, true);

    try {
      // Fetch data from API
      const response = await fetchData(apiUrl, formData);

      // Process response data
      const properties = await processResponse(response);

      // Create or update data table
      manageDataTable(properties);

      // Show scrape container after successful data fetch and table creation
      setElementVisibility(scrapeContainer, true);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      // Hide loading spinner
      setElementVisibility(loadingSpinner, false);
    }
  }

  function setElementVisibility(element, isVisible) {
    element.style.display = isVisible ? "block" : "none";
  }

  async function fetchData(apiUrl, formData) {
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

    return response;
  }

  async function processResponse(response) {
    const data = await response.json();
    return data.properties;
  }

  function manageDataTable(properties) {
    // If DataTable is not initialized, create and append it
    if (!dataTableInitialized) {
      const table = createDataTable(properties);
      dataTableContainer.appendChild(table);
      initializeDataTable(table);
      dataTableInitialized = true;
    }
  }

  function createDataTable(data) {
    const table = document.createElement("table");
    table.id = "data-table";
    table.classList.add("display");

    // Create table header and body
    createTableHeader(table, data);
    createTableBody(table, data);

    return table;
  }

  function createTableHeader(table, data) {
    const headerRow = table.createTHead().insertRow();
    Object.keys(data[0]).forEach((key) => {
      const headerCell = document.createElement("th");
      headerCell.textContent = key;
      headerRow.appendChild(headerCell);
    });
  }

  function createTableBody(table, data) {
    const tbody = table.createTBody();
    data.forEach((item) => {
      const row = tbody.insertRow();
      Object.values(item).forEach((value) => {
        const cell = row.insertCell();
        cell.textContent = value;
      });
    });
  }

  function initializeDataTable(table) {
    $("#data-table").DataTable({
      scrollX: true, // Enable horizontal scrolling
      layout: {
        topStart: {
          buttons: ["copy", "csv", "excel", "pdf", "print"],
        },
      },
    });
  }
});
