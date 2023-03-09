const addToCartBtn = document.getElementsByClassName('update-cart');
const cancelOrderItemBtn = document.getElementsByClassName('cart_cancel');


for (let i=0; i < cancelOrderItemBtn.length; i++) {
    cancelOrderItemBtn[i].addEventListener('click', function () {
        //const toRemoveDiv = cancelOderItemDiv.closest('.cart')
        // toRemoveDiv.remove()
        // нам нужно удалить и объекты из Базы данных !! и во фронтэнде пересчитать сумму
        const productId = this.dataset.cart_cancel;
        const action = 'removeOrderItem';
        const neededDiv = cancelOrderItemBtn[i]
        // console.log(`action detected productId: ${productId}, action ${action}, neededDiv ${neededDiv}`)
        updateCart(productId, action, neededDiv);
    })
}

for (let i=0; i < addToCartBtn.length; i++) {
    addToCartBtn[i].addEventListener('click', function () {
        // console.log(`dataset is ${this.dataset}`)
        const productId = this.dataset.product;
        const action = this.dataset.action;
        const neededDiv = addToCartBtn[i]
        // console.log(`action detected productId: ${productId}, action ${action}`)
        // console.log(neededDiv)
        updateCart(productId, action, neededDiv);
    })
}

function updateCart(productId, action, neededDiv) {
    console.log('starting action update')
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
             // console.log(`quantity: ${quantity}, total: ${total}, grand_total: ${grand_total}, productID ${productId}`)
             // return data
             updateFrontEnd(productId, quantity, total, grand_total, neededDiv, action)
  });
    // console.log(`quantity: ${quantity}, total: ${total}, grand_total: ${grand_total}`)
}

function updateFrontEnd(productId, quantity, total_item, grand_total, neededDiv, action) {
    // console.log('INSIDE updatefrontend');
    // console.log(neededDiv);

    document.getElementsByClassName(' order_total_figure')[0].innerHTML = grand_total

    if (action ==='remove') {
        // console.log(neededDiv.closest('.cart_quantity'))
        const amountWrapper = neededDiv.closest('.cart_quantity');
        const counter = amountWrapper.querySelector('[data-counter]');
        // console.log(counter)

        if (counter.innerText > '1') {
            // отнимаем единицу
            counter.innerText = --counter.innerText;
            total(neededDiv, total_item, grand_total)
        }
        else {
            // удаляем елемент
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