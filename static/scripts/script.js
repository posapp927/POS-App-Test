//document.addEventListener('DOMContentLoaded', function() {
//    const searchInput = document.querySelector('.search-input');
//    const suggestionsContainer = document.querySelector('.search-dropdown');
//
//    function fetchProductSuggestions(query, isBarcodeScan) {
//            fetch(`/search?query=${query}`)
//                .then(response => response.json())
//                .then(data => {
//                    suggestionsContainer.innerHTML = '';  // Clear previous suggestions
//                    if (data.length > 0) {
//                        data.forEach(item => {
//                            const suggestionItem = document.createElement('li');
//                            suggestionItem.textContent = `${item['Brand']} ${item['Short Name']} - ${item['Size']}`;
//                            suggestionItem.dataset.systemId = item['System ID'];
//                            suggestionsContainer.appendChild(suggestionItem);
//
//                            // Handle click on suggestion to add to cart
//                            suggestionItem.addEventListener('click', function() {
//                                addToCart(item);
//                                suggestionsContainer.style.display = 'none';  // Hide suggestions after selection
//                            });
//                        });
//
//                        suggestionsContainer.style.display = 'block';
//
//                        // If it's a barcode scan, automatically select the first suggestion
//                        if (isBarcodeScan && data.length > 0) {
//                            addToCart(data[0]);  // Automatically add the first item to the cart
//                            suggestionsContainer.style.display = 'none';  // Hide the suggestions
//                        }
//
//                    } else {
//                        suggestionsContainer.style.display = 'none';
//                    }
//                })
//                .catch(error => console.error('Error fetching product suggestions:', error));
//    }
//
//    // Handle search input
//    searchInput.addEventListener('input', function() {
//        const query = this.value.trim();
//        if (query.length > 3) {
//            fetchProductSuggestions(query, false);
//        } else {
//            suggestionsContainer.style.display = 'none';
//        }
//    });
//
//    // Handle suggestion click
//    suggestionsContainer.addEventListener('click', function(event) {
//        if (event.target.tagName === 'LI') {
//            const systemId = event.target.dataset.systemId;
//            addToCart(systemId);
//            suggestionsContainer.style.display = 'none';
//            searchInput.value = '';  // Clear the search input
//        }
//    });
//
//    let barcodeInput = '';  // Accumulates the barcode characters
//    let lastKeyTime = Date.now();  // Track the time of the last keypress
//
//    document.addEventListener('keydown', function(event) {
//        const currentTime = Date.now();
//
//        // If more than 100ms has passed, consider it a new input
//        if (currentTime - lastKeyTime > 100) {
//            barcodeInput = '';  // Reset the barcode input
//        }
//
//        lastKeyTime = currentTime;
//
//        // Accumulate the keypresses if they are not 'Enter'
//        if (event.key !== 'Enter') {
//            barcodeInput += event.key;
//        } else {
//            // When 'Enter' is pressed, process the barcode input
//            if (barcodeInput.length > 0) {
//                console.log('Barcode scanned:', barcodeInput);
//                fetchProductSuggestions(barcodeInput.trim(), true);  // Perform the search with the accumulated barcode input
//
//                barcodeInput = '';  // Reset after processing
//            }
//        }
//    });
//
//    // Function to add an item to the cart (This needs to be implemented based on your cart logic)
//    function addToCart(systemId) {
//        console.log('Add to cart:', systemId);
//        // Implement logic to add the product to the cart using systemId
//        // This could involve making another AJAX call to add the item to the server-side cart
//    }
//});


document.addEventListener('DOMContentLoaded', function() {

    const inputs = document.querySelectorAll('input[type="text"]');
    inputs.forEach(input => {
        input.setAttribute('autocomplete', 'off');
        input.setAttribute('autocorrect', 'off');
        input.setAttribute('spellcheck', 'false');
    });
    let barcodeInput = '';  // Accumulates the barcode characters
    let lastKeyTime = Date.now();  // Track the time of the last keypress
    const searchInput = document.querySelector('.search-input');
    const suggestionsContainer = document.querySelector('.product-suggestions');

    // Handle global barcode input
    document.addEventListener('keydown', function(event) {
        const currentTime = Date.now();

        if (currentTime - lastKeyTime > 100) {
            barcodeInput = '';  // Reset the barcode input
        }

        lastKeyTime = currentTime;

        if (event.key !== 'Enter') {
            barcodeInput += event.key;
        } else {
            if (barcodeInput.length > 0) {
                console.log('Barcode scanned:', barcodeInput);
                fetchProductSuggestions(barcodeInput.trim(), true);  // Handle barcode input
                barcodeInput = '';  // Reset after processing
            }
        }
    });

    searchInput.addEventListener('input', function() {
        const query = searchInput.value.trim();
        if (query.length > 3) {
            fetchProductSuggestions(query, false);  // Handle manual input
        } else {
            suggestionsContainer.style.display = 'none';  // Hide suggestions if query is too short
        }
    });

    function fetchProductSuggestions(query, isBarcodeScan) {
        fetch(`/search?query=${query}`)
            .then(response => response.json())
            .then(data => {
                console.log('Fetched data:', data);  // Debugging line
                suggestionsContainer.innerHTML = '';  // Clear previous suggestions
                if (data.length > 0) {
                    data.forEach(item => {
                        const suggestionItem = document.createElement('li');
                        suggestionItem.textContent = `${item['Brand']} ${item['Short_Name']} - ${item['Size']}`;
                        suggestionItem.dataset.systemId = item['System_ID'];
                        suggestionsContainer.appendChild(suggestionItem);

                        suggestionItem.addEventListener('click', function() {
                            addToCart(item['System_ID']);
                            suggestionsContainer.style.display = 'none';  // Hide suggestions after selection
                        });
                    });

                    suggestionsContainer.style.display = 'block';
                    console.log('Suggestions displayed:', suggestionsContainer.innerHTML);  // Debugging line

                    if (isBarcodeScan && data.length > 0) {
                        addToCart(data[0]['System_ID']);  // Automatically add the first item to the cart
                        suggestionsContainer.style.display = 'none';
                    }

                } else {
                    suggestionsContainer.style.display = 'none';
                    console.log('No suggestions found.');  // Debugging line
                }
            })
            .catch(error => console.error('Error fetching product suggestions:', error));
    }

    function addToCart(systemId) {
        console.log('adding system id', systemId)
        fetch('/add_to_cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ system_id: systemId })
        })
        .then(response => response.json())
        .then(data => {
            console.log('data response', data)
            if (data.success) {
                console.log('Product added to cart:', data.message);
                addToCartTable(data);  // Pass the `cart_items` array to display it
            } else {
                console.error('Error adding product to cart:', data.message);
            }
    })
    .catch(error => console.error('Error adding product to cart:', error));
    }


});


