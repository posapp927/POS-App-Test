document.addEventListener('DOMContentLoaded', function() {
    const requiredColumns = ['System ID', 'UPC', 'Name'];
    const allColumns = ['System ID', 'UPC', 'Name', 'Brand', 'Short Name', 'Size', 'Price', 'QOH', 'Photo'];
    let products = JSON.parse(localStorage.getItem('productDatabase')) || [];


    // Import button to trigger CSV file input
    document.getElementById('importButton').addEventListener('click', function() {
        document.getElementById('csvFileInput').click();
    });

    // CSV file input change event
    document.getElementById('csvFileInput').addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            Papa.parse(file, {
                header: true,
                complete: function(results) {
                    const csvData = results.data;
                    if (validateCSVColumns(results.meta.fields)) {
                        processCSVData(csvData);
                    } else {
                        alert('CSV file is missing required columns: System ID, UPC, or Name.');
                    }
                }
            });
        }
    });

    // Validate CSV columns
    function validateCSVColumns(fields) {
        const hasRequiredColumns = requiredColumns.some(col => fields.includes(col));
        return hasRequiredColumns && fields.includes('Name');
    }

    // Process CSV data
    function processCSVData(data) {
        data.forEach(row => {
            const existingProductIndex = products.findIndex(product =>
                product['System ID'] === row['System ID'] || product['UPC'] === row['UPC']);

            if (existingProductIndex > -1) {
                // Update existing product
                updateProduct(existingProductIndex, row);
            } else {
                // Add new product
                addNewProduct(row);
            }
        });

        console.log('Updated Product Database:', products);
        // Pass the updated product data to localStorage for use in index.html
        localStorage.setItem('productDatabase', JSON.stringify(products));
    }

    // Update existing product
    function updateProduct(index, row) {
        allColumns.forEach(column => {
            if (row[column]) {
                products[index][column] = row[column];
            }
        });
    }

    // Add new product
    function addNewProduct(row) {
        if (!row['System ID']) {
            row['System ID'] = generateSystemID();
        }
        products.push(row);
    }

    // Generate System ID
    function generateSystemID() {
        return 'SYS' + Math.floor(Math.random() * 1000000).toString().padStart(6, '0');
    }

	// Function to display data in table
	function displayDataInTable() {
		const tableBody = document.querySelector('.product-table tbody');
		tableBody.innerHTML = ''; // Clear existing rows

		products.forEach(row => {
			// Extract the photo path, removing any surrounding quotes and trimming whitespace
			const photoList = row.Photo ? row.Photo.match(/\[(.*?)\]/) : null;
			const photoPath = photoList ? photoList[1].replace(/['"]+/g, '').split(',')[0].trim() : '';

			// Assuming photoPath is a URL or relative path to the image
			const firstPhotoLocation = photoPath ? photoPath : '';

			const tableRow = document.createElement('tr');

			tableRow.innerHTML = `
				<td><label class="custom-checkbox"><input type="checkbox"><span class="checkmark"></span></label></td>
				<td class="photo-column">${firstPhotoLocation ? `<img src="static/images/${firstPhotoLocation}" alt="Product Photo">` : ''}</td>
				<td>${row.Brand || ''}</td>
				<td>${row.Name || ''}</td>
				<td>${row.Price || ''}</td>
				<td>${row.Discounts || ''}</td>
				<td>${row.QOH || ''}</td>
			`;

			tableBody.appendChild(tableRow);
		});
	}






    // Display the initial data from localStorage
    displayDataInTable();
});

document.getElementById('crossButton').addEventListener('click', function() {
    var url = this.getAttribute('data-url');
    window.location.href = url;
});