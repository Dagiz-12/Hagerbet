document.addEventListener("DOMContentLoaded", function() {
    initCurrencyConverter();
});

async function initCurrencyConverter() {
    const locationDropdown = document.getElementById('location-dropdown');
    const currencyDisplay = document.querySelector('.location-selector .icon-label');
    let exchangeRates = {};
    let baseCurrency = 'USD';

    // Fetch exchange rates
    async function fetchExchangeRates() {
        try {
            const response = await fetch(`https://api.exchangerate-api.com/v4/latest/${baseCurrency}`);
            if (!response.ok) throw new Error('Failed to fetch rates');
            const data = await response.json();
            exchangeRates = data.rates;
        } catch (error) {
            console.error('Using fallback rates:', error);
            exchangeRates = {
                USD: 1, GBP: 0.79, EUR: 0.93, CAD: 1.36, ETB: 56.5
            };
        }
    }

    // Convert all prices on page
    function convertPrices(targetCurrency) {
        if (!exchangeRates[targetCurrency]) return;

        const rate = exchangeRates[targetCurrency];
        currencyDisplay.textContent = targetCurrency;

        // Convert product cards
        document.querySelectorAll('.product-card [data-price-original]').forEach(el => {
            const original = parseFloat(el.dataset.priceOriginal);
            el.textContent = formatCurrency(original * rate, targetCurrency);
        });

        // Convert product detail pages
        document.querySelectorAll('.product-price[data-price-original]').forEach(el => {
            const original = parseFloat(el.dataset.priceOriginal);
            el.textContent = formatCurrency(original * rate, targetCurrency);
        });

        // Convert cart items
        document.querySelectorAll('.cart-item-price[data-price-original]').forEach(el => {
            const original = parseFloat(el.dataset.priceOriginal);
            el.textContent = formatCurrency(original * rate, targetCurrency);
        });
    }

    // Format currency with symbol
    function formatCurrency(amount, currency) {
        amount = parseFloat(amount.toFixed(2));
        switch(currency) {
            case 'USD': return `$${amount}`;
            case 'GBP': return `£${amount}`;
            case 'EUR': return `€${amount}`;
            case 'CAD': return `CA$${amount}`;
            case 'ETB': return `ETB ${amount}`;
            default: return `${currency} ${amount}`;
        }
    }

    // Initialize
    await fetchExchangeRates();
    const savedCurrency = localStorage.getItem('preferredCurrency') || 'USD';
    
    // Set the dropdown to saved currency
    if (locationDropdown) {
        const option = Array.from(locationDropdown.options).find(opt => opt.dataset.currency === savedCurrency);
        if (option) option.selected = true;
    }
    
    convertPrices(savedCurrency);

    // Handle changes from dropdown
    if (locationDropdown) {
        locationDropdown.addEventListener('change', function() {
            const currency = this.options[this.selectedIndex].dataset.currency;
            localStorage.setItem('preferredCurrency', currency);
            convertPrices(currency);
        });
    }

    // Handle changes from dropdown content clicks
    document.querySelectorAll('.location-selector .dropdown-content a').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const currency = this.dataset.currency;
            localStorage.setItem('preferredCurrency', currency);
            
            // Update dropdown selection
            if (locationDropdown) {
                const option = Array.from(locationDropdown.options).find(opt => opt.dataset.currency === currency);
                if (option) option.selected = true;
            }
            
            convertPrices(currency);
            
            // Close dropdown
            document.querySelector('.location-selector').classList.remove('show-dropdown');
        });
    });
}