//function addToCartTable(cartResponse) {
//    const cart = cartResponse.cart;  // Access the cart array from the response
//    console.log('cart', cart);
//    const tableBody = document.querySelector('.cart-items-table tbody');
//    const garbageIconUrl = document.getElementById('garbage-icon-url').getAttribute('data-url');
//
//    // Clear the cart table before rendering the updated items
//    tableBody.innerHTML = '';
//
//    cart.forEach(cartItem => {
//        const product = cartItem.product_name;
//        const quantity = cartItem.quantity;
//        const discount = cartItem.discount_amount === 'Free' ? 0 : cartItem.discount_amount || 0;
//        const discount_name = cartItem.discount_name || '';
//        const discount_taxable = cartItem.discount_taxable || false;
//        const price = parseFloat(cartItem.base_price);
//        const taxRate = 0.09;
//        let tax;
//
//        // Separate logic to handle 'Free' items
//        if (cartItem.discount_amount === 'Free') {
//            tax = 0;  // Free items have no tax
//            total = 0;
//        } else {
//            if (!discount_taxable) {
//                tax = (price - discount) * quantity * taxRate;
//            } else {
//                tax = price * quantity * taxRate;
//            }
//            total = (price * quantity) + tax;
//        }
//
//        let itemColumnContent = '';
//        if (cartItem.brand) {
//            itemColumnContent += `<div style="font-size: 0.9em;"><strong>${cartItem.brand}</strong></div>`;
//        }
//        if (product) {
//            itemColumnContent += `<div style="font-size: 0.8em;">${product}</div>`;
//        }
//        if (cartItem.size) {
//            itemColumnContent += `<div style="font-size: 0.6em;">${cartItem.size} | ${cartItem.pets}</div>`;
//        } else {
//            itemColumnContent += `<div style="font-size: 0.6em;">${cartItem.pets}</div>`;
//        }
//
//        const row = document.createElement('tr');
//        row.className = 'cart-item-row';
//        row.setAttribute('data-upc', cartItem.upc);
//        row.setAttribute('data-system-id', cartItem.system_id);
//
//        row.innerHTML = `
//            <td class="item-column">
//                ${itemColumnContent}
//            </td>
//            <td class="price-column">
//                ${cartItem.discount_amount === 'Free'
//                    ? `<span class="original-price" style="text-decoration: line-through;">${price.toFixed(2)}</span><br>
//                       <span class="discounted-price">Free</span>`
//                    : (discount > 0
//                        ? `<span class="original-price" style="text-decoration: line-through;">${price.toFixed(2)}</span><br>
//                           <span class="discounted-price">${(price - discount).toFixed(2)}</span>`
//                        : `<span class="original-price">${price.toFixed(2)}</span>`
//                    )
//                }
//            </td>
//            <td class="quantity-column">
//                <input type="number" value="${quantity}" min="1" />
//            </td>
//            <td class="discounts-column ${discount > 0 ? (discount_taxable ? 'taxable' : 'non-taxable') : ''}">
//                <span style="line-height: 1;">${discount > 0 ? discount.toFixed(2) : ''}</span>
//                ${discount > 0 || cartItem.discount_amount === 'Free' ? `<br><span class="discount-name">${discount_name}</span>` : ''}
//            </td>
//            <td class="tax-column">${tax.toFixed(2)}</td>
//            <td class="total-column">
//                ${cartItem.discount_amount === 'Free'
//                    ? 'Free'
//                    : (discount > 0 ? (total - discount * quantity).toFixed(2) : total.toFixed(2))
//                }
//            </td>
//            <td class="empty-column">
//                <img src="${garbageIconUrl}" class="delete-icon row" alt="Delete">
//            </td>
//        `;
//
//        // Add event listener to delete the item
//        row.querySelector('.delete-icon.row').addEventListener('click', () => {
//            removeFromCart(cartItem.system_id);  // Adjust this to correctly remove from the server-side cart
//            addToCartTable(cart);  // Re-render the cart table
//        });
//
//        // Add event listener to update total on quantity change
//        row.querySelector('.quantity-column input').addEventListener('change', function () {
//            const newQuantity = parseInt(this.value, 10);
//            updateCartQuantity(cartItem.system_id, newQuantity);  // Adjust this to correctly update the server-side cart
//            addToCartTable(cart);  // Re-render the cart table
//        });
//
//        tableBody.appendChild(row);
//    });
//
//    // Update summary table (optional, depending on your implementation)
//    updateSummaryTable(cart);
//}





