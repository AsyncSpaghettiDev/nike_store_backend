from flask import Flask
import json
from config import me, hello
from mock_data import catalog

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


@app.get('/api/catalog')
def get_catalog():
    return json.dumps(catalog)

# get /api/products/count
# return the number of products in the catalog


@app.get('/api/products/count')
def get_products_count():
    total_products = len(catalog)
    return json.dumps({'total_products': total_products})

# get /api/products/total
# return the sum of all the prices of the products in the catalog


@app.get('/api/products/total')
def get_products_total():
    total = 0
    for product in catalog:
        total += product['price']
    return json.dumps({'total': total})

# get /api/products/categories
# return all the products that below to the received category


@app.get('/api/products/categories/<category>')
def get_products_by_category(category):
    products = []
    category = category.lower()
    for product in catalog:
        if product['category'].lower() == category:
            products.append(product)
    return json.dumps(products)

# get /api/catalog/lower/<amount>
# return all the products that are below the received amount


@app.get('/api/catalog/lower/<amount>')
def get_products_lower_than(amount):
    products = []
    for product in catalog:
        if product['price'] < float(amount):
            products.append(product)
    return json.dumps(products)

# get /api/category/unique
# return all the unique categories in the catalog


@app.get('/api/category/unique')
def get_unique_categories():
    categories = []
    for product in catalog:
        if product['category'] not in categories:
            categories.append(product['category'])
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


app.run(debug=True)
