// search.js
document.addEventListener("DOMContentLoaded", function() {
    // Search functionality
    const searchInput = document.querySelector('.search-bar input');
    const categoryDropdown = document.querySelector('.category-dropdown');
    const productsGrid = document.querySelector('.products-grid');
    
    if (searchInput && categoryDropdown && productsGrid) {
      // Store original products HTML for reset
      const originalProductsHTML = productsGrid.innerHTML;
      
      // Search when typing (with debounce)
      let searchTimeout;
      searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(performSearch, 300);
      });
      
      // Search when category changes
      categoryDropdown.addEventListener('change', performSearch);
      
      function performSearch() {
        const searchTerm = searchInput.value.trim().toLowerCase();
        const selectedCategory = categoryDropdown.value.toLowerCase();
        
        // If both search term and category are empty, reset to original
        if (!searchTerm && selectedCategory === 'all') {
          productsGrid.innerHTML = originalProductsHTML;
          return;
        }
        
        // Get all product cards
        const productCards = productsGrid.querySelectorAll('.product-card');
        let hasResults = false;
        
        productCards.forEach(card => {
          const cardCategory = (card.dataset.category || '').toLowerCase();
          const cardTitle = card.querySelector('h3').textContent.toLowerCase();
          const cardDesc = card.querySelector('p').textContent.toLowerCase();
          
          // Check category match
          const categoryMatch = selectedCategory === 'all' || 
                              cardCategory === selectedCategory;
          
          // Check search term match
          const searchMatch = !searchTerm || 
                            cardTitle.includes(searchTerm) || 
                            cardDesc.includes(searchTerm);
          
          if (categoryMatch && searchMatch) {
            card.style.display = 'block';
            hasResults = true;
          } else {
            card.style.display = 'none';
          }
        });
        
        // Show no results message if needed
        const noResultsMsg = productsGrid.querySelector('.no-results');
        if (!hasResults) {
          if (!noResultsMsg) {
            const msg = document.createElement('p');
            msg.className = 'no-results';
            msg.textContent = 'No products found matching your criteria.';
            productsGrid.appendChild(msg);
          }
        } else if (noResultsMsg) {
          noResultsMsg.remove();
        }
        
        // Reinitialize cart functionality for any new elements
        initializeCart();
      }
    }
    
    function initializeCart() {
      // Reattach event listeners to any new add-to-cart buttons
      document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function(e) {
          e.preventDefault();
          const product = {
            id: this.dataset.id,
            name: this.dataset.name,
            price: parseFloat(this.dataset.price),
            image: this.dataset.image
          };
          
          if (!isNaN(product.price)) {
            // Call addToCart function from cart.js
            if (typeof addToCart === 'function') {
              addToCart(product);
            }
          }
        });
      });
    }
  });