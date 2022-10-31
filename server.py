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

    if product is None:
        abort(400, 'No product required')

    # add the product to the database
    product['category'] = product['category'].lower()

    print('----------')
    db.products.insert_one(product)
    print('----------')

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


@app.get('/api/test/colors')
def unique_colors():
    colors = ["red", 'blue', "Pink", "yelloW", "Red",
              "Black", "BLUE", "RED", "BLACK", "YELLOW"]
    unique_colors = []
    for color in colors:
        if color.lower() not in unique_colors:
            unique_colors.append(color.lower())
    return json.dumps(unique_colors)


@app.get('/api/test/count/<color>')
def count_colors(color):
    colors = ["red", 'blue', "Pink", "yelloW", "Red",
              "Black", "BLUE", "RED", "BLACK", "YELLOW"]
    count = 0
    for c in colors:
        if c.lower() == color.lower():
            count += 1
    return json.dumps({'count': count})


# app.run(debug=True)