function addToCartTable(cartResponse) {
    const cart = cartResponse.cart;  // Access the cart array from the response
    console.log('cart', cart);
    const tableBody = document.querySelector('.cart-items-table tbody');
    const garbageIconUrl = document.getElementById('garbage-icon-url').getAttribute('data-url');

    // Clear the cart table before rendering the updated items
    tableBody.innerHTML = '';


    cart.forEach(cartItem => {
        const product = cartItem.product_name;
        const brand = cartItem.brand;
        const size = cartItem.size;
        const pets = cartItem.pets;
        const basePrice = parseFloat(cartItem.base_price);
        const discountedQuantity = cartItem.discounted_quantity;
        const nonDiscountedQuantity = cartItem.non_discounted_quantity;
        const discountAmount = cartItem.discount_amount;
        const discountName = cartItem.discount_name || '';
        const discountTaxable = cartItem.discount_taxable || false;
        const taxRate = 0.09;
        const originalCartId = cartItem.cart_id; // Use the original cart_id
        let tax;

        // Determine total quantity and effective price
        const totalQuantity = discountedQuantity + nonDiscountedQuantity;
        const isDiscounted = discountAmount > 0 && discountedQuantity > 0;
        const effectivePrice = isDiscounted ? basePrice - (discountAmount / discountedQuantity) : basePrice;

        // Calculate tax based on whether the item is taxable
        tax = discountTaxable
            ? effectivePrice * totalQuantity * taxRate
            : basePrice * totalQuantity * taxRate;

        const totalPrice = effectivePrice * totalQuantity + tax;

        // Create a single row for the item
        const row = document.createElement('tr');
        row.className = 'cart-item-row';
        row.setAttribute('data-cart-id', originalCartId);  // Set cart_id

        // Generate the HTML content
        row.innerHTML = `
            <td class="item-column">
                <div style="font-size: 0.9em;"><strong>${brand}</strong></div>
                <div style="font-size: 0.8em;">${product}</div>
                <div style="font-size: 0.6em;">${size} | ${pets}</div>
            </td>
            <td class="price-column">
                ${isDiscounted
                    ? `<span class="original-price" style="text-decoration: line-through;">${basePrice.toFixed(2)}</span><br>
                       <span class="discounted-price">${effectivePrice.toFixed(2)}</span>`
                    : `<span class="original-price">${basePrice.toFixed(2)}</span>`
                }
            </td>
            <td class="quantity-column">
                <input type="number" value="${totalQuantity}" min="1" class="quantity-input" data-cart-id="${originalCartId}" />
            </td>
            <td class="discounts-column ${discountTaxable ? 'taxable' : 'non-taxable'}">
                ${isDiscounted ? `<span style="line-height: 1;">${discountAmount.toFixed(2)}</span><br><span class="discount-name">${discountName}</span>` : ''}
            </td>
            <td class="tax-column">${tax.toFixed(2)}</td>
            <td class="total-column">${totalPrice.toFixed(2)}</td>
            <td class="empty-column">
                <img src="${garbageIconUrl}" class="delete-icon row" alt="Delete">
            </td>
        `;

        // Append the row to the table body
        tableBody.appendChild(row);
    });

//    cart.forEach(cartItem => {
//        const product = cartItem.product_name;
//        const brand = cartItem.brand;
//        const size = cartItem.size;
//        const pets = cartItem.pets;
//        const basePrice = parseFloat(cartItem.base_price);
//        const discountedQuantity = cartItem.discounted_quantity;
//        const nonDiscountedQuantity = cartItem.non_discounted_quantity;
//        const discountAmount = cartItem.discount_amount;
//        const discountName = cartItem.discount_name || '';
//        const discountTaxable = cartItem.discount_taxable || false;
//        const taxRate = 0.09;
//        const originalCartId = cartItem.cart_id; // Use the original cart_id
//        let tax;
//
//        // Create rows for non-discounted quantity
//        if (nonDiscountedQuantity > 0) {
//            tax = discountTaxable
//                ? basePrice * nonDiscountedQuantity * taxRate
//                : (basePrice - discountAmount) * nonDiscountedQuantity * taxRate;
//
//            const totalNonDiscounted = basePrice * nonDiscountedQuantity + tax;
//
//            const row = document.createElement('tr');
//            row.className = 'cart-item-row';
//            row.setAttribute('data-cart-id', originalCartId);  // Set cart_id
//
//            row.innerHTML = `
//                <td class="item-column">
//                    <div style="font-size: 0.9em;"><strong>${brand}</strong></div>
//                    <div style="font-size: 0.8em;">${product}</div>
//                    <div style="font-size: 0.6em;">${size} | ${pets}</div>
//                </td>
//                <td class="price-column">
//                    <span class="original-price">${basePrice.toFixed(2)}</span>
//                </td>
//                <td class="quantity-column">
//                    <input type="number" value="${nonDiscountedQuantity}" min="1" class="quantity-input" data-cart-id="${originalCartId}" />
//                </td>
//                <td class="discounts-column"></td>
//                <td class="tax-column">${tax.toFixed(2)}</td>
//                <td class="total-column">${totalNonDiscounted.toFixed(2)}</td>
//                <td class="empty-column">
//                    <img src="${garbageIconUrl}" class="delete-icon row" alt="Delete">
//                </td>
//            `;
//
//            tableBody.appendChild(row);
//        }
//
//        // Create rows for discounted quantity
//        if (discountedQuantity > 0) {
//            const discountedPrice = basePrice - (discountAmount / discountedQuantity);
//            tax = discountTaxable
//                ? discountedPrice * discountedQuantity * taxRate
//                : basePrice * discountedQuantity * taxRate;
//
//            const totalDiscounted = discountedQuantity === 'Free'
//                ? 0
//                : discountedPrice * discountedQuantity + tax;
//
//            // Generate a unique cart ID for discounted items
//            const discountedCartId = `${originalCartId}_d`;
//
//            const row = document.createElement('tr');
//            row.className = 'cart-item-row';
//            row.setAttribute('data-cart-id', discountedCartId);  // Set unique cart_id for discounted items
//
//            row.innerHTML = `
//                <td class="item-column">
//                    <div style="font-size: 0.9em;"><strong>${brand}</strong></div>
//                    <div style="font-size: 0.8em;">${product}</div>
//                    <div style="font-size: 0.6em;">${size} | ${pets}</div>
//                </td>
//                <td class="price-column">
//                    ${discountedQuantity === 'Free'
//                        ? `<span class="original-price" style="text-decoration: line-through;">${basePrice.toFixed(2)}</span><br>
//                           <span class="discounted-price">Free</span>`
//                        : `<span class="original-price" style="text-decoration: line-through;">${basePrice.toFixed(2)}</span><br>
//                           <span class="discounted-price">${discountedPrice.toFixed(2)}</span>`
//                    }
//                </td>
//                <td class="quantity-column">
//                    <input type="number" value="${discountedQuantity}" min="1" class="quantity-input" data-cart-id="${discountedCartId}" />
//                </td>
//                <td class="discounts-column ${discountTaxable ? 'taxable' : 'non-taxable'}">
//                    <span style="line-height: 1;">${discountAmount === 'Free' ? 'Free' : discountAmount.toFixed(2)}</span>
//                    <br><span class="discount-name">${discountName}</span>
//                </td>
//                <td class="tax-column">${tax.toFixed(2)}</td>
//                <td class="total-column">${totalDiscounted.toFixed(2)}</td>
//                <td class="empty-column">
//                    <img src="${garbageIconUrl}" class="delete-icon row" alt="Delete">
//                </td>
//            `;
//
//            tableBody.appendChild(row);
//        }
//    });

    // Add event listeners for quantity input fields
    document.querySelectorAll('.quantity-input').forEach(function (input) {
        input.addEventListener('focus', function (event) {
            event.target.select();
        });

//        input.addEventListener('change', function (event) {
//            const newQuantity = event.target.value;
//            const cartItemId = event.target.getAttribute('data-cart-id');
//            updateCartItem(cartItemId, newQuantity);
//        });
    });

    // Update summary table (optional, depending on your implementation)
    updateSummaryTable(cart);
}



