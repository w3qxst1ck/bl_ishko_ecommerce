// csrf token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


// add to wish list
var wishButtons = document.getElementsByClassName('wishlist-status');

for(var i = 0; i < wishButtons.length; i++){
  wishButtons[i].addEventListener('click', function(e){
  e.preventDefault();

  var productId = this.dataset.product;
  var action = this.dataset.action;
  var url = this.dataset.domain;
  if (action == 'add-item'){
      this.style.background = '#af5875'; 
      this.style.color = '#fff';
      this.dataset.action = 'delete-item'
  }else{
      this.style.removeProperty('background'); 
      this.style.removeProperty('color');
      this.dataset.action = 'add-item';
  }

  changeWishStatus(productId, action, url)
  })
};


function changeWishStatus (productId, action, url){
  fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'aplication/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({'productId': productId, 'action': action})
  })
  
  .then((response) => {
      return response.json()
  })

  .then((data) => {
      console.log('data:', data)
  })
};


// add to cart in detail
var cartButton = document.getElementById('ajax-add-to-cart');

cartButton.addEventListener('click', function(e){
    e.preventDefault();

    var itemCount = document.getElementById('quantity_input').value;
    if (itemCount == '0') {
      console.log('item count must be greater than 0');
    } else {
      var itemSize = document.getElementById('size_input').value;
      var productId = this.dataset.product;
      var url = this.dataset.domain;

      addToCart(url, productId, itemSize, itemCount);
      var hiddenP = document.getElementById('ajax-add-to-cart-p');
      hiddenP.removeAttribute('hidden');

      // chech span is exist
      if (document.getElementsByClassName('numb').length) {
        // change span value
        var currentItemCount = document.getElementsByClassName('numb')[0].innerText;
        newItemCount = Number(itemCount) + Number(currentItemCount);
        document.getElementsByClassName('numb')[0].innerHTML = newItemCount;

      } else {
        // create span element if ajax
        var cartSpan = document.createElement("span");
        cartSpan.classList.add('numb');

        // add span with new item count
        cartSpan.textContent = `${itemCount}`;
        var cartUl = document.getElementById("cart-dropdown-menu-ul");
        var parentEl = cartUl.parentNode;
        parentEl.insertBefore(cartSpan, cartUl);
      };

      // delete ul dropdown
      var cartUl = document.getElementById("cart-dropdown-menu-ul");
      cartUl.parentNode.removeChild(cartUl);
    };
});

function addToCart(url, productId, itemSize, itemCount){
  fetch(url, {
          method: 'POST',
          headers: {
          'Content-Type': 'aplication/json',
          'X-CSRFToken': csrftoken,
        },
      body: JSON.stringify({'productId': productId, 'itemSize': itemSize, 'itemCount': itemCount})
  })

    .then((response) => {
      return response.json()
  })

  .then((data) => {
      console.log('data:', data)
  })
}



