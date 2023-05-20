const addToCartBtn1 = document.getElementsByClassName('update-cart');

for (let i=0; i < addToCartBtn1.length; i++) {
    addToCartBtn1[i].addEventListener('click', function () {
        const productId = this.dataset.product;
        const action = 'add';
        updateScreen(productId, action);
    })
}

function updateScreen(productId, action) {
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
             const pcs_ordered = data.pcs_ordered;
             const grand_total = data.grand_total;
             updateCartPicture(pcs_ordered, grand_total)
  });
}

function updateCartPicture(pcs_ordered, grand_total) {
    const cart_indicator = document.getElementsByClassName('cart_indicator')[0]
    const totalOrderFigure = document.getElementsByClassName('order_total_figure')[0]
    cart_indicator.innerText = pcs_ordered
    totalOrderFigure.innerHTML = grand_total
}