document.querySelectorAll('.quantity-input').forEach(input => {
    input.addEventListener('change', function () {
        const newQuantity = parseInt(this.value);
        const cartItemId = this.closest('.cart-item-row').getAttribute('data-cart-id');
        console.log('cartItemId', cartItemId, 'newQuantity', newQuantity)

        // Call add_to_cart instead of update_cart
        fetch(`/add_to_cart`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                system_id: cartItemId,
                quantity: newQuantity
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update the cart UI with the new data
                addToCartTable(data.cart);
            } else {
                console.error('Failed to update cart', data.message);
            }
        })
        .catch(error => console.error('Error updating cart:', error));
    });
});


//function updateCartItem(cartItemId, newQuantity) {
//    console.log(`Updating cart item ${cartItemId} with new quantity: ${newQuantity}`);
//
//    fetch(`/update-cart`, {
//        method: 'POST',
//        headers: {
//            'Content-Type': 'application/json',
//        },
//        body: JSON.stringify({
//            cartItemId: cartItemId,
//            newQuantity: newQuantity
//        })
//    })
//    .then(response => response.json())
//    .then(data => {
//        if (data.success) {
//            console.log('Cart updated successfully');
//            // Optionally refresh the cart UI after the update
//        } else {
//            console.error('Failed to update the cart');
//        }
//    })
//    .catch(error => {
//        console.error('Error updating the cart:', error);
//    });
//}

//function addToCartTable(cartResponse) {
//    const cart = cartResponse.cart;  // Access the cart array from the response
//    console.log('cart', cart);
//    const tableBody = document.querySelector('.cart-items-table tbody');
//    const garbageIconUrl = document.getElementById('garbage-icon-url').getAttribute('data-url');
//
//    // Clear the cart table before rendering the updated items
//    tableBody.innerHTML = '';
//
//    cart.forEach(cartItem => {
//        const product = cartItem.product_name;
//        const brand = cartItem.brand;
//        const size = cartItem.size;
//        const basePrice = parseFloat(cartItem.base_price);
//        const discountedQuantity = cartItem.discounted_quantity;
//        const nonDiscountedQuantity = cartItem.non_discounted_quantity;
//        const discountAmount = cartItem.discount_amount;
//        const discountName = cartItem.discount_name || '';
//        const discountTaxable = cartItem.discount_taxable || false;
//        const taxRate = 0.09;
//        let tax;
//
//        // If there is both discounted and non-discounted quantity, create two rows
//        if (nonDiscountedQuantity > 0) {
//            tax = discountTaxable
//                ? basePrice * nonDiscountedQuantity * taxRate
//                : (basePrice - discountAmount) * nonDiscountedQuantity * taxRate;
//
//            const totalNonDiscounted = basePrice * nonDiscountedQuantity + tax;
//
//            let itemColumnContent = `
//                <div style="font-size: 0.9em;"><strong>${brand}</strong></div>
//                <div style="font-size: 0.8em;">${product}</div>
//                <div style="font-size: 0.6em;">${size}</div>`;
//
//            const row = document.createElement('tr');
//            row.className = 'cart-item-row';
//            row.setAttribute('data-upc', cartItem.upc);
//            row.setAttribute('data-system-id', cartItem.system_id);
//
//            row.innerHTML = `
//                <td class="item-column">
//                    ${itemColumnContent}
//                </td>
//                <td class="price-column">
//                    <span class="original-price">${basePrice.toFixed(2)}</span>
//                </td>
//                <td class="quantity-column">
//                    <input type="number" value="${nonDiscountedQuantity}" min="1" />
//                </td>
//                <td class="discounts-column"></td>
//                <td class="tax-column">${tax.toFixed(2)}</td>
//                <td class="total-column">${totalNonDiscounted.toFixed(2)}</td>
//                <td class="empty-column">
//                    <img src="${garbageIconUrl}" class="delete-icon row" alt="Delete">
//                </td>
//            `;
//
//            // Add event listeners to this row if needed
//            // ...
//
//            tableBody.appendChild(row);
//        }
//
//        if (discountedQuantity > 0) {
//            const discountedPrice = basePrice - (discountAmount / discountedQuantity);
//            tax = discountTaxable
//                ? discountedPrice * discountedQuantity * taxRate
//                : basePrice * discountedQuantity * taxRate;
//
//            const totalDiscounted = discountedQuantity === 'Free'
//                ? 0
//                : discountedPrice * discountedQuantity + tax;
//
//            let itemColumnContent = `
//                <div style="font-size: 0.9em;"><strong>${brand}</strong></div>
//                <div style="font-size: 0.8em;">${product}</div>
//                <div style="font-size: 0.6em;">${size}</div>`;
//
//            const row = document.createElement('tr');
//            row.className = 'cart-item-row';
//            row.setAttribute('data-upc', cartItem.upc);
//            row.setAttribute('data-system-id', cartItem.system_id);
//
//            row.innerHTML = `
//                <td class="item-column">
//                    ${itemColumnContent}
//                </td>
//                <td class="price-column">
//                    ${discountedQuantity === 'Free'
//                        ? `<span class="original-price" style="text-decoration: line-through;">${basePrice.toFixed(2)}</span><br>
//                           <span class="discounted-price">Free</span>`
//                        : `<span class="original-price" style="text-decoration: line-through;">${basePrice.toFixed(2)}</span><br>
//                           <span class="discounted-price">${discountedPrice.toFixed(2)}</span>`
//                    }
//                </td>
//                <td class="quantity-column">
//                    <input type="number" value="${discountedQuantity}" min="1" />
//                </td>
//                <td class="discounts-column ${discountTaxable ? 'taxable' : 'non-taxable'}">
//                    <span style="line-height: 1;">${discountAmount === 'Free' ? 'Free' : discountAmount.toFixed(2)}</span>
//                    <br><span class="discount-name">${discountName}</span>
//                </td>
//                <td class="tax-column">${tax.toFixed(2)}</td>
//                <td class="total-column">${totalDiscounted.toFixed(2)}</td>
//                <td class="empty-column">
//                    <img src="${garbageIconUrl}" class="delete-icon row" alt="Delete">
//                </td>
//            `;
//
//            // Add event listeners to this row if needed
//            // ...
//
//            tableBody.appendChild(row);
//        }
//    });
//
//    // Update summary table (optional, depending on your implementation)
//    updateSummaryTable(cart);
//}


