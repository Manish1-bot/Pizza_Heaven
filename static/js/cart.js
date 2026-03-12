// Cart specific functionalities

document.addEventListener('DOMContentLoaded', function() {
    // Update quantities via AJAX or Form submission
    const qtyInputs = document.querySelectorAll('.cart-qty-input');
    
    qtyInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (this.value < 1) this.value = 1;
            // The form will be submitted automatically when using the plus/minus buttons
        });
    });
});
