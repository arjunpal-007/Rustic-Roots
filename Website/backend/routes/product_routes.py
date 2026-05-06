import io
import os
import json
from flask import Blueprint, jsonify, request, send_file
from models import Product, Order, db, Review
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from flask_mail import Message
from extensions import mail

product_routes = Blueprint("product_routes", __name__)

# ===============================
# 📦 GET ALL PRODUCTS
# ===============================
@product_routes.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()

    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "description": p.description,
            "image": p.image,
            "is_best_seller": p.is_best_seller
        }
        for p in products
    ])


# ===============================
# 📦 SINGLE PRODUCT
# ===============================
@product_routes.route("/product/<int:id>", methods=["GET"])
def get_single_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "description": product.description,
        "image": product.image,
        "is_best_seller": product.is_best_seller
    })


# ===============================
# 🛒 PLACE ORDER
# ===============================
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

@product_routes.route("/place-order", methods=["POST"])
def place_order():

    data = request.get_json()

    order = Order(
        name=data["name"],
        phone=data["phone"],
        address=data["address"],
        items=json.dumps(data["items"]),
        total=int(data["total"]),
        status="Paid"
    )

    db.session.add(order)
    db.session.commit()

    # ==========================
    # 🧾 CREATE INVOICE PDF (MEMORY)
    # ==========================
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("<b>Rustic Roots Invoice</b>", styles["Title"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Order ID: {order.id}", styles["Normal"]))
    elements.append(Paragraph(f"Customer: {order.name}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    items = data["items"]
    table_data = [["Product", "Price", "Qty", "Subtotal"]]

    for item in items:
        qty = item.get("quantity", 1)
        subtotal = item["price"] * qty
        table_data.append([
            item["name"],
            f"₹{item['price']}",
            qty,
            f"₹{subtotal}"
        ])

    table_data.append(["", "", "Total", f"₹{order.total}"])

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgreen),
        ('GRID', (0,0), (-1,-1), 1, colors.grey)
    ]))

    elements.append(table)
    doc.build(elements)
    buffer.seek(0)

    # ==========================
    # 📦 BUILD HTML PRODUCT LIST
    # ==========================
    product_html = ""
    for item in items:
        qty = item.get("quantity", 1)
        subtotal = item["price"] * qty

        product_html += f"""
        <tr>
            <td>{item['name']}</td>
            <td>₹{item['price']}</td>
            <td>{qty}</td>
            <td>₹{subtotal}</td>
        </tr>
        """

    # ==========================
    # 📧 CUSTOMER EMAIL (HTML)
    # ==========================
    customer_msg = Message(
        subject=f"🛒 Order Confirmation - #{order.id}",
        recipients=[data["email"]]
    )

    customer_msg.html = f"""
    <div style="font-family:Arial;">
        <h2 style="color:#2e7d32;">Thank you for your order 🌿</h2>

        <p><b>Order ID:</b> {order.id}</p>

        <table border="1" cellpadding="8" cellspacing="0" width="100%">
            <tr style="background:#2e7d32;color:white;">
                <th>Product</th>
                <th>Price</th>
                <th>Qty</th>
                <th>Subtotal</th>
            </tr>
            {product_html}
        </table>

        <h3>Total: ₹{order.total}</h3>

        <p>We will notify you once your order is shipped.</p>
    </div>
    """

    customer_msg.attach(
        filename=f"Invoice_{order.id}.pdf",
        content_type="application/pdf",
        data=buffer.read()
    )

    # ==========================
    # 📧 ADMIN EMAIL
    # ==========================
    admin_msg = Message(
        subject=f"📢 New Order #{order.id}",
        recipients=["arjunpal647489@gmail.com"]
    )

    admin_msg.html = f"""
    <h2>New Order Received 🚀</h2>

    <p><b>Customer:</b> {order.name}</p>
    <p><b>Phone:</b> {order.phone}</p>
    <p><b>Address:</b> {order.address}</p>

    <hr>

    <table border="1" cellpadding="8" cellspacing="0" width="100%">
        <tr style="background:black;color:white;">
            <th>Product</th>
            <th>Price</th>
            <th>Qty</th>
            <th>Subtotal</th>
        </tr>
        {product_html}
    </table>

    <h3>Total: ₹{order.total}</h3>
    """

    admin_msg.attach(
        filename=f"Invoice_{order.id}.pdf",
        content_type="application/pdf",
        data=buffer.getvalue()
    )

    try:
        mail.send(customer_msg)
        mail.send(admin_msg)
    except Exception as e:
        print("Mail error:", e)

    return jsonify({"message": "Order placed successfully"})


