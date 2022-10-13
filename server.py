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


app.run(debug=True)
