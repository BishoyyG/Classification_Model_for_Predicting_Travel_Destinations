// script.js

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('test-form');
    const reportDiv = document.getElementById('classification-report');

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(form);

        fetch('/test', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            formatReport(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    function formatReport(data) {
        // Split the response by new line
        const lines = data.split('\n');

        // Create a table element to display the report
        const table = document.createElement('table');
        table.classList.add('report-table');

        // Create table header
        const headerRow = document.createElement('tr');
        const headers = ['Class', 'Precision', 'Recall', 'F1-Score', 'Support'];
        headers.forEach(headerText => {
            const th = document.createElement('th');
            th.textContent = headerText;
            headerRow.appendChild(th);
        });
        table.appendChild(headerRow);

        // Parse and add data rows
        lines.forEach(line => {
            const cells = line.trim().split(/\s+/);
            if (cells.length === 5) {
                const row = document.createElement('tr');
                cells.forEach(cellText => {
                    const td = document.createElement('td');
                    td.textContent = cellText;
                    row.appendChild(td);
                });
                table.appendChild(row);
            }
        });

        // Clear previous report
        reportDiv.innerHTML = '';

        // Append the table to the report container
        reportDiv.appendChild(table);
    }
});
