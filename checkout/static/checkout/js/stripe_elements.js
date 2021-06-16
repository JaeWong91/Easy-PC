/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment
    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

var stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);     /* get public key and client secret from template/views.py */
var client_secret = $('#id_client_secret').text().slice(1, -1);             /* slice off first and last characters which are the quotation marks */
var stripe = Stripe(stripe_public_key);                                     /* create variable of stripe using our public key */
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