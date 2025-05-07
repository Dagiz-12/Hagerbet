// Cart functionality with AJAX
document.addEventListener("DOMContentLoaded", function() {
  // Update cart count on page load
  updateCartCount();
  
  // Handle cart icon click - redirect to cart page
  document.querySelectorAll('.cart-icon, .nav-icon.cart').forEach(icon => {
      icon.addEventListener('click', function(e) {
          e.preventDefault();
          window.location.href = '/cart/';
      });
  });
  
  // Handle add to cart buttons
  document.addEventListener('click', function(e) {
      if (e.target.classList.contains('add-to-cart') || e.target.closest('.add-to-cart')) {
          e.preventDefault();
          const button = e.target.classList.contains('add-to-cart') ? 
                       e.target : e.target.closest('.add-to-cart');
          
          let quantity = 1;
          const quantityInput = button.closest('.product-actions') ? 
                               button.closest('.product-actions').querySelector('.quantity-input') : 
                               null;
          if (quantityInput) {
              quantity = parseInt(quantityInput.value) || 1;
          }

          const product = {
              id: button.dataset.id,
              name: button.dataset.name,
              price: parseFloat(button.dataset.price),
              image: button.dataset.image,
              quantity: quantity,
              description: button.dataset.description || ''
          };
          
          if (!isNaN(product.price)) {
              addToCart(product);
          }
      }
  });
});

// Add to cart with AJAX
function addToCart(product) {
  fetch('/cart/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({
          action: 'add',
          product_id: product.id,
          name: product.name,
          price: product.price,
          image: product.image,
          quantity: product.quantity,
          description: product.description
      })
  })
  .then(response => {
      if (!response.ok) {
          return response.json().then(err => { throw err; });
      }
      return response.json();
  })
  .then(data => {
      if (data.status === 'success') {
          updateCartCount(data.cart_count);
          showNotification(`${product.name} (${product.quantity}) added to cart`);
          
          // Redirect to cart page if on product detail page
          if (window.location.pathname.includes('/products/')) {
              window.location.href = '/cart/';
          }
      }
  })
  .catch(error => {
      console.error('Error:', error);
      showNotification(error.message || 'Failed to add to cart');
  });
}

// Update cart item quantity with AJAX
// ... (keep all your existing cart.js code until the updateCartItem function) ...

// Update cart item quantity with AJAX - fixed version
function updateCartItem(productId, change) {
  fetch('/cart/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({
          action: 'update',
          product_id: productId,
          change: change
      })
  })
  .then(response => {
      if (!response.ok) {
          return response.json().then(err => { throw err; });
      }
      return response.json();
  })
  .then(data => {
      if (data.status === 'success') {
          updateCartCount(data.cart_count);
          showNotification('Cart updated');
          
          // Update the quantity display without reloading
          const quantityElement = document.querySelector(`.cart-item[data-id="${productId}"] .quantity`);
          if (quantityElement) {
              const currentQuantity = parseInt(quantityElement.textContent);
              const newQuantity = currentQuantity + change;
              
              if (newQuantity > 0) {
                  quantityElement.textContent = newQuantity;
              } else {
                  // If quantity reaches 0, remove the item from DOM
                  document.querySelector(`.cart-item[data-id="${productId}"]`)?.remove();
              }
          }
          
          // Update the cart summary
          updateCartSummary();
      }
  })
  .catch(error => {
      console.error('Error:', error);
      showNotification(error.message || 'Failed to update cart');
  });
}

// Add this new function to update cart summary
function updateCartSummary() {
  fetch('/cart/summary/')
      .then(response => response.json())
      .then(data => {
          if (data.status === 'success') {
              document.querySelector('.summary-row:nth-child(1) span:last-child').textContent = `$${data.subtotal.toFixed(2)}`;
              document.querySelector('.summary-total span:last-child').textContent = `$${data.total.toFixed(2)}`;
          }
      })
      .catch(error => console.error('Error:', error));
}


// Remove cart item with AJAX
function removeCartItem(productId) {
  fetch('/cart/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({
          action: 'remove',
          product_id: productId
      })
  })
  .then(response => {
      if (!response.ok) {
          return response.json().then(err => { throw err; });
      }
      return response.json();
  })
  .then(data => {
      if (data.status === 'success') {
          updateCartCount(data.cart_count);
          showNotification('Item removed from cart');
          // Reload the page to reflect changes
          window.location.reload();
      }
  })
  .catch(error => {
      console.error('Error:', error);
      showNotification(error.message || 'Failed to remove item');
  });
}

// Update cart count in navbar
function updateCartCount(count = null) {
  if (count === null) {
      // Get current count from server if not provided
      fetch('/cart/count/')
          .then(response => response.json())
          .then(data => {
              setCartCount(data.count);
          })
          .catch(error => console.error('Error:', error));
  } else {
      setCartCount(count);
  }
}

function setCartCount(count) {
  const countElements = document.querySelectorAll('.cart-count');
  countElements.forEach(element => {
      element.textContent = count;
      element.style.display = count > 0 ? 'flex' : 'none';
  });
}

// Helper function to get CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

// Show notification
function showNotification(message) {
  const notification = document.createElement('div');
  notification.className = 'cart-notification';
  notification.textContent = message;
  document.body.appendChild(notification);

  setTimeout(() => {
      notification.classList.add('fade-out');
      setTimeout(() => notification.remove(), 300);
  }, 2000);
}