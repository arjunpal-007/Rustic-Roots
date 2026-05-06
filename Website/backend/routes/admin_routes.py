from flask import Blueprint, request, jsonify, redirect, render_template, session
from models import db, Product
import os
from werkzeug.utils import secure_filename
from functools import wraps

admin_routes = Blueprint("admin_routes", __name__)

# =========================
# CONFIG
# =========================
UPLOAD_FOLDER = "backend/static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

products = []  # In-memory product list (replace with DB in production)

# =========================
# 🔐 ADMIN AUTH DECORATOR
# =========================
def admin_login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("admin"):
            return redirect("/admin/login")
        return func(*args, **kwargs)
    return wrapper


# =========================
# 🔑 ADMIN LOGIN
# =========================
@admin_routes.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "GET":
        return render_template("admin/login.html")

    data = request.json
    if data["email"] == "arjunpal647489@gmail.com" and data["password"] == "Admin@123":
        session["admin"] = True
        return jsonify({"success": True})

    return jsonify({"success": False})


# =========================
# 🚪 ADMIN LOGOUT
# =========================
@admin_routes.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect("/admin/login")


# =========================
# ➕ ADD PRODUCT
# =========================
@admin_routes.route("/add-product", methods=["POST"])
def add_product():

    name = request.form["name"]
    price = int(request.form["price"])
    description = request.form["description"]
    image = request.files["image"]

    is_best_seller = True if request.form.get("best_seller") else False

    if image:
        image_path = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(image_path)

        new_product = Product(
            name=name,
            price=price,
            description=description,
            image=image.filename,
            is_best_seller=is_best_seller
        )

        db.session.add(new_product)
        db.session.commit()

    return redirect("/static/admin/add-product.html?success=1")



# =========================
# 📦 GET ALL PRODUCTS (ADMIN)
# =========================
@admin_routes.route("/admin/products")
def admin_products():
    products = Product.query.all()
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "is_best_seller": p.is_best_seller
        } for p in products
    ])


# =========================
# ✏️ UPDATE ORDER STATUS
# =========================
@admin_routes.route("/admin/update-order-status/<int:id>", methods=["PUT"])
@admin_login_required
def update_order_status(id):
    from models import Order

    order = Order.query.get(id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    data = request.json
    order.status = data.get("status", order.status)
    db.session.commit()

    return jsonify({"message": "Status updated"})


# ❌ DELETE PRODUCT
@admin_routes.route("/admin/delete-product/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "deleted"})

# =========================
# 📦 GET ALL ORDERS
# =========================
@admin_routes.route("/admin/orders", methods=["GET"])
@admin_login_required
def get_orders():
    from models import Order

    orders = Order.query.all()
    return jsonify([
        {
            "id": o.id,
            "name": o.name,
            "phone": o.phone,
            "address": o.address,
            "total": o.total,
            "items": o.items,
            "status": o.status
        } for o in orders
    ])


# ✏️ UPDATE PRODUCT
@admin_routes.route("/admin/edit-product/<int:id>", methods=["PUT"])
def edit_product(id):
    data = request.get_json()
    product = Product.query.get(id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    product.name = data["name"]
    product.price = int(data["price"])
    product.description = data["description"]
    product.is_best_seller = data["is_best_seller"]

    db.session.commit()
    return jsonify({"message": "updated"})


# =========================
# ⭐ ADD BEST SELLER
# =========================
@admin_routes.route("/admin/add-best-seller", methods=["POST"])
@admin_login_required
def add_best_seller():
    image = request.files["image"]
    filename = secure_filename(image.filename)
    image.save(f"{UPLOAD_FOLDER}/{filename}")

    bs = BestSeller(
        name=request.form["name"],
        price=request.form["price"],
        description=request.form["description"],
        image=filename
    )
    db.session.add(bs)
    db.session.commit()

    return redirect("/static/admin/add-best-seller.html?success=1")


@admin_routes.route("/best-sellers")
def get_best_sellers():
    from models import BestSeller
    sellers = BestSeller.query.all()

    return jsonify([
        {
            "id": s.id,
            "name": s.name,
            "price": s.price,
            "image": s.image,
            "description": s.description
        } for s in sellers
    ])


@admin_routes.route("/admin/delete-order/<int:id>", methods=["DELETE"])
def delete_order(id):
    order = Order.query.get(id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "deleted"})
