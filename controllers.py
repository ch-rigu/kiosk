from py4web import action, request, abort, redirect, URL
from py4web.utils.form import Form, FormStyleBulma
from py4web.utils.grid import Grid, GridClassStyleBulma, Column
from yatl.helpers import A
from pydal.tools.tags import Tags
from py4web.utils.url_signer import URLSigner
from .common import (
    db,
    session,
    T,
    cache,
    auth,
    logger,
    authenticated,
    unauthenticated,
    flash,
    Field,
)
from pydal.validators import *
import uuid
import datetime

groups = Tags(db.auth_user)
url_signer = URLSigner(session)


@action("carts")
@action.uses(session, db, auth)
def carts():
    #print(dir(session.items()))
    return db(db.cart).select().as_list()


@action("delcart")
@action.uses(session, db, auth)
def delcart():
    #print(dir(session.items()))
    db(db.cart).delete()
    db(db.cart_summary).delete()
    return 'ok'


def validate_json_post(data, required_fields):
    
    print(data)
    
    if not data:
        return {'error': 'invalid request'}
    
    for field in required_fields:
        print(field)
        if field not in data.keys():
            return {'error': f'missing {field}'}
    
    return None  # Si no hay errores, retorna None


@action("index", method=['GET'])
@action.uses("index.html", session, db, auth, url_signer)
def index():

    return dict(
                get_products_url=URL("get_products", signer=url_signer),
                add_item_to_cart_url=URL("add_item_to_cart", signer=url_signer),
                cart_list_url = URL("cart_list", signer=url_signer),
                search_product_url = URL("search_product", signer=url_signer),
                delete_item_cart_url = URL("delete_item_cart", signer=url_signer),
                pay_now_url = URL("pay_now", signer=url_signer),
               )

@action("search_product", method=['POST'])
@action.uses(session, db, auth, url_signer.verify())
def search_product():
    if 'query' not in request.forms.keys():
        return dict(error='invalid request')

    print('serching...')

    value = request.forms.get('query')
    print(value)
    if value == '':
        items = db(db.product).select().as_list()
    else:
        items = db(db.product.name.contains(value)).select().as_list()
    for item in items:
        item['images'] = [item['image1'],
                           item['image2'],
                           item['image3']]
    print(items)
    return dict(items=items)

@action("get_products", method=['GET'])
@action.uses(session, db, auth, url_signer.verify())
def get_products():
    products = db(db.product).select().as_list()
    for product in products:
        product['images'] = [product['image1'],
                           product['image2'],
                           product['image3']]
    #print(items)
    return dict(products=products)

@action("cart_list", method=['POST'])
@action.uses(session, db, auth, url_signer.verify())
def cart_list():
    if not request.json:
        return dict(error='invalid request')
    if not request.json.get('get'):
        return dict(error='missing action')
    action = request.json.get('get')
    products = db(db.cart.cart_id == session['uuid']).select()
    product_cart = {}
    if action == 'all':
        
        for product in products:
            p = db(db.product.rand_id == product['product_id']).select(db.product.final_price,db.product.image1,db.product.name).first()
            #print(p)
            product['final_price'] = p['final_price']
            product['image'] = URL('static/media',p['image1'])
            product['name'] = p['name']
            product_cart[product['product_id']] = product

        return dict(products=product_cart)
    else:
        elements = 0
        for product in products:
            elements += product['quantity']
            
        return dict(products=elements)

    