//function addToCartTable(cartResponse) {
//    const cart = cartResponse.cart;  // Access the cart array from the response
//    console.log('cart', cart);
//    const tableBody = document.querySelector('.cart-items-table tbody');
//    const garbageIconUrl = document.getElementById('garbage-icon-url').getAttribute('data-url');
//
//    // Clear the cart table before rendering the updated items
//    tableBody.innerHTML = '';
//
//    cart.forEach(cartItem => {
//        const product = cartItem.product_name;
//        const quantity = cartItem.quantity;
//        const discount = cartItem.discount_amount || 0;
//        const discount_name = cartItem.discount_name || '';
//        const discount_taxable = cartItem.discount_taxable || false;
//        const price = parseFloat(cartItem.base_price);
//        const taxRate = 0.09;
//        let tax;
//
//
//        console.log('cartItem:', cartItem, ', product:', product, ', quantity:', quantity)
//        let itemColumnContent = '';
//        if (cartItem.brand) {
//            itemColumnContent += `<div style="font-size: 0.9em;"><strong>${cartItem.brand}</strong></div>`;
//        }
//        if (product) {
//            itemColumnContent += `<div style="font-size: 0.8em;">${product}</div>`;
//        }
//        if (cartItem.size) {
//            itemColumnContent += `<div style="font-size: 0.6em;">${cartItem.size} | ${cartItem.pets}</div>`;
//        } else {
//            itemColumnContent += `<div style="font-size: 0.6em;">${cartItem.pets}</div>`;
//        }
//
//        if (!discount_taxable) {
//            tax = (price - discount) * quantity * taxRate;
//        } else {
//            tax = price * quantity * taxRate;
//        }
//        const total = (price * quantity) + tax;
//
//        const row = document.createElement('tr');
//        row.className = 'cart-item-row';
//        row.setAttribute('data-upc', cartItem.upc);
//        row.setAttribute('data-system-id', cartItem.system_id);
//
//        row.innerHTML = `
//            <td class="item-column">
//                ${itemColumnContent}
//            </td>
//            <td class="price-column">
//                ${discount > 0
//                    ? `<span class="original-price" style="text-decoration: line-through;">${price.toFixed(2)}</span><br>
//                       <span class="discounted-price">${(price - discount).toFixed(2)}</span>`
//                    : `<span class="original-price">${price.toFixed(2)}</span>`
//                }
//            </td>
//            <td class="quantity-column">
//                <input type="number" value="${quantity}" min="1" />
//            </td>
//            <td class="discounts-column ${discount > 0 ? (discount_taxable ? 'taxable' : 'non-taxable') : ''}">
//                <span style="line-height: 1;">${discount.toFixed(2)}</span>
//                ${discount > 0 ? `<br><span class="discount-name">${discount_name}</span>` : ''}
//            </td>
//            <td class="tax-column">${tax.toFixed(2)}</td>
//            <td class="total-column">
//                ${discount > 0 ? (total - discount * quantity).toFixed(2) : total.toFixed(2)}
//            </td>
//            <td class="empty-column">
//                <img src="${garbageIconUrl}" class="delete-icon row" alt="Delete">
//            </td>
//        `;
//
//        // Add event listener to delete the item
//        row.querySelector('.delete-icon.row').addEventListener('click', () => {
//            removeFromCart(cartItem.system_id);  // Adjust this to correctly remove from the server-side cart
//            addToCartTable(cart);  // Re-render the cart table
//        });
//
//        // Add event listener to update total on quantity change
//        row.querySelector('.quantity-column input').addEventListener('change', function () {
//            const newQuantity = parseInt(this.value, 10);
//            updateCartQuantity(cartItem.system_id, newQuantity);  // Adjust this to correctly update the server-side cart
//            addToCartTable(cart);  // Re-render the cart table
//        });
//
//        tableBody.appendChild(row);
//    });
//
//    // Update summary table (optional, depending on your implementation)
//    updateSummaryTable(cart);
//}
//


