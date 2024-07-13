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


@action("index")
@action.uses("index.html", session, db, auth, url_signer)
def index():

    return dict(
                get_items_url=URL("get_items", signer=url_signer),
               )


@action("get_items")
@action.uses(session, db, url_signer.verify())
def get_items():
    items = db(db.item).select().as_list()
    return dict(items=items)


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

    return dict(form_add_item=form_add_item, form_items=form_items, items=items, form_groups=form_groups, groups=groups)