@product_routes.route("/update-status/<int:order_id>", methods=["POST"])
def update_status(order_id):

    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    data = request.get_json()
    new_status = data["status"]

    order.status = new_status
    db.session.commit()

    # 📧 Notify customer
    msg = Message(
        subject=f"📦 Order #{order.id} Update",
        recipients=[data["email"]]
    )

    msg.html = f"""
    <h2>Order Status Updated</h2>
    <p>Your order <b>#{order.id}</b> is now:</p>
    <h3 style="color:#2e7d32;">{new_status}</h3>
    """

    try:
        mail.send(msg)
    except:
        pass

    return jsonify({"message": "Status updated"})    


# ===============================
# 📄 DOWNLOAD INVOICE
# ===============================
@product_routes.route("/invoice/<int:order_id>")
def download_invoice(order_id):

    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("<b>Rustic Roots Invoice</b>", styles["Title"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"Order ID: {order.id}", styles["Normal"]))
    elements.append(Paragraph(f"Customer: {order.name}", styles["Normal"]))
    elements.append(Paragraph(f"Phone: {order.phone}", styles["Normal"]))
    elements.append(Paragraph(f"Address: {order.address}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    items = json.loads(order.items)

    table_data = [["Product", "Price", "Qty", "Subtotal"]]

    for item in items:
        qty = item.get("quantity", item.get("qty", 1))
        subtotal = item.get("price") * qty

        table_data.append([
            item.get("name"),
            f"₹{item.get('price')}",
            qty,
            f"₹{subtotal}"
        ])

    table_data.append(["", "", "Total", f"₹{order.total}"])

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER')
    ]))

    elements.append(table)
    doc.build(elements)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"Invoice_Order_{order.id}.pdf",
        mimetype="application/pdf"
    )


# ===============================
# 📦 MY ORDERS
# ===============================
@product_routes.route("/my-orders", methods=["GET"])
def my_orders():
    orders = Order.query.all()

    return jsonify([
        {
            "id": o.id,
            "total": o.total,
            "status": o.status,
            "items": json.loads(o.items)
        }
        for o in orders
    ])


# ===============================
# ⭐ BEST SELLERS
# ===============================
@product_routes.route("/best-sellers")
def best_sellers():
    products = Product.query.filter_by(is_best_seller=True).all()

    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "image": p.image
        }
        for p in products
    ])


# ===============================
# ➕ ADD PRODUCT
# ===============================
@product_routes.route("/add-product", methods=["POST"])
def add_product():

    name = request.form["name"]
    price = request.form["price"]
    description = request.form["description"]
    is_best_seller = request.form.get("is_best_seller") == "on"

    image_file = request.files["image"]
    filename = image_file.filename
    image_path = os.path.join("static/uploads", filename)
    image_file.save(image_path)

    new_product = Product(
        name=name,
        price=price,
        description=description,
        image=filename,
        is_best_seller=is_best_seller
    )

    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Product added successfully"})


# ===============================
# ⭐ ADD REVIEW
# ===============================
@product_routes.route("/add-review", methods=["POST"])
def add_review():
    data = request.get_json()

    review = Review(
        product_id=data["product_id"],
        name=data["name"],
        rating=int(data["rating"]),
        comment=data["comment"]
    )

    db.session.add(review)
    db.session.commit()

    return jsonify({"message": "Review added"})


# ===============================
# ⭐ GET REVIEWS
# ===============================
@product_routes.route("/reviews/<int:product_id>")
def get_reviews(product_id):

    reviews = Review.query.filter_by(product_id=product_id).all()

    return jsonify([
        {
            "name": r.name,
            "rating": r.rating,
            "comment": r.comment
        }
        for r in reviews
    ])


    # 📦 ADMIN ORDERS
@product_routes.route("/admin/orders")
def admin_orders():
    orders = Order.query.all()

    return jsonify([
        {
            "id": o.id,
            "name": o.name,
            "phone": o.phone,
            "address": o.address,
            "total": o.total,
            "status": o.status
        }
        for o in orders
    ])




@product_routes.route("/test-mail")
def test_mail():
    msg = Message(
        subject="Test Mail",
        recipients=["arjunpal647489@gmail.com"]
    )
    msg.body = "Mail working properly!"

    try:
        mail.send(msg)
        return "Mail sent!"
    except Exception as e:
        return str(e)
    

@product_routes.route("/send-query", methods=["POST"])
def send_query():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if not name or not email or not message:
        return jsonify({"error": "Missing fields"}), 400

    try:
        msg = Message(
            subject="New Website Query - Rustic Roots",
            sender="arjunpal647489@gmail.com",   # same as MAIL_USERNAME
            recipients=["arjunpal647489@gmail.com"]  # YOUR ADMIN EMAIL
        )

        msg.body = f"""
        New Query Received:

        Name: {name}
        Email: {email}

        Message:
        {message}
        """

        mail.send(msg)

        return jsonify({"message": "Query sent successfully"})

    except Exception as e:
        print("QUERY MAIL ERROR:", e)
        return jsonify({"error": "Mail failed"}), 500