//function addToCartTable(cartItems) {
//    console.log('cartItems', cartItems)
//    const tableBody = document.querySelector('.cart-items-table tbody');
//    const garbageIconUrl = document.getElementById('garbage-icon-url').getAttribute('data-url');
//
//    // Clear the cart table before rendering the updated items
//    tableBody.innerHTML = '';
//
//    cartItems.forEach(item => {
//        const row = document.createElement('tr');
//        row.className = 'cart-item-row';
//        row.setAttribute('data-upc', item.upc);
//        row.setAttribute('data-system-id', item.system_id);
//
//        const price = parseFloat(item.base_price);
//        const taxRate = 0.09;
//        let tax;
//
//        let itemColumnContent = '';
//        if (item.brand) {
//            itemColumnContent += `<div style="font-size: 0.9em;"><strong>${item.brand}</strong></div>`;
//        }
//        if (item.product_name) {
//            itemColumnContent += `<div style="font-size: 0.8em;">${item.product_name}</div>`;
//        }
//        if (item.size) {
//            itemColumnContent += `<div style="font-size: 0.6em;">${item.size} | ${item.pets}</div>`;
//        } else {
//            itemColumnContent += `<div style="font-size: 0.6em;">${item.pets}</div>`;
//        }
//
//        if (!item.discount_taxable) {
//            tax = (price - item.discount_amount) * item.quantity * taxRate;
//        } else {
//            tax = price * item.quantity * taxRate;
//        }
//        const total = (price * item.quantity) + tax;
//
//        row.innerHTML = `
//            <td class="item-column">
//                ${itemColumnContent}
//            </td>
//            <td class="price-column">
//                ${item.discount_amount > 0
//                    ? `<span class="original-price" style="text-decoration: line-through;">${price.toFixed(2)}</span><br>
//                       <span class="discounted-price">${(price - item.discount_amount).toFixed(2)}</span>`
//                    : `<span class="original-price">${price.toFixed(2)}</span>`
//                }
//            </td>
//            <td class="quantity-column">
//                <input type="number" value="${item.quantity}" min="1" />
//            </td>
//            <td class="discounts-column ${item.discount_amount > 0 ? (item.discount_taxable ? 'taxable' : 'non-taxable') : ''}">
//                <span style="line-height: 1;">${item.discount_amount.toFixed(2)}</span>
//                ${item.discount_name ? `<br><span class="discount-name">${item.discount_name}</span>` : ''}
//            </td>
//            <td class="tax-column">${tax.toFixed(2)}</td>
//            <td class="total-column">
//                ${(total).toFixed(2)}
//            </td>
//            <td class="empty-column">
//                <img src="${garbageIconUrl}" class="delete-icon row" alt="Delete">
//            </td>
//        `;
//
//        // Add event listener to delete the item
//        row.querySelector('.delete-icon.row').addEventListener('click', () => {
//            removeFromCart(item.cart_id);  // Pass cart_id to remove the item
//            addToCartTable(cartItems);  // Re-render the cart table
//        });
//
//        // Add event listener to update total on quantity change
//        row.querySelector('.quantity-column input').addEventListener('change', function () {
//            const newQuantity = parseInt(this.value, 10);
//            updateQuantity(item.cart_id, newQuantity);  // Update quantity in the backend
//            addToCartTable(cartItems);  // Re-render the cart table
//        });
//
//        tableBody.appendChild(row);
//    });
//
//    // Update summary table (optional, depending on your implementation)
//    updateSummaryTable(cartItems);
//}


//function addToCartTable(cart) {
//    console.log('cart', cart)
//    const tableBody = document.querySelector('.cart-items-table tbody');
//    const garbageIconUrl = document.getElementById('garbage-icon-url').getAttribute('data-url');
//
//    // Clear the cart table before rendering the updated items
//    tableBody.innerHTML = '';
//
//    for (const cartId in cart) {
//        if (cart.hasOwnProperty(cartId)) {
//            const cartItem = cart.items[cartId];
//            console.log('cartItem', cartItem);
//
//            const product = cartItem.product;
//            console.log('product', product);
//
//            const quantity = cartItem.quantity;
//            console.log('quantity', quantity);
//
//            const discount = cartItem.discount_amount || 0;
//            console.log('discount', discount);
//
//            // Assuming `discount_id` is available in the cartItem to reference Discounts
//            const discount_id = cartItem.discount_id || null;
//            let discount_name = '';
//
//            if (discount_id) {
//                // Fetch the discount details from the Discounts class using the discount_id
//                const discountDetails = cart.discounts.discounts[discount_id];
//                discount_name = discountDetails ? discountDetails.details : '';
//            }
//
//            console.log('discount_name:', discount_name);
//
//            const discount_taxable = cartItem.discount_taxable || false;
//            console.log('discount_taxable', discount_taxable);
//
//            const price = parseFloat(product.base_price);
//            console.log('price', price);
//
//            const taxRate = 0.09;
//            let tax;
//
//            let itemColumnContent = '';
//            if (product.brand) {
//                itemColumnContent += `<div style="font-size: 0.9em;"><strong>${product.brand}</strong></div>`;
//            }
//            if (product.short_name) {
//                itemColumnContent += `<div style="font-size: 0.8em;">${product.short_name}</div>`;
//            }
//            if (product.size) {
//                itemColumnContent += `<div style="font-size: 0.6em;">${product.size} | ${product.pets}</div>`;
//            } else {
//                itemColumnContent += `<div style="font-size: 0.6em;">${product.pets}</div>`;
//            }
//
//            // Calculate tax based on whether the discount is taxable
//            if (!discount_taxable) {
//                tax = (price - discount) * quantity * taxRate;
//            } else {
//                tax = price * quantity * taxRate;
//            }
//            const total = (price * quantity) + tax;
//
//            const row = document.createElement('tr');
//            row.className = 'cart-item-row';
//            row.setAttribute('data-upc', product.upc);
//            row.setAttribute('data-system-id', product.system_id);
//
//            // Fill the row with the correct data
//            row.innerHTML = `
//                <td class="item-column">
//                    ${itemColumnContent}
//                </td>
//                <td class="price-column">
//                    ${discount > 0
//                        ? `<span class="original-price" style="text-decoration: line-through;">${price.toFixed(2)}</span><br>
//                           <span class="discounted-price">${(price - discount).toFixed(2)}</span>`
//                        : `<span class="original-price">${price.toFixed(2)}</span>`
//                    }
//                </td>
//                <td class="quantity-column">
//                    <input type="number" value="${quantity}" min="1" />
//                </td>
//                <td class="discounts-column ${discount > 0 ? (discount_taxable ? 'taxable' : 'non-taxable') : ''}">
//                    <span style="line-height: 1;">${discount.toFixed(2)}</span>
//                    ${discount > 0 ? `<br><span class="discount-name">${discount_name}</span>` : ''}
//                </td>
//                <td class="tax-column">${tax.toFixed(2)}</td>
//                <td class="total-column">
//                    ${total.toFixed(2)}
//                </td>
//                <td class="empty-column">
//                    <img src="${garbageIconUrl}" class="delete-icon row" alt="Delete">
//                </td>
//            `;
//
//            // Add event listener to delete the item
//            row.querySelector('.delete-icon.row').addEventListener('click', () => {
//                cart.remove_item(cartId);  // Remove the item from the cart class
//                addToCartTable(cart);  // Re-render the cart table
//            });
//
//            // Add event listener to update total on quantity change
//            row.querySelector('.quantity-column input').addEventListener('change', function () {
//                const newQuantity = parseInt(this.value, 10);
//                cart.update_quantity(cartId, newQuantity);  // Update quantity in the cart class
//                addToCartTable(cart);  // Re-render the cart table
//            });
//
//            tableBody.appendChild(row);
//        }
//    }
//
//    // Update summary table (optional, depending on your implementation)
//    updateSummaryTable(cart);
//}

