
const vue_app = Vue.createApp({
  data() {
      return {
        show_payment: false,
        empty_value: {'nombre': false, 'apellido': false, 'rut': false, 'email': false, 'telefono': false, 'direccion': false, 'region': false, 'comuna': false},
        products: [],
          shippingDetails: {
              customer_name: '[[=cart_info['customer_name'] ]]',
              customer_lastname: '[[=cart_info['customer_lastname'] ]]',
              customer_rut: '[[=cart_info['customer_rut'] ]]',
              customer_email: '[[=cart_info['customer_email'] ]]',
              customer_phone: '[[=cart_info['customer_phone'] ]]',
              customer_address:  '[[=cart_info['customer_address'] ]]',
              customer_address_details: '[[=cart_info['customer_address_details'] ]]',
              customer_region: '[[=cart_info['customer_region'] ]]',
              customer_comuna: '[[=cart_info['customer_comuna'] ]]',
              customer_message: '[[=cart_info['customer_message'] ]]',
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
      
      if (this.shippingDetails.customer_name.length < 3){
        this.empty_value.nombre = true
        console.log('nombre vacio')
        return
      }
      if (this.shippingDetails.customer_lastname.length < 3){
        this.empty_value.apellido = true
        console.log('apellido vacio')
        return

      }
      if (this.shippingDetails.customer_rut.length < 9 ) {
        this.empty_value.rut = true
        console.log('rut vacio')
        return
      }
      if (!this.shippingDetails.customer_rut.includes('-')){
        this.empty_value.rut = true
        console.log('rut sin guion')
        return
      }
      if (this.shippingDetails.customer_email === '' || !this.shippingDetails.customer_email.includes('@')){
        this.empty_value.email = true
        console.log('email vacio')
        return
      }
      if (this.shippingDetails.customer_phone === '' || this.shippingDetails.customer_phone.length < 9){
        this.empty_value.phone = true
        console.log('telefono vacio')
        return
      }
      if (this.shippingDetails.customer_address === ''){
        this.empty_value.direccion = true
        console.log('direccion vacioo')
        return
      }
      if (this.shippingDetails.customer_region === ''){
        this.empty_value.region = true
        console.log('region vacio')
        return 
      }
      if (this.shippingDetails.customer_comuna === ''){
        this.empty_value.comuna = true
        console.log('comuna vacio')
        return
      }
      for (const [key, value] of Object.entries(this.empty_value)) {
        this.empty_value[key] = false
      }
      
      axios.post(cart_info_url, {
        'customer_name': this.shippingDetails.customer_name,
        'customer_lastname': this.shippingDetails.customer_lastname,
        'customer_rut': this.shippingDetails.customer_rut,
        'customer_email': this.shippingDetails.customer_email,
        'customer_phone': this.shippingDetails.customer_phone,
        'customer_address': this.shippingDetails.customer_address,
        'customer_address_details': this.shippingDetails.customer_address_details,
        'customer_region': this.shippingDetails.customer_region,
        'customer_comuna': this.shippingDetails.customer_comuna,
        'customer_message': this.shippingDetails.customer_message,

      })
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