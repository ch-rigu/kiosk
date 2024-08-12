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


db.define_table('item',
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
                Field('score', 'list:integer', default='[]'),
                Field('price', 'integer', default=0, requires=IS_NOT_EMPTY()),
                Field('discount', 'integer', default=0, requires=IS_NOT_EMPTY()),
                Field('final_price', compute=lambda r: r.price - (r.price * r.discount) / 100)
               )

# db.item.final_price.writable=False

db.define_table('cart',
                Field('cart_id', 'string', requires=IS_NOT_EMPTY()),
                Field('item_list', 'list:string', default='[]', requires=IS_NOT_EMPTY()),

               )



db.commit()

#
