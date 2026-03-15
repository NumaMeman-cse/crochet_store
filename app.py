from flask import Flask, render_template, session, redirect, url_for
from models import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "crochet_secret"

db.init_app(app)


@app.route('/')
def home():
    return render_template('home.html')

from models import Product

@app.route('/products')
def products():

    all_products = Product.query.all()

    return render_template(
        "products.html",
        products=all_products
    )

@app.route('/add-test-product')
def add_test_product():

    new_product = Product(
        name="Crochet Bag",
        description="Handmade crochet bag",
        price=499,
        image="https://via.placeholder.com/300",
        category="Bags",
        stock=10
    )

    db.session.add(new_product)
    db.session.commit()

    return "Product Added!"
@app.route('/product/<int:product_id>')
def product_detail(product_id):

    product = Product.query.get(product_id)

    return render_template(
        "product_detail.html",
        product=product
    )

@app.route('/add-to-cart/<int:product_id>')
def add_to_cart(product_id):

    if "cart" not in session:
        session["cart"] = []

    session["cart"].append(product_id)

    session.modified = True

    return redirect(url_for("cart"))

@app.route('/cart')
def cart():

    cart_items = []

    if "cart" in session:

        for product_id in session["cart"]:
            product = Product.query.get(product_id)
            cart_items.append(product)

    return render_template(
        "cart.html",
        cart_items=cart_items
    )

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)