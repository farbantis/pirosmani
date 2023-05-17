// const addToCartBtn = document.getElementsByClassName('update-cart');
// const cancelOrderItemBtn = document.getElementsByClassName('cart_cancel');
const addToCartBtn = document.querySelectorAll('.update-cart');
const cancelOrderItemBtn = document.querySelectorAll('.cart_cancel');

for (let i=0; i < cancelOrderItemBtn.length; i++) {
    cancelOrderItemBtn[i].addEventListener('click', function () {
        const productId = this.dataset.cart_cancel;
        const action = 'removeOrderItem';
        const neededDiv = cancelOrderItemBtn[i]
        updateCart(productId, action, neededDiv);
    })
}

for (let i=0; i < addToCartBtn.length; i++) {
    addToCartBtn[i].addEventListener('click', function () {
        // console.log(`dataset is ${this.dataset}`)
        const productId = this.dataset.product;
        const action = this.dataset.action;
        const neededDiv = addToCartBtn[i]
        updateCart(productId, action, neededDiv);
    })
}

function updateCart(productId, action, neededDiv) {
    let url = '/cafe/update-cart/';
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })
    .then((response) => {
        return response.json();
    })
          .then((data) => {
             const quantity = data.quantity;
             const currentItemValue = data.total_item;
             const currentOrderValue = data.grand_total;
             const total_pcs_ordered = data.pcs_ordered;
             // console.log('there response', quantity, total, grand_total_value)
             // console.log('pcs ordered ')
             updateCartPicture(total_pcs_ordered, currentOrderValue)
             updateFrontEnd(productId, quantity, currentItemValue, currentOrderValue, neededDiv, action)
  });
}


function updateCartPicture(total_pcs_ordered, currentOrderValue) {
    const cart_indicator = document.getElementsByClassName('cart_indicator')[0]
    const totalOrderFigure = document.getElementsByClassName('order_total_figure')[0]
    cart_indicator.innerText = total_pcs_ordered
    totalOrderFigure.innerText = currentOrderValue
}


function updateFrontEnd(productId, quantity, currentItemValue, currentOrderValue, neededDiv, action) {
    // document.getElementsByClassName('order_total_figure')[0].innerHTML = grand_total
    if (action ==='remove') {
        const amountWrapper = neededDiv.closest('.cart_quantity');
        const counter = amountWrapper.querySelector('[data-counter]');

        if (counter.innerText > '1') {
            counter.innerText = --counter.innerText;
            total(neededDiv, currentItemValue, currentOrderValue)
        }
        else {
            const childWrapper = neededDiv.closest('.cart');
            childWrapper.remove()
            total(neededDiv, currentItemValue, currentOrderValue)
        }
    }

    if (action === 'add') {
        const amountWrapper = neededDiv.closest('.cart_quantity');
        const counter = amountWrapper.querySelector('[data-counter]');
        counter.innerText = ++counter.innerText;
        total(neededDiv, currentItemValue, currentOrderValue)
    }

    if (action === 'removeOrderItem') {
        const toRemoveDiv = neededDiv.closest('.cart')
        toRemoveDiv.remove()
        total(neededDiv, currentItemValue, currentOrderValue)
        location.reload()
    }
}

function total(neededDiv, currentItemValue, currentOrderValue) {
        const cardWrapper = neededDiv.closest('.cart');
        const currentItemValueDiv = cardWrapper.querySelector('[data-item_total]');
        const currentOrderValueDiv = document.querySelector('[data-grand_total]')
        const promoDiscount = document.querySelector('.order_promo_figure').innerHTML
        const checkoutOrderValueDiv = document.querySelector('[data-total_checkout]')
        currentItemValueDiv.innerHTML = currentItemValue + " uah";
        currentOrderValueDiv.innerText = currentOrderValue + " uah";
        checkoutOrderValueDiv.innerHTML = (currentOrderValue - parseFloat(promoDiscount)).toFixed(2) + " uah"

}
