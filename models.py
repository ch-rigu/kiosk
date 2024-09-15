"""
This file defines the database models
"""
from py4web import URL
from .common import db, Field
from pydal.validators import *
from .settings import UPLOAD_FOLDER, UPLOAD_FOLDER_STATIC

### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later
#

db.define_table('groups',
                Field('group_id', 'string', requires=IS_NOT_EMPTY()),
                Field('name', 'string', requires=IS_NOT_EMPTY()),
                Field('description', 'string', requires=IS_NOT_EMPTY()),
               )


db.define_table('product',
                Field('rand_id', 'string', requires=IS_NOT_EMPTY()),
                Field('name', 'string', requires=IS_NOT_EMPTY()),
                Field('description', 'text', default=''),
                
                Field('stock', 'integer', requires=IS_NOT_EMPTY()),
                Field('image1', 'upload', uploadfolder='./apps/kiosk/static/media',download_url=lambda image1: URL('static/media', image1),
                      requires=IS_EMPTY_OR(IS_FILE(extension=['png', 'jpg', 'jpeg']))),
                Field('image2', 'upload', uploadfolder='./apps/kiosk/static/media', download_url=lambda image2: URL('static/media', image2),
                      requires=IS_EMPTY_OR(IS_FILE(extension=['png', 'jpeg', 'jpg']))),
                Field('image3', 'upload', uploadfolder='./apps/kiosk/static/media', download_url=lambda image3: URL('static/media', image3),
                      requires=IS_EMPTY_OR(IS_FILE(extension=['png', 'jpeg', 'jpg']))),
                Field('tags', 'list:string'),
                Field('score', 'list:string', default='[]'),
                Field('price', 'integer',  requires=IS_NOT_EMPTY()),
                Field('discount', 'integer', requires=IS_NOT_EMPTY()),
               Field('final_price', compute=lambda r: int(r.price) - ((int(r.price) * int(r.discount)) / 100), writable=False)
               )



# db.item.final_price.writable=False


db.define_table('cart_summary',
                Field('cart_id', 'string', requires=IS_NOT_EMPTY()),
                Field('customer_name', 'string', default='', requires=IS_NOT_EMPTY()),
                Field('customer_lastname', 'string', default='', requires=IS_NOT_EMPTY()),
                Field('customer_email', 'string', default='', requires=IS_NOT_EMPTY()),
                Field('customer_rut', 'string', default='', requires=IS_NOT_EMPTY()),
                Field('customer_address', 'string', default='', requires=IS_NOT_EMPTY()),
                Field('customer_address_details', 'string', default='', requires=IS_NOT_EMPTY()),
                Field('customer_phone', 'string', default='', requires=IS_NOT_EMPTY()),
                Field('customer_region', 'string', default='', requires=IS_NOT_EMPTY()),
                Field('customer_comuna', 'string', default='', requires=IS_NOT_EMPTY()),
                Field('customer_message', 'string', default='', requires=IS_NOT_EMPTY()),
                Field('created_at', 'datetime', requires=IS_NOT_EMPTY()),
                Field('status', 'string', requires=IS_NOT_EMPTY()),

)


db.define_table('cart',
                Field('cart_id', 'string', requires=IS_NOT_EMPTY()),
                Field('product_id', 'string', requires=IS_IN_DB(db, 'product.rand_id', '%(name)s')),
                Field('quantity', 'integer', requires=IS_NOT_EMPTY()),
                

               )


db.commit()

#