@action("add_item_to_cart", method=['POST'])
@action.uses(session, db, auth, url_signer.verify())
def add_item_to_cart():
    if not request.forms.get('product_id'):
        print('missing product id')
        return dict(msg="nok", error='invalid item')
    product_id = request.forms.get('product_id')
    if len(product_id) != 36:
        return dict(msg="nok", error='invalid item id')

    #check if item exist and if there is stock
    product = db((db.product.rand_id == product_id) & (db.product.stock > 0)).select().first()
    product_stock = product['stock']
    if not product:
        return dict(msg="nok", error='invalid item or out of stock')

    #update cart
    if db(db.cart_summary.cart_id == session['uuid']).isempty():
        db.cart_summary.insert(cart_id=session['uuid'],
                               created_at=datetime.datetime.now())

    cart_items = db(db.cart.cart_id == session['uuid']).isempty()
    if cart_items:
        
        
        print(f"creating cart: {session['uuid']}- item: {product_id}")
        
        db.cart.insert(cart_id=session['uuid'],
                            product_id=product_id,
                            quantity=1
                            )

        print(f'inserted item: {product_id}')


    else:
        item = db((db.cart.cart_id == session['uuid']) & (db.cart.product_id == product_id)).select().first()
        
        
        if item:
            if item.quantity >= product_stock:
                return dict(error='no hay suficiente stock')
            
            item.update_record(quantity=item['quantity'] + 1)
        else:
            
            db.cart.insert(cart_id=session['uuid'],
                            product_id=product_id,
                            quantity=1
                            )
        
    return dict(msg="added", error='')

@action("shopping_cart")
@action.uses('shopping_cart.html',session, db, auth)
def shopping_cart():
    if not 'uuid' in session.keys():
        return 'missing session'

    return dict()


@action("delete_item_cart", method=['POST'])
@action.uses(session, db, auth, url_signer.verify())
def delete_item_cart():
    if not request.forms.get('product_id'):
        return 'missing product id'
    product_id = request.forms.get('product_id')
    if len(product_id) != 36:
        return 'invalid product id'
    if db(db.cart.cart_id == session['uuid']).isempty():
        return dict(error='cart not found')
    
    db((db.cart.cart_id == session['uuid']) & (db.cart.product_id == product_id)).delete()
    
    return dict(msg='deleted')


@action("pay_now", method=['GET'])
@action.uses('pay_now.html',session, db, auth, url_signer, url_signer.verify())
def pay_now():

    if not 'uuid' in session.keys():
        return 'missing session'
    
    cart_info = db(db.cart_summary.cart_id == session['uuid']).select().first()
    if not cart_info:

        cart_info = {
            'customer_name': '',
            'customer_lastname': '',
            'customer_email': '',
            'customer_rut': '',
            'customer_address': '',
            'customer_address_details': '',
            'customer_phone': '',
            'customer_region': '',
            'customer_comuna': '',
            'customer_message': '',
        }
        
    return dict(
                get_products_url=URL("get_products", signer=url_signer),
                cart_list_url = URL("cart_list", signer=url_signer),
                delete_item_cart_url = URL("delete_item_cart", signer=url_signer),
                cart_info_url = URL("cart_info_save", signer=url_signer),
                cart_info=cart_info,
                )


@action("cart_info_save", method=['POST'])
@action.uses(session, db, auth, url_signer, url_signer.verify())
def cart_info_save():
    
    required_fields = [
        'customer_name',
        'customer_lastname',
        'customer_email',
        'customer_rut',
        'customer_address',
        'customer_phone',
        'customer_region',
        'customer_comuna',

    ]
    error = validate_json_post(request.json, required_fields)
    if error:
        return error
    

    db.cart_summary.update_or_insert(db.cart_summary.cart_id == session['uuid'],
                                        customer_name=request.json['customer_name'],
                                        customer_lastname=request.json['customer_lastname'],
                                        customer_email=request.json['customer_email'],
                                        customer_rut=request.json['customer_rut'],
                                        customer_address=request.json['customer_address'],
                                        customer_address_details=request.json['customer_address_details'],
                                        customer_phone=request.json['customer_phone'],
                                        customer_region=request.json['customer_region'],
                                        customer_comuna=request.json['customer_comuna'],
                                        customer_message=request.json['customer_message'],

                                        created_at=datetime.datetime.now(),
                                        status='created'
    )

    return dict(msg='ok')

######## Admin functions ###########

