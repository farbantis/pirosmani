const addToCartBtn = document.getElementsByClassName('update-cart');
const cancelOrderItemBtn = document.getElementsByClassName('cart_cancel');


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
             const total = data.total_item;
             const grand_total = data.grand_total;
             // const pcs_ordered = data.pcs_ordered;
             // updateCartPicture(pcs_ordered)
             updateFrontEnd(productId, quantity, total, grand_total, neededDiv, action)
  });
}


function updateCartPicture(pcs_ordered) {
    const cart_indicator = document.getElementsByClassName('cart_indicator')[0]
    cart_indicator.innerText = pcs_ordered
}


function updateFrontEnd(productId, quantity, total_item, grand_total, neededDiv, action) {
    document.getElementsByClassName('order_total_figure')[0].innerHTML = grand_total
    if (action ==='remove') {
        const amountWrapper = neededDiv.closest('.cart_quantity');
        const counter = amountWrapper.querySelector('[data-counter]');

        if (counter.innerText > '1') {
            counter.innerText = --counter.innerText;
            total(neededDiv, total_item, grand_total)
        }
        else {
            const childWrapper = neededDiv.closest('.cart');
            childWrapper.remove()
        }
    }

    if (action === 'add') {
        const amountWrapper = neededDiv.closest('.cart_quantity');
        const counter = amountWrapper.querySelector('[data-counter]');
        counter.innerText = ++counter.innerText;
        total(neededDiv, total_item, grand_total)
    }

    if (action === 'removeOrderItem') {
        const toRemoveDiv = neededDiv.closest('.cart')
        toRemoveDiv.remove()

    }
}

function total(neededDiv, total_item, grand_total) {
        const cardWrapper = neededDiv.closest('.cart');
        const amountWrapper = cardWrapper.querySelector('[data-item_total]');
        const totalWrapper = document.querySelector('[data-grand_total]')
        amountWrapper.innerText = total_item + "грн";
        totalWrapper.innerText = grand_total + "грн";
}