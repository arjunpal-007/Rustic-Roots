from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# models.py
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    description = db.Column(db.Text)
    image = db.Column(db.String(200))
    is_best_seller = db.Column(db.Boolean, default=False)



class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    items = db.Column(db.Text)
    total = db.Column(db.Integer)
    payment_method = db.Column(db.String(50))   # 🔥 NEW
    payment_status = db.Column(db.String(50), default="Pending")  # 🔥 NEW
    status = db.Column(db.String(50), default="Pending")



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    name = db.Column(db.String(100))
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)

