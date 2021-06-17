/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment
    
    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);     /* get public key and client secret from template/views.py */
var clientSecret = $('#id_client_secret').text().slice(1, -1);             /* slice off first and last characters which are the quotation marks */
var stripe = Stripe(stripePublicKey);                                     /* create variable of stripe using our public key */
var elements = stripe.elements();                                           
var style = {                                                               
    base: {
        color: '#220038',                                                   /* change colour to purple */
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',                                                   /* change colour to match bootstrap's danger class */
        iconColor: '#dc3545'
    }
};
var card = elements.create('card', {style: style});                         /* use that to create an instance of stripe elements */
card.mount('#card-element');                                                /* mount the card element to the dic we created */

// Handle realtime validation errors on the card element
card.addEventListener('change', function (event) {                          // add a listener on the card element for the change event and every time it changes we;ll check to see if there are any errors
    var errorDiv = document.getElementById('card-errors');
    if(event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

//Handle form submit
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    card.update({'disabled': true});        // disable both card element and submit button to prevent multiple submissions
    $('#submit-button').attr('disabled', true)
    stripe.confirmCardPayment(clientSecret, {   
        payment_method: {
            card: card,           
        }
    }).then(function(result) {
        if (result.error) {
            var errorDiv = document.getElementById('card-errors');
            var html = `
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            $(errorDiv).html(html);
            card.update({'disabled': false});        // re-enable the buttons when there is an error to allow user to fix it
            $('#submit-button').attr('disabled', false)
        } else {
            // The payment has been processed!
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});