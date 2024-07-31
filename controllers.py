from py4web import action, request, abort, redirect, URL
from py4web.utils.form import Form, FormStyleBulma
from py4web.utils.grid import Grid, GridClassStyleBulma
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
    return 'ok'

@action("index")
@action.uses("index.html", session, db, auth, url_signer)
def index():
    #print(dir(session.items()))
    try:
        print(db(db.cart.cart_id == session['uuid']).select())
        if not db(db.cart.cart_id == session['uuid']).select().first():
            db.cart.insert(
                        cart_id=session['uuid'],
                        item_list=[])
    except:
        pass
    #else:
    #    db(db.cart.cart_id == session['uuid']).update(item_list=[])
    return dict(
                get_items_url=URL("get_items", signer=url_signer),
                add_item_to_cart_url=URL("add_item_to_cart", signer=url_signer),
                cart_list_url = URL("cart_list", signer=url_signer),
               )


@action("get_items")
@action.uses(session, db, auth, url_signer.verify())
def get_items():
    items = db(db.item).select().as_list()
    return dict(items=items)

@action("cart_list")
@action.uses(session, db, auth, url_signer.verify())
def cart_list():
    if request.forms.get('get') == 'all':
        items = db(db.cart.cart_id == session['uuid']).select().first()
        cart_items = []
        for item in items['item_list']:
            i = db(db.item.rand_id == item).select().first()
            cart_items.append({'id':i.id, 'name': i.name, 'price':i.price})
        return dict(items=cart_items)
    else:
        cart = db(db.cart.cart_id == session['uuid']).select().first()


        if cart['item_list'] == None:
            cart.update_record(item_list=[])
            cart.update(item_list=[])
        print(f'cart items:{cart} ')


        return dict(items=len(cart['item_list']))


@action("add_item_to_cart")
@action.uses(session, db, auth, url_signer.verify())
def add_item_to_cart():
    if not request.forms.get('item_id'):
        print('missing item id')
        return 'missing item id'
    item_id = request.forms.get('item_id')
    if len(item_id) != 36:
        print('invalid item id')
        return 'invalid item id'

    #check if item exist and if there is stock
    item = db((db.item.rand_id == item_id) & (db.item.stock > 0)).select().first()

    if item:
        #print('updating cart')
        #update cart
        cart_items = db(db.cart.cart_id == session['uuid']).select().first()
        print(cart_items)
        if cart_items['item_list'] == None:
            print(f"inserting in cart: {session['uuid']}- item: {item_id}")
            cart_items.update_record(item_list=[item_id])
            print(f'inserted item: {item_id}')

        else:
            print(cart_items['item_list'], item_id)
            updated_items = cart_items['item_list'] + [item_id]
            print("updated ite")
            print(updated_items)
            cart_items.update_record(item_list=updated_items)

        return dict(msg="added")
    else:
        print('invalid item or out of stock')
        return 'invalid item or out of stock'

@action("shopping_cart")
@action.uses('shopping_cart.html',session, db, auth)
def shopping_cart():
    if not 'uuid' in session.keys():
        return 'missing session'

    return dict()



######## Admin functions ###########

@action("admin", method=["GET", "POST"])
@action('admin/<path:path>', method=['POST', 'GET'])
@action.uses("admin.html", session, db, auth.user, )
def admin(path=None):
    form_items = Form(db.item, _formname='form_items')
    form_groups = Form(db.groups, _formname='form_groups')
    items = db(db.item).select()
    groups = db(db.groups).select()

    grid = Grid(path,
            formstyle=FormStyleBulma, # FormStyleDefault or FormStyleBulma
            grid_class_style=GridClassStyleBulma, # GridClassStyle or GridClassStyleBulma
            query=(db.item.id > 0),
            orderby=[db.item.name],
            search_queries=[['Search by Name', lambda val: db.item.name.contains(val)]])
    db.item.rand_id.default = str(uuid.uuid4())
    db.item.rand_id.readable = False
    db.item.rand_id.writable = False
    form_add_item = Form(db.item,
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

        #db.item.insert(**form_obj)
        redirect(URL('admin'))

    return dict(form_add_item=form_add_item, form_items=form_items, items=items,
                form_groups=form_groups, groups=groups,
               delete_item_url=URL("delete_item", signer=url_signer),)

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
@action.uses("form_edit.html", session, db, auth.user) #url_signer.verify())
def edit_item(id=None):
    record = db(db.item.rand_id == id).select().first()
    print(record)
    if not record:
        redirect(URL('admin'))
    form_edit = Form(db.item, record.id,
                     _formname='form_edit_item',
                    formstyle=FormStyleBulma,
                    )
    if form_edit.accepted:
        redirect(URL('admin'))
    if form_edit.deleted:
        redirect(URL('admin'))
    return dict(form_edit=form_edit)

@action("delete_item/<id>")
@action.uses(session, db, auth.user, )#url_signer.verify())
def delete_item(id=None):
    #if not request.forms.get('item_id'):
    #    return 'missing item id'
    #item_id = request.forms.get('item_id')
    #if len(item_id) != 36:
    #    return 'invalid item id'
    #db(db.item.id > 28).delete()
    redirect(URL('admin'))