@action("admin", method=["GET", "POST"])
@action.uses("admin.html", session, db, auth )
def admin(path=None):
    form_items = Form(db.product, _formname='form_items')
    form_groups = Form(db.groups, _formname='form_groups')
    items = db(db.product).select()
    groups = db(db.groups).select()
    total_cart = db(db.cart_summary).count()
 
    db.product.rand_id.default = str(uuid.uuid4())
    db.product.rand_id.readable = False
    db.product.rand_id.writable = False
    form_add_item = Form(db.product,
        formname='form_add_item',
        formstyle=FormStyleBulma,

    )

    if form_add_item.accepted:
        #item_id = str(uuid.uuid4())
        #form_obj = {}
        #if form_add_item.vars['image1']:
        #    print(form_add_item.vars['image1'])
        #    form_obj['image1'] = form_add_item.vars['image1']
        #if form_add_item.vars['image2']:
        #    form_obj['image2'] = form_add_item.vars['image2']
        #if form_add_item.vars['image3']:
        #    form_obj['image3'] = form_add_item.vars['image3']

        #form_obj['rand_id'] = item_id
        #form_obj['name'] = form_add_item.vars.get('name')
        #form_obj['description'] = form_add_item.vars.get('description')
        #form_obj['price'] = form_add_item.vars.get('price')

        #db.product.insert(**form_obj)
        redirect(URL('admin'))
    


    return dict(form_add_item=form_add_item, form_items=form_items, items=items,
                form_groups=form_groups, groups=groups,
               delete_item_url=URL("delete_item", signer=url_signer),
               total_cart=total_cart)

"""
@action("formm", method=["GET", "POST"])
@action.uses("form_edit.html", session, db) #url_signer.verify())
def edit_form():
    form = Form([
            Field('my_file', 'upload', uploadfolder='./apps/kiosk/uploads/', requires=IS_FILE()),
            Field('create_node', 'boolean', default=False,label='import even if host is down'),
        ]
    )
    if form.accepted:
        print('ok')
        #parsed_file = MyParser.parse_fromfile('./apps/kiosk/uploads/'+form.vars['my_file'])
        #os.remove("./apps/MYAPP/uploads/'+form.vars['my_file']")
        redirect(URL('formm'))
    return dict(form_edit=form)
"""

@action("edit_item/<id>", method=["GET", "POST"])
@action.uses("form_edit.html", session, db, auth) #url_signer.verify())
def edit_item(id=None):
    record = db(db.product.rand_id == id).select().first()
    print(record)
    if not record:
        redirect(URL('admin'))
    form_edit = Form(db.product, record.id,
                     _formname='form_edit_item',
                    formstyle=FormStyleBulma,
                    )
    if form_edit.accepted:
        redirect(URL('admin'))
    if form_edit.deleted:
        redirect(URL('admin'))
    return dict(form_edit=form_edit)


@action("cart_management", method=["GET"])
@action.uses('cart_management.html', session, db, auth)
def cart_management():
    #print(dir(session.items()))
    cart_list = db(db.cart_summary).select().as_list()
    print(cart_list)
    return dict(cart_list=cart_list)


@action("cart_inspect/<rand_id>", method=["GET"])
@action.uses('cart_inspect.html', session, db, auth)
def cart_inspect(rand_id=None):
    if not rand_id:
        return 'missing cart id'
    cart_info = db(db.cart_summary.cart_id == rand_id).select().first()
    cart_list = db(db.cart.cart_id == rand_id).select().as_list()
    
    if not cart_info:
        return 'invalid cart id'

    for item in cart_list:
        product = db(db.product.rand_id == item['product_id']).select().first()
        item['product_name'] = product['name']
        item['product_price'] = product['price']
        item['product_image'] = product['image1']
        item['product_discount'] = product['discount']
        item['product_final_price'] = product['final_price']


    return dict(cart_info=cart_info,cart_list=cart_list)








@action("delete_cart")
@action.uses(session, db, auth)#url_signer.verify())
def delete_cart(id=None):
    #if not request.forms.get('item_id'):
    #    return 'missing item id'
    #item_id = request.forms.get('item_id')
    #if len(item_id) != 36:
    #    return 'invalid item id'
    #db(db.product.id > 28).delete()

    db(db.cart.cart_id == id).delete()   
    db(db.cart_summary.cart_id == id).delete()   


    return 'ok'

@action("delete_item/<id>")
@action.uses(session, db, auth.user, )#url_signer.verify())
def delete_item(id=None):
    #if not request.forms.get('item_id'):
    #    return 'missing item id'
    #item_id = request.forms.get('item_id')
    #if len(item_id) != 36:
    #    return 'invalid item id'
    #db(db.product.id > 28).delete()
    redirect(URL('admin'))