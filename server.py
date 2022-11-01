from flask import Flask, request, abort
import json
from config import me, hello, db
from mock_data import catalog
from bson import ObjectId

app = Flask('server')


@app.get('/')
def home():
    return 'Hello from Flask!'


@app.get('/test')
def test():
    return 'This is a test!'


@app.get('/about')
def about():
    return 'Jonathan Mojica'

# ---------------------
#     API Endpoints
#     /api/v1 JSONS
# ---------------------


@app.get('/api/version')
def version():
    v = {
        'version': '1.0.0',
        'build': 42,
        'name': 'sloth',
        'developer': me
    }
    hello()
    # todo: return as json
    return json.dumps(v)

# get /api/catalog


def fix_id(obj):
    obj['_id'] = str(obj['_id'])
    return obj


def get_catalog_products(conditions={}):
    products = db.products.find(conditions)
    products = [fix_id(p) for p in products]
    return products


@app.get('/api/catalog')
def get_catalog():
    return json.dumps(get_catalog_products())


@app.post('/api/catalog')
def add_product():
    # get the data from the request
    product = request.get_json()

    # should be a title
    # the title should have at least 5 chars

    # should be a category

    # should be a price
    # the price should be a number (int or float)
    # the number should be greater than 0

    if product is None:
        abort(400, 'No product required')

    if not product.get('title') or len(product['title']) < 5:
        abort(400, 'Title is required and must be at least 5 characters long')

    if not product.get('category'):
        abort(400, 'Category is required')

    if not product.get('price') or product['price'] <= 0:
        abort(400, 'Price is required and must be greater than 0')

    if product.get('price') and not isinstance(product['price'], (int, float)):
        abort(400, 'Price must be a number')

    # add the product to the database
    product['category'] = product['category'].lower()

    db.products.insert_one(product)

    product['_id'] = str(product['_id'])

    return json.dumps(product)

# put /api/catalog


@app.put('/api/catalog')
def update_product():
    # get the data from the request
    product = request.get_json()

    if product is None:
        abort(400, 'No product to update')

    id = product.pop('_id')

    # update the product in the database
    product['category'] = product['category'].lower()

    res = db.products.update_one({'_id': ObjectId(id)}, {'$set': product})

    return json.dumps("Product updated")

# delete /api/catalog


@app.delete('/api/catalog/<id>')
def delete_product(id):
    # delete the product from the database
    db.products.delete_one({'_id': ObjectId(id)})

    return json.dumps("Product deleted")

# get /api/catalog/details/<id>


@app.get('/api/catalog/details/<id>')
def get_product_details(id):
    product = db.products.find_one({'_id': ObjectId(id)})
    product = fix_id(product)
    if product is None:
        abort(404, 'Product not found')

    return json.dumps(product)

# get /api/products/count
# return the number of products in the catalog


@app.get('/api/catalog/count')
def get_products_count():
    total_products = db.products.count_documents({})
    return json.dumps({'total_products': total_products})

# get /api/products/total
# return the sum of all the prices of the products in the catalog


@app.get('/api/catalog/total')
def get_products_total():
    total = 0
    for product in get_catalog_products():
        total += product['price']
    return json.dumps({'total': total})

# get /api/products/categories
# return all the products that below to the received category


@app.get('/api/catalog/categories/<category>')
def get_products_by_category(category):
    products = get_catalog_products({'category': category})

    return json.dumps(products)

# get /api/catalog/lower/<amount>
# return all the products that are below the received amount


@app.get('/api/catalog/lower/<amount>')
def get_products_lower_than(amount):
    products = get_catalog_products({'price': {'$lt': float(amount)}})

    return json.dumps(products)

# create an endpoint that allow us retrieve product with prices greater or equal than a given amount


@app.get('/api/catalog/greater/<amount>')
def get_products_greater_than(amount):
    products = get_catalog_products({'price': {'$gte': float(amount)}})

    return json.dumps(products)

# get /api/catalog/category/unique
# return all the unique categories in the catalog


@app.get('/api/catalog/category/unique')
def get_unique_categories():
    categories = db.products.distinct('category')
    return json.dumps(categories)

# create a post on /api/coupons
# should receive a coupon object with code and discount
# should save the coupon in the database
# should return the coupon

# validate that there is a coupon discount in the request
# validate that the coupon has a code
# validate that the coupon has a discount


def get_all_coupons(conditions={}):
    coupons = db.coupons.find(conditions)
    coupons = [fix_id(c) for c in coupons]
    return coupons


@app.get('/api/coupons')
def get_coupons():
    return json.dumps(get_all_coupons())


@app.post('/api/coupons')
def add_coupon():
    # get the data from the request
    coupon = request.get_json()

    # break this condition into 3 different conditions
    if coupon is None:
        abort(400, 'Coupon cannot be empty')

    if 'code' not in coupon:
        abort(400, 'Coupon code is required')

    if 'discount' not in coupon:
        abort(400, 'Coupon discount is required')

    # validate if discont is a float or number
    if not isinstance(coupon['discount'], float) and not isinstance(coupon['discount'], int):
        abort(400, 'The coupon is not valid, the discount should be a number')

    # check if the coupon already exists
    if len(get_all_coupons({'code': coupon['code']})) > 0:
        abort(400, 'The coupon already exists')

    # add the coupon to the database
    db.coupons.insert_one(coupon)

    coupon['_id'] = str(coupon['_id'])

    return json.dumps(coupon)


@app.get('/api/coupons/<code>')
def get_coupon(code):
    coupon = db.coupons.find_one({'code': code})
    coupon = fix_id(coupon)
    if coupon is None:
        abort(404, 'Invalid coupon')

    return json.dumps(coupon)


@app.delete('/api/coupons/<code>')
def delete_coupon(code):
    # delete the coupon from the database
    db.coupons.delete_one({'code': code})

    return json.dumps("Coupon deleted")


@app.put('/api/coupons')
def update_coupon():
    # get the data from the request
    coupon = request.get_json()

    if coupon is None:
        abort(400, 'No coupon to update')

    code = coupon.pop('code')

    # update the coupon in the database
    res = db.coupons.update_one({'code': code}, {'$set': coupon})

    return json.dumps("Coupon updated")
