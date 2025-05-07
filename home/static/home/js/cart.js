// cart.js
document.addEventListener("DOMContentLoaded", function() {
    // Initialize cart from localStorage
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    
    // Update cart count in navbar
    function updateCartCount() {
      const count = cart.reduce((total, item) => total + item.quantity, 0);
      document.querySelectorAll('.cart-count').forEach(element => {
        element.textContent = count;
        element.style.display = count > 0 ? "block" : "none";
      });
    }
  
    // Render cart items in dropdown
    function renderCartDropdown() {
      const cartItemsContainer = document.getElementById("cart-items");
      const cartTotalElement = document.getElementById("cart-total");
      
      if (!cartItemsContainer || !cartTotalElement) return;
  
      if (cart.length === 0) {
        cartItemsContainer.innerHTML = '<p class="empty-cart-message">Your cart is empty</p>';
        cartTotalElement.textContent = "0.00";
        return;
      }
  
      let itemsHTML = "";
      let total = 0;
  
      cart.forEach(item => {
        const itemTotal = item.price * item.quantity;
        total += itemTotal;
        
        itemsHTML += `
          <div class="cart-item" data-id="${item.id}">
            <img src="${item.image}" alt="${item.name}" class="cart-item-image">
            <div class="cart-item-details">
              <h5>${item.name}</h5>
              <p>$${item.price.toFixed(2)}</p>
              <div class="quantity-controls">
                <button class="quantity-btn minus">-</button>
                <span class="quantity">${item.quantity}</span>
                <button class="quantity-btn plus">+</button>
              </div>
            </div>
            <button class="remove-item">×</button>
          </div>
        `;
      });
  
      cartItemsContainer.innerHTML = itemsHTML;
      cartTotalElement.textContent = total.toFixed(2);
  
      // Add event listeners to cart dropdown buttons
      document.querySelectorAll('.minus').forEach(btn => {
        btn.addEventListener('click', function() {
          const itemId = this.closest('.cart-item').dataset.id;
          updateCartItem(itemId, -1);
        });
      });
  
      document.querySelectorAll('.plus').forEach(btn => {
        btn.addEventListener('click', function() {
          const itemId = this.closest('.cart-item').dataset.id;
          updateCartItem(itemId, 1);
        });
      });
  
      document.querySelectorAll('.remove-item').forEach(btn => {
        btn.addEventListener('click', function() {
          const itemId = this.closest('.cart-item').dataset.id;
          removeCartItem(itemId);
        });
      });
    }
  
    // Update cart item quantity
    function updateCartItem(productId, change) {
      const itemIndex = cart.findIndex(item => item.id == productId);
      if (itemIndex === -1) return;
  
      cart[itemIndex].quantity += change;
  
      if (cart[itemIndex].quantity <= 0) {
        cart.splice(itemIndex, 1);
      }
  
      saveCart();
      updateCartCount();
      renderCartDropdown();
      showNotification(`Cart updated`);
    }
  
    // Remove item from cart
    function removeCartItem(productId) {
      cart = cart.filter(item => item.id != productId);
      saveCart();
      updateCartCount();
      renderCartDropdown();
      showNotification(`Item removed from cart`);
    }
  
    // Add item to cart
    function addToCart(product) {
      const existingItem = cart.find(item => item.id == product.id);
      
      if (existingItem) {
        existingItem.quantity += 1;
      } else {
        cart.push({
          id: product.id,
          name: product.name,
          price: product.price,
          image: product.image,
          quantity: 1
        });
      }
  
      saveCart();
      updateCartCount();
      renderCartDropdown();
      showNotification(`${product.name} added to cart`);
    }
  
    // Save cart to localStorage
    function saveCart() {
      localStorage.setItem("cart", JSON.stringify(cart));
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
  
    // Initialize cart display
    updateCartCount();
  
    // Cart dropdown toggle
    const cartIcon = document.querySelector('.nav-icon.cart');
    const cartDropdown = document.getElementById('cart-dropdown');
    const closeCart = document.getElementById('close-cart');
  
    if (cartIcon && cartDropdown) {
      cartIcon.addEventListener('click', (e) => {
        e.stopPropagation();
        cartDropdown.classList.toggle('show');
        if (cartDropdown.classList.contains('show')) {
          renderCartDropdown();
        }
      });
    }
  
    if (closeCart) {
      closeCart.addEventListener('click', () => {
        cartDropdown.classList.remove('show');
      });
    }
  
    // Close cart when clicking outside
    document.addEventListener('click', (e) => {
      if (!cartDropdown.contains(e.target) && !e.target.closest('.nav-icon.cart')) {
        cartDropdown.classList.remove('show');
      }
    });
  
    // Add to cart button handler
    document.addEventListener('click', function(e) {
      if (e.target.classList.contains('add-to-cart')) {
        e.preventDefault();
        const button = e.target;
        const product = {
          id: button.dataset.id,
          name: button.dataset.name,
          price: parseFloat(button.dataset.price),
          image: button.dataset.image
        };
        
        if (!isNaN(product.price)) {
          addToCart(product);
          
          // Open cart dropdown
          if (cartDropdown) {
            cartDropdown.classList.add('show');
            renderCartDropdown();
          }
        }
      }
    });
  
// Update the sidebar toggle part in your cart.js
const openSidebar = document.getElementById('open-sidebar');
const closeSidebar = document.getElementById('close-sidebar');
const sidebar = document.getElementById('sidebar');

if (openSidebar && sidebar) {
  openSidebar.addEventListener('click', (e) => {
    e.stopPropagation();
    sidebar.style.left = '0';
  });
}

if (closeSidebar && sidebar) {
  closeSidebar.addEventListener('click', () => {
    sidebar.style.left = '-300px';
  });
}

// Close sidebar when clicking outside
document.addEventListener('click', (e) => {
  if (sidebar && !sidebar.contains(e.target) && !e.target.closest('#open-sidebar')) {
    sidebar.style.left = '-300px';
  }
});