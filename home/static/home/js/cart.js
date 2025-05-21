document.addEventListener("DOMContentLoaded", function() {
    // Handle quantity buttons on product pages
    document.querySelectorAll('.quantity-btn').forEach(button => {
        button.addEventListener('click', function() {
            const input = this.parentElement.querySelector('.quantity-input');
            const formInput = this.closest('.product-actions')?.querySelector('.form-quantity-input');
            let value = parseInt(input.value);
            
            if (this.classList.contains('minus') && value > 1) {
                value -= 1;
            } else if (this.classList.contains('plus')) {
                value += 1;
            }
            
            input.value = value;
            if (formInput) formInput.value = value;
        });
    });

    // Update cart count in navbar
    function updateNavCartCount() {
        fetch('/cart/count/')
            .then(response => response.json())
            .then(data => {
                document.querySelectorAll('.cart-count').forEach(element => {
                    element.textContent = data.count;
                });
            });
    }

    // Update count every 2 seconds
    setInterval(updateNavCartCount, 2000);
    updateNavCartCount(); // Initial update
});

function addToCart(productId, productName, productPrice, productImage, quantity = 1) {
    
    
    if (!productId || isNaN(productId)) {
        console.error('Invalid product ID');
        return;
    }

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    if (!csrfToken) {
        console.error('CSRF token missing');
        return;
    }

    const formData = new FormData();
    formData.append('product_id', productId);
    formData.append('quantity', quantity);
    formData.append('csrfmiddlewaretoken', csrfToken);

    fetch(`/cart/add/${productId}/`, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) throw new Error('Network error');
        return response.json().catch(() => ({ success: false }));
    })
    .then(data => {
        if (data.success) {
            updateNavCartCount();
            showCartNotification(`${productName} added to cart`);
        }
    })
    .catch(error => console.error('Error:', error));
}

function showCartNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'cart-notification';
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('fade-out');
        setTimeout(() => notification.remove(), 300);
    }, 2000);
}

// Update cart dropdown
function updateCartDropdown() {
    const cartDropdown = document.querySelector('.cart-dropdown .cart-items');
    if (!cartDropdown) return;

    fetch('/cart/view/')
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const cartItems = doc.querySelector('.cart-items');
            if (cartItems) {
                cartDropdown.innerHTML = cartItems.innerHTML;
            }
        });
}

// Initialize cart buttons on page load
function initializeCartButtons() {
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.id;
            const productName = this.dataset.name;
            const productPrice = this.dataset.price;
            const productImage = this.dataset.image;
            const quantity = this.closest('.product-actions')?.querySelector('.quantity-input')?.value || 1;
            
            addToCart(productId, productName, productPrice, productImage, parseInt(quantity));
        });
    });
}

document.addEventListener('DOMContentLoaded', initializeCartButtons);