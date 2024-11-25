let currentPage = 1;
const rowsPerPage = 10;

function setupPagination() {
    const table = document.querySelector("table");
    const rows = Array.from(table.querySelectorAll("tr")); // Select all rows including header
    const totalPages = Math.ceil((rows.length - 1) / rowsPerPage); // Exclude header from total rows count
    
    showPage(currentPage, rows, totalPages);
    document.getElementById("prevBtn").addEventListener("click", () => changePage(-1, rows, totalPages));
    document.getElementById("nextBtn").addEventListener("click", () => changePage(1, rows, totalPages));
}

function showPage(page, rows, totalPages) {
    // Always show the header row (first row)
    rows[0].style.display = "";
    
    // Loop through data rows, starting from the second row
    for (let i = 1; i < rows.length; i++) {
        rows[i].style.display = (i > (page - 1) * rowsPerPage && i <= page * rowsPerPage) ? "" : "none";
    }

    document.getElementById("pageNumber").textContent = page;
    document.getElementById("prevBtn").disabled = page === 1;
    document.getElementById("nextBtn").disabled = page === totalPages;
}

function changePage(increment, rows, totalPages) {
    currentPage = Math.max(1, Math.min(currentPage + increment, totalPages));
    showPage(currentPage, rows, totalPages);
}

document.addEventListener("DOMContentLoaded", setupPagination);
