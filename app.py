from flask import Flask, render_template, session, redirect, url_for, request
from models import db, Product, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = "crochet_secret"

db.init_app(app)

@app.route('/signup', methods=["GET","POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        address = request.form["address"]

        new_user = User(
            name=name,
            email=email,
            password=password,
            address=address
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route('/login', methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email, password=password).first()

        if user:

            session["user_id"] = user.id

            return redirect(url_for("products"))

    return render_template("login.html")

@app.route('/logout')
def logout():

    session.pop("user_id", None)

    return redirect(url_for("home"))

@app.route('/checkout')
def checkout():

    if "user_id" not in session:
        return redirect(url_for("login"))

    cart_items = []
    total_price = 0

    if "cart" in session:

        for product_id, quantity in session["cart"].items():

            product = Product.query.get(product_id)

            if product:

                subtotal = product.price * quantity

                cart_items.append({
                    "product": product,
                    "quantity": quantity,
                    "subtotal": subtotal
                })

                total_price += subtotal

    shipping_price = 50
    grand_total = total_price + shipping_price

    return render_template(
        "checkout.html",
        cart_items=cart_items,
        total_price=total_price,
        shipping_price=shipping_price,
        grand_total=grand_total
    )

@app.route('/')
def home():
    return render_template('home.html')


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
        session["cart"] = {}

    cart = session["cart"]

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    session["cart"] = cart
    session.modified = True

    return redirect(url_for("cart"))


@app.route('/cart')
def cart():

    cart_items = []
    total_price = 0

    if "cart" in session:

        for product_id, quantity in session["cart"].items():

            product = Product.query.get(int(product_id))

            if product:

                subtotal = product.price * quantity

                cart_items.append({
                    "product": product,
                    "quantity": quantity,
                    "subtotal": subtotal
                })

                total_price += subtotal

    return render_template(
        "cart.html",
        cart_items=cart_items,
        total_price=total_price
    )


@app.route('/remove-from-cart/<int:product_id>')
def remove_from_cart(product_id):

    product_id = str(product_id)

    if "cart" in session:

        cart = session["cart"]

        if product_id in cart:
            del cart[product_id]

        session["cart"] = cart
        session.modified = True

    return redirect(url_for("cart"))

@app.route('/place-order')
def place_order():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if "cart" not in session:
        return redirect(url_for("products"))

    total_price = 0

    for product_id, quantity in session["cart"].items():

        product = Product.query.get(product_id)

        total_price += product.price * quantity

    shipping_price = 50

    order = Order(
        user_id=session["user_id"],
        total_price=total_price,
        shipping_price=shipping_price,
        payment_status="Pending",
        order_status="Processing"
    )

    db.session.add(order)
    db.session.commit()

    for product_id, quantity in session["cart"].items():

        product = Product.query.get(product_id)

        item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=quantity,
            price=product.price
        )

        db.session.add(item)

    db.session.commit()

    session.pop("cart", None)

    return "Order placed successfully!"

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)