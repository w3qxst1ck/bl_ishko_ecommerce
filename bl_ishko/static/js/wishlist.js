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

