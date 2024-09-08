
function focusIn(id) {
  //console.log("Focus in:", id);
  // Obtener todos los elementos con el mismo ID
  actual_quote_id = id.replace("_tag","")
  const elemento = document.getElementById(id);
  //console.log(elemento)
  // Aplicar el resaltado a cada elemento

  // Aplicar un pequeño zoom
  if ( elemento !== null) {
    elemento.classList.add('highlight-aura');
    elemento.style.box_shadow = '0 0 10px rgba(0, 0, 0, 0.5);';
    elemento.style.transition = 'transform 0.2s ease-in-out';
    elemento.style.transform = 'scale(1.1)'; // Puedes ajustar el valor según tus preferencias
    elemento.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
}
function focusOut(id) {
  // Obtener todos los elementos con el mismo ID
  const elemento = document.getElementById(id);
  if ( elemento !== null) {
    elemento.classList.remove('highlight-aura');
    elemento.style.transform = 'scale(1)';
  }

}

document.addEventListener('DOMContentLoaded', () => {
  // Functions to open and close a modal
  function openModal($el) {
    $el.classList.add('is-active');
  }

  function closeModal($el) {
    $el.classList.remove('is-active');
  }

  function closeAllModals() {
    (document.querySelectorAll('.modal') || []).forEach(($modal) => {
      closeModal($modal);
    });
  }

  // Add a click event on buttons to open a specific modal
  (document.querySelectorAll('.js-modal-trigger') || []).forEach(($trigger) => {
    const modal = $trigger.dataset.target;
    const $target = document.getElementById(modal);

    $trigger.addEventListener('click', () => {
      openModal($target);
    });
  });

  // Add a click event on various child elements to close the parent modal
  (document.querySelectorAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button') || []).forEach(($close) => {
    const $target = $close.closest('.modal');

    $close.addEventListener('click', () => {
      closeModal($target);
    });
  });


  // Add a keyboard event to close all modals
  document.addEventListener('keydown', (event) => {
    if (event.code === 'Escape') {
      closeAllModals();
    }
  });
  });






const vue_app = Vue.createApp({
  data() {
    return {
      pay_now_url: pay_now_url,
      cart_count: 0,
      searchValue:'',
      shippingDetails: {
        name: '',
        lastName: '',
        address: '',
        city: '',
        details: ''
    },
      colors: [['primary','is-primary'],
               ['link','is-link'],
               ['info','is-info'],
               ['success','is-success'],
               ['warning','is-warning'],
               ['danger','is-danger'],
               ['light','is-light'],
               ['dark','is-dark'],
               ['primary','is-primary is-light'],
               ['link','is-link is-light'],
               ['info','is-info is-light'],
               ['success','is-success is-light'],
               ['warning','is-warning is-light'],
               ['danger','is-danger is-light'],
               ['light','is-light is-light'],
              ],
      //products = [],
      products: [{'name': 'loading products', 'price': 0, 'tags': ['',''], 'id':'xxx-xxx-kitsune','description':'loading products'},
             ],
      shopping_cart: [{'rand_id':'','name': '', 'quantity': '', 'price':'', 'image':''}],
      shopping_total: 0,
      show_product: {'name': 'loading products', 'price': 0, 'tags': ['',''], 'id':'xxx-xxx-kitsune','description':'loading products'},
      currentImageIndex: 0,
      loadingSearch: false,
      product: {
          name: 'Producto de Ejemplo',
          description: 'Esta es una descripción del producto. Ofrece características únicas y beneficios.',
          images: [
              '',
              '',
              ''
          ]
      }
    }
  },
  computed: {
        chunkedproducts() {
            return this.chunkArray(this.products, 3);
        }
    },
    methods: {
      handleCheckout() {
        // Handle checkout logic here
        console.log('Order confirmed', this.shippingDetails);
    },
    payWithBankTransfer() {
        // Payment logic for bank transfer
        console.log('Paying with Bank Transfer');
    },
    payWithWeepy() {
        // Payment logic for Weepy
        console.log('Paying with Weepy');
    },
        searchProduct(product) {
            this.loadingSearch = true
            axios.post(search_product_url, {
            'query':this.searchValue,
            })
            .then(response => {
              this.loadingSearch = false
              this.products = response.data.products;
              console.log(this.products)
          })
          .catch(error => {
              this.loadingSearch = false
              alert(error)
            })

        },
      nextImage() {
        if (this.currentImageIndex < this.product.images.length - 1) {
            this.currentImageIndex++;
        }
        console.log(this.currentImageIndex)
    },
    prevImage() {
        if (this.currentImageIndex > 0) {
            this.currentImageIndex--;
        }
    },
      productModal(position) {
        console.log(position)
        this.product = this.products[position];
        this.currentImageIndex = 0; // Reiniciar el índice de la imagen al abrir el modal
        const modal = document.getElementById("modal-product");
        modal.classList.add('is-active'); // Abrir el modal
    },
    closeModal() {
        const modal = document.getElementById("modal-product");
        modal.classList.remove('is-active'); // Cerrar el modal
    },
      getproducts() {
          axios.get(get_products_url)
          .then(response => {
              this.products = response.data.products;
              console.log(this.products)
          })
          .catch(error => {
              alert(error)
              console.error(error);
          });
      },
      chunkArray(array, chunkSize) {
          const result = [];
          for (let i = 0; i < array.length; i += chunkSize) {
              result.push(array.slice(i, i + chunkSize));
          }
          return result;
      },
      add_to_cart(product_id){
          axios.post(add_item_to_cart_url,{
                  'product_id':product_id,
                  })
          .then(response => {
              if (response.data.msg ==='added') {
                  //this.cart_products.push(product_id)
                  //alert(this.cart_products)
                  this.cart_listing('count')
                  //document.getElementById("cart_counter").innerText = this.cart_count
              }
              else {
                  alert(response.data.error)
              }
          })
          .catch(error => {
              alert(error);
              console.log(error)}
                )
        },
        cart_listing(action){
            axios.post(cart_list_url, {
            'get':action})
            .then(response => {
                if (action === 'all') {
                    this.shopping_cart =  response.data.products
                    for (const [key, value] of Object.entries(this.shopping_cart)) {
                      this.shopping_total += parseInt(value.final_price)
                    }
                 
                } else {
                    //alert(response.data.products)
                    //this.cart_count = response.data.products
                    document.getElementById("cart_counter").innerText = response.data.products
                }
                
            })
        },
        
        toCurrency(value) {
          if (typeof value !== "number") {
            return value;
          }
          const formatter = new Intl.NumberFormat('es-CL', {
            style: 'currency',
            currency: 'CLP'
          });
          return formatter.format(value);
        },
        deleteproductCart(product_id){
          console.log(product_id)
          console.log(this.shopping_cart)
          
          axios.post(delete_item_cart_url,{
                  'product_id':product_id,
                  })
          .then(response => {
              if (response.data.msg ==='deleted') {
                this.shopping_total -= parseInt(this.shopping_cart[product_id].final_price)
                delete this.shopping_cart[product_id]
                  //alert(this.cart_products)
                this.cart_listing('count')
                  
                  //document.getElementById("cart_counter").innerText = this.cart_count
              }
              else {
                  alert(response.data.msg)
              }
          })
          .catch(error => {
              alert(error);
              console.log(error)}
                )
        },
    },

beforeMount() {
  this.getproducts();



},

mounted() {
    this.cart_listing('count');
  //this.changeSize();
  //this.renderHorizontalBarChart();
  
},

});
//vue_app.config.compilerOptions = {
//  isCustomElement: tag => tag === 'marked'
//};
vue_app.mount("#app");
