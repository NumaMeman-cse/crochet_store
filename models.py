from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    address = db.Column(db.Text)

    orders = db.relationship('Order', backref='user', lazy=True)


class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    image = db.Column(db.String(200))
    category = db.Column(db.String(100))
    stock = db.Column(db.Integer)


class Order(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    total_price = db.Column(db.Float)
    shipping_price = db.Column(db.Float)

    payment_status = db.Column(db.String(50))
    order_status = db.Column(db.String(50))

    items = db.relationship('OrderItem', backref='order', lazy=True)


class OrderItem(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    quantity = db.Column(db.Integer)

    price = db.Column(db.Float)