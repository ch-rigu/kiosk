
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








const vue_app = Vue.createApp({
  data() {
    return {

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
      //items = [],
      items: [{'name': 'error loading products', 'price': 0, 'tags': ['',''], 'id':'xxx-xxx-kitsune','description':'error loading products'},
             ],

    }
  },
  methods: {
    getItems(){
        //prompt('',get_items_url)
      //prompt(get_items_url,get_items_url)
      axios.get(get_items_url)
      .then(response => {
        //alert(response.data.items)
        //console.log(response.data.content.content);
        this.items = response.data.items
      })
    },


},

beforeMount() {
  this.getItems();

},

mounted() {
  //this.changeSize();
  //this.renderHorizontalBarChart();
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
        this.unselectQuotes();
        document.getElementById('search_codes').style.display = 'none';
        closeAllModals();
      }
    });
    });
},

});
//vue_app.config.compilerOptions = {
//  isCustomElement: tag => tag === 'marked'
//};
vue_app.mount("#app");
