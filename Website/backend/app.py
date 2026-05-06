from flask import Flask, redirect
from flask_cors import CORS
from config import Config
from models import db
from flask import render_template
from routes.admin_routes import admin_routes
from routes.product_routes import product_routes
from routes.auth_routes import auth_routes
from extensions import mail
from flask import send_from_directory

# APP INIT
app = Flask(__name__)

# CONFIG
app.config.from_object(Config)
app.secret_key = "rustic-roots-secret-key"

# EXTENSIONS
CORS(app)
db.init_app(app)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = "arjunpal647489@gmail.com"
app.config["MAIL_PASSWORD"] = "12345678"
app.config['MAIL_DEFAULT_SENDER'] = ''


mail.init_app(app)

# BLUEPRINTS
app.register_blueprint(admin_routes)
app.register_blueprint(product_routes)
app.register_blueprint(auth_routes)

# DB CREATE
with app.app_context():
    db.create_all()

# TEST ROUTE
@app.route("/")
def home():
    return send_from_directory("static/customer", "index.html") 


if __name__ == "__main__":
    app.run(debug=True)