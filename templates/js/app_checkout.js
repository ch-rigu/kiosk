
const vue_app = Vue.createApp({
  data() {
      return {
        show_payment: false,
        empty_value: {'nombre': false, 'apellido': false, 'rut': false, 'email': false, 'telefono': false, 'direccion': false, 'region': false, 'comuna': false},
        products: [],
          shippingDetails: {
              name: '',
              lastName: '',
              rut: '',
              email: '',
              phone: '',
              address: '',
              addressDetail: '',
              region: '',
              comuna: '',
              details: ''
          },
        shopping_cart: [],
        shopping_total: 0,
        loadingSearch: false,
        searchValue: '',
      };
  },
  computed: {
      totalPrice() {
          return this.cartItems.reduce((total, item) => total + (item.price * item.quantity), 0);
      }
  },
  methods: {
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
            this.cart_listing('all')
              
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
    validaForm(){
      
      if (this.shippingDetails.name.length < 3){
        this.empty_value.nombre = true
        console.log('nombre vacio')
        return
      }
      if (this.shippingDetails.lastName.length < 3){
        this.empty_value.apellido = true
        console.log('apellido vacio')
        return

      }
      if (this.shippingDetails.rut.length < 9 ) {
        this.empty_value.rut = true
        console.log('rut vacio')
        return
      }
      if (!this.shippingDetails.rut.includes('-')){
        this.empty_value.rut = true
        console.log('rut sin guion')
        return
      }
      if (this.shippingDetails.email === '' || !this.shippingDetails.email.includes('@')){
        this.empty_value.email = true
        console.log('email vacio')
        return
      }
      if (this.shippingDetails.phone === '' || this.shippingDetails.phone.length < 9){
        this.empty_value.phone = true
        console.log('telefono vacio')
        return
      }
      if (this.shippingDetails.direccion === ''){
        this.empty_value.direccion = true
        console.log('direccion vacioo')
        return
      }
      if (this.shippingDetails.region === ''){
        this.empty_value.region = true
        console.log('region vacio')
        return 
      }
      if (this.shippingDetails.comuna === ''){
        this.empty_value.comuna = true
        console.log('comuna vacio')
        return
      }
      for (const [key, value] of Object.entries(this.empty_value)) {
        this.empty_value[key] = false
      }
      this.show_payment = true
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
      cart_listing(action){
        if (window.location.pathname === '/kiosk/pay_now') {
          this.shopping_total = 0
        }
        
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
  },
  mounted() {
    this.cart_listing('count');
    this.cart_listing('all');
  //this.changeSize();
  //this.renderHorizontalBarChart();
  
},
});

vue_app.mount("#app");