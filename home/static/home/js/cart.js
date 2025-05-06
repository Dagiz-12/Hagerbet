// cart.js
document.addEventListener("DOMContentLoaded", function () {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    updateCartCount();
  
    // Update cart count display
    function updateCartCount() {
      const count = cart.reduce((total, item) => total + item.quantity, 0);
      const cartCountElements = document.querySelectorAll("#cart-count");
      cartCountElements.forEach(cartCount => {
        if (cartCount) {
          cartCount.textContent = count;
          cartCount.style.display = count > 0 ? "block" : "none";
        }
      });
    }
  
    // Render cart items in the dropdown
    function renderCartItems() {
      const cartItemsContainer = document.getElementById("cart-items");
      const cartTotalElement = document.getElementById("cart-total");
  
      if (!cartItemsContainer || !cartTotalElement) return;
  
      if (cart.length === 0) {
        cartItemsContainer.innerHTML =
          '<p class="empty-cart-message">Your cart is empty</p>';
        cartTotalElement.textContent = "0.00";
        return;
      }
  
      let total = 0;
      let itemsHTML = "";
  
      cart.forEach((item) => {
        if (!item.price || isNaN(item.price)) {
          console.warn(`Invalid price for item: ${item.name}`);
          return;
        }
  
        total += item.price * item.quantity;
        itemsHTML += `
          <div class="cart-item" data-product-id="${item.id}">
            <img src="${item.image}" alt="${item.name}" class="cart-item-image">
            <div class="cart-item-details">
              <h5>${item.name}</h5>
              <p class="cart-item-price">$${item.price.toFixed(2)}</p>
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
  
      // Add event listeners for quantity controls
      document.querySelectorAll(".quantity-btn.minus").forEach((btn) => {
        btn.addEventListener("click", function () {
          const productId = this.closest(".cart-item").dataset.productId;
          updateCartItemQuantity(productId, -1);
        });
      });
  
      document.querySelectorAll(".quantity-btn.plus").forEach((btn) => {
        btn.addEventListener("click", function () {
          const productId = this.closest(".cart-item").dataset.productId;
          updateCartItemQuantity(productId, 1);
        });
      });
  
      document.querySelectorAll(".remove-item").forEach((btn) => {
        btn.addEventListener("click", function () {
          const productId = this.closest(".cart-item").dataset.productId;
          removeCartItem(productId);
        });
      });
    }
  
    function updateCartItemQuantity(productId, change) {
      const item = cart.find((item) => item.id == productId);
      if (item) {
        item.quantity += change;
        if (item.quantity <= 0) {
          cart = cart.filter((item) => item.id != productId);
        }
        localStorage.setItem("cart", JSON.stringify(cart));
        updateCartCount();
        renderCartItems();
        showCartNotification(`Quantity updated for ${item.name}`);
      }
    }
  
    function removeCartItem(productId) {
      const item = cart.find(item => item.id == productId);
      cart = cart.filter((item) => item.id != productId);
      localStorage.setItem("cart", JSON.stringify(cart));
      updateCartCount();
      renderCartItems();
      if (item) {
        showCartNotification(`${item.name} removed from cart`);
      }
    }
  
    // Cart dropdown toggle
    const cartIcon = document.querySelector(".nav-icon.cart");
    const cartDropdown = document.getElementById("cart-dropdown");
    const closeCart = document.getElementById("close-cart");
  
    if (cartIcon) {
      cartIcon.addEventListener("click", (e) => {
        e.stopPropagation();
        cartDropdown.classList.toggle("show");
        if (cartDropdown.classList.contains("show")) {
          renderCartItems();
        }
      });
    }
  
    if (closeCart) {
      closeCart.addEventListener("click", () => {
        cartDropdown.classList.remove("show");
      });
    }
  
    // Close cart when clicking outside
    document.addEventListener("click", (e) => {
      if (cartDropdown && !cartDropdown.contains(e.target) && !e.target.closest(".nav-icon.cart")) {
        cartDropdown.classList.remove("show");
      }
    });
  
    // Show notification
    function showCartNotification(message) {
      const notification = document.createElement("div");
      notification.className = "cart-notification";
      notification.textContent = message;
      document.body.appendChild(notification);
  
      setTimeout(() => {
        notification.classList.add("fade-out");
        setTimeout(() => notification.remove(), 300);
      }, 2000);
    }
  
    // Add to cart functionality
    document.addEventListener("click", function(e) {
      if (e.target.classList.contains("add-to-cart")) {
        e.preventDefault();
        const button = e.target;
        const productId = button.dataset.id;
        const productName = button.dataset.name;
        const productPrice = parseFloat(button.dataset.price);
        const productImage = button.dataset.image;
  
        if (isNaN(productPrice) {
          console.error("Invalid product price");
          return;
        }
  
        // Check if product is already in cart
        const existingItem = cart.find((item) => item.id == productId);
        if (existingItem) {
          existingItem.quantity += 1;
          showCartNotification(`${existingItem.name} quantity updated`);
        } else {
          // Add new product to cart
          cart.push({
            id: productId,
            name: productName,
            price: productPrice,
            image: productImage,
            quantity: 1
          });
          showCartNotification(`${productName} added to cart`);
        }
  
        // Save to localStorage
        localStorage.setItem("cart", JSON.stringify(cart));
        updateCartCount();
        renderCartItems();
      }
    });
  
    // Initialize cart on page load
    renderCartItems();
  });