//function addToCartTable(cart) {
//    console.log('Cart data:', cart);
//    const tableBody = document.querySelector('.cart-items-table tbody');
//    const garbageIconUrl = document.getElementById('garbage-icon-url').getAttribute('data-url');
//
//    console.log('Updating cart table...');
//
//    // Clear the cart table before rendering the updated items
//    tableBody.innerHTML = '';
//
//    for (const cartId in cart.items) {
//        const cartItem = cart.items[cartId];
//        console.log('cartItem', cartItem);
//        const product = cartItem.product;
//        console.log('product', product);
//        const quantity = cartItem.quantity;
//        console.log('quantity', quantity);
//        const discount = cartItem.discount_amount || 0;
//        console.log('discount', discount);
//        const discount_name = cartItem.discount_name || '';
//        console.log('discount_name', discount_name);
//        const discount_taxable = cartItem.discount_taxable || false;
//        console.log(' discount_taxable',  discount_taxable);
//        const price = parseFloat(product.base_price);
//        console.log('price', price);
//        const taxRate = 0.09;
//        let tax;
//
//        let itemColumnContent = '';
//        if (product.brand) {
//            itemColumnContent += `<div style="font-size: 0.9em;"><strong>${product.brand}</strong></div>`;
//        }
//        if (product.short_name) {
//            itemColumnContent += `<div style="font-size: 0.8em;">${product.short_name}</div>`;
//        }
//        if (product.size) {
//            itemColumnContent += `<div style="font-size: 0.6em;">${product.size} | ${product.pets}</div>`;
//        } else {
//            itemColumnContent += `<div style="font-size: 0.6em;">${product.pets}</div>`;
//        }
//
//        if (!discount_taxable) {
//            tax = (price - discount) * quantity * taxRate;
//        } else {
//            tax = price * quantity * taxRate;
//        }
//        const total = (price * quantity) + tax;
//
//        const row = document.createElement('tr');
//        row.className = 'cart-item-row';
//        row.setAttribute('data-upc', product.upc);
//        row.setAttribute('data-system-id', product.system_id);
//
//        row.innerHTML = `
//            <td class="item-column">
//                ${itemColumnContent}
//            </td>
//            <td class="price-column">
//                ${discount > 0
//                    ? `<span class="original-price" style="text-decoration: line-through;">${price.toFixed(2)}</span><br>
//                       <span class="discounted-price">${(price - discount).toFixed(2)}</span>`
//                    : `<span class="original-price">${price.toFixed(2)}</span>`
//                }
//            </td>
//            <td class="quantity-column">
//                <input type="number" value="${quantity}" min="1" />
//            </td>
//            <td class="discounts-column ${discount > 0 ? (discount_taxable ? 'taxable' : 'non-taxable') : ''}">
//                <span style="line-height: 1;">${discount.toFixed(2)}</span>
//                ${discount > 0 ? `<br><span class="discount-name">${discount_name}</span>` : ''}
//            </td>
//            <td class="tax-column">${tax.toFixed(2)}</td>
//            <td class="total-column">
//                ${discount > 0 ? (total - discount * quantity).toFixed(2) : total.toFixed(2)}
//            </td>
//            <td class="empty-column">
//                <img src="${garbageIconUrl}" class="delete-icon row" alt="Delete">
//            </td>
//        `;
//
//        console.log('Appending row to table:', row.innerHTML);
//        tableBody.appendChild(row);  // Ensure this line is being executed
//        console.log('Table updated:', tableBody.innerHTML);
//
//        // Add event listener to delete the item
//        row.querySelector('.delete-icon.row').addEventListener('click', () => {
//            cart.remove_item(cartId);  // Remove the item from the cart class
//            addToCartTable(cart);  // Re-render the cart table
//        });
//
//        // Add event listener to update total on quantity change
//        row.querySelector('.quantity-column input').addEventListener('change', function () {
//            const newQuantity = parseInt(this.value, 10);
//            cart.update_quantity(cartId, newQuantity);  // Update quantity in the cart class
//            addToCartTable(cart);  // Re-render the cart table
//        });
//    }
//
//    // Update summary table (optional, depending on your implementation)
//    updateSummaryTable(cart);
//}

//function addToCartTable(cart) {
//    const tableBody = document.querySelector('.cart-items-table tbody');
//    const garbageIconUrl = document.getElementById('garbage-icon-url').getAttribute('data-url');
//
//    // Clear the cart table before rendering the updated items
//    tableBody.innerHTML = '';
//
//    for (const cartId in cart.items) {
//        const cartItem = cart.items[cartId];
//        const product = cartItem.product;
//        const quantity = cartItem.quantity;
//        const discount = cartItem.discount_amount || 0;
//        const discount_name = cartItem.discount_name || '';
//        const discount_taxable = cartItem.discount_taxable || false;
//        const price = parseFloat(product.base_price);
//        const taxRate = 0.09;
//        let tax;
//
//        let itemColumnContent = '';
//        if (product.brand) {
//            itemColumnContent += `<div style="font-size: 0.9em;"><strong>${product.brand}</strong></div>`;
//        }
//        if (product.short_name) {
//            itemColumnContent += `<div style="font-size: 0.8em;">${product.short_name}</div>`;
//        }
//        if (product.size) {
//            itemColumnContent += `<div style="font-size: 0.6em;">${product.size} | ${product.pets}</div>`;
//        } else {
//            itemColumnContent += `<div style="font-size: 0.6em;">${product.pets}</div>`;
//        }
//
//        if (!discount_taxable) {
//            tax = (price - discount) * quantity * taxRate;
//        } else {
//            tax = price * quantity * taxRate;
//        }
//        const total = (price * quantity) + tax;
//
//        const row = document.createElement('tr');
//        row.className = 'cart-item-row';
//        row.setAttribute('data-upc', product.upc);
//        row.setAttribute('data-system-id', product.system_id);
//
//        row.innerHTML = `
//            <td class="item-column">
//                ${itemColumnContent}
//            </td>
//            <td class="price-column">
//                ${discount > 0
//                    ? `<span class="original-price" style="text-decoration: line-through;">${price.toFixed(2)}</span><br>
//                       <span class="discounted-price">${(price - discount).toFixed(2)}</span>`
//                    : `<span class="original-price">${price.toFixed(2)}</span>`
//                }
//            </td>
//            <td class="quantity-column">
//                <input type="number" value="${quantity}" min="1" />
//            </td>
//            <td class="discounts-column ${discount > 0 ? (discount_taxable ? 'taxable' : 'non-taxable') : ''}">
//                <span style="line-height: 1;">${discount.toFixed(2)}</span>
//                ${discount > 0 ? `<br><span class="discount-name">${discount_name}</span>` : ''}
//            </td>
//            <td class="tax-column">${tax.toFixed(2)}</td>
//            <td class="total-column">
//                ${discount > 0 ? (total - discount * quantity).toFixed(2) : total.toFixed(2)}
//            </td>
//            <td class="empty-column">
//                <img src="${garbageIconUrl}" class="delete-icon row" alt="Delete">
//            </td>
//        `;
//
//        // Add event listener to delete the item
//        row.querySelector('.delete-icon.row').addEventListener('click', () => {
//            cart.remove_item(cartId);  // Remove the item from the cart class
//            addToCartTable(cart);  // Re-render the cart table
//        });
//
//        // Add event listener to update total on quantity change
//        row.querySelector('.quantity-column input').addEventListener('change', function () {
//            const newQuantity = parseInt(this.value, 10);
//            cart.update_quantity(cartId, newQuantity);  // Update quantity in the cart class
//            addToCartTable(cart);  // Re-render the cart table
//        });
//
//        tableBody.appendChild(row);
//    }
//
//    // Update summary table (optional, depending on your implementation)
//    updateSummaryTable(cart);
////    adjustAvailableOffersHeight();
////    updateTotalTableVisibility();
//}


function removeFromCart(cart, cartId) {
    cart.remove_item(cartId);
    addToCartTable(cart);
}

function updateSummaryTable(cart) {
    let grossSales = 0;
    let totalTax = 0;
    let netSales = 0;
    let discountAmount = 0;
    let taxableSale = 0;

    for (const cartId in cart.items) {
        const cartItem = cart.items[cartId];
        const product = cartItem.product;
        const quantity = cartItem.quantity;
        const discount = cartItem.discount_amount || 0;
        const price = parseFloat(product.base_price);
        const taxRate = 0.09;
        const discount_taxable = cartItem.discount_taxable || false;

        grossSales += price * quantity;
        discountAmount += discount * quantity;

        if (discount_taxable) {
            taxableSale += price * quantity;
        } else {
            taxableSale += (price - discount) * quantity;
        }

        totalTax += taxableSale * taxRate;
        netSales += (price * quantity) - discountAmount;
    }

    const total = netSales + totalTax;

    document.querySelector('.total-table-amount.gross-sale').innerText = grossSales.toFixed(2);
    document.querySelector('.total-table-amount.discounts').innerText = discountAmount.toFixed(2);
    document.querySelector('.total-table-amount.net-sale').innerText = netSales.toFixed(2);
    document.querySelector('.total-table-amount.taxable-sales').innerText = taxableSale.toFixed(2);
    document.querySelector('.total-table-amount.total-tax').innerText = totalTax.toFixed(2);
    document.querySelector('.total-table-amount-total.total').innerText = total.toFixed(2);
}

document.addEventListener('DOMContentLoaded', function() {
    let barcodeInput = '';  // Accumulates the barcode characters
    let lastKeyTime = Date.now();  // Track the time of the last keypress
    const searchInput = document.querySelector('#customer-search-input');
    const customerSuggestionsContainer = document.querySelector('.suggestions');

    // Handle global barcode input
    document.addEventListener('keydown', function(event) {
        const currentTime = Date.now();

        if (currentTime - lastKeyTime > 100) {
            barcodeInput = '';  // Reset the barcode input
        }

        lastKeyTime = currentTime;

        if (event.key !== 'Enter') {
            barcodeInput += event.key;
        } else {
            if (barcodeInput.length > 0) {
                console.log('Barcode scanned:', barcodeInput);
                addCustomerToCartById(barcodeInput.trim());
                barcodeInput = '';  // Reset after processing
            }
        }
    });

    searchInput.addEventListener('input', function() {
        const query = searchInput.value.trim();
        if (query.length > 3) {
            fetchCustomerSuggestions(query);
        } else {
            customerSuggestionsContainer.style.display = 'none';  // Hide suggestions if query is too short
        }
    });

    function fetchCustomerSuggestions(query) {
        fetch(`/search_customer?query=${query}`)
            .then(response => response.json())
            .then(data => {
                customerSuggestionsContainer.innerHTML = '';  // Clear previous suggestions
                if (data.length > 0) {
                    data.forEach(item => {
                        const suggestionItem = document.createElement('li');
                        suggestionItem.textContent = `${item.name} (${item.contact_info})`;
                        suggestionItem.dataset.customerId = item.customer_id;
                        customerSuggestionsContainer.appendChild(suggestionItem);

                        suggestionItem.addEventListener('click', function() {
                            addCustomerToCart(item.customer_id);
                            customerSuggestionsContainer.style.display = 'none';  // Hide suggestions after selection
                        });
                    });

                    customerSuggestionsContainer.style.display = 'block';
                } else {
                    customerSuggestionsContainer.style.display = 'none';
                }
            })
            .catch(error => console.error('Error fetching customer suggestions:', error));
    }

    function addCustomerToCart(customerId) {
        fetch('/add_customer_to_cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ customer_id: customerId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Customer added to cart:', data.message);
            } else {
                console.error('Error adding customer to cart:', data.message);
            }
        })
        .catch(error => console.error('Error adding customer to cart:', error));
    }

    function addCustomerToCartById(customerId) {
        addCustomerToCart(customerId);  // Same logic as adding by ID
    }
});


