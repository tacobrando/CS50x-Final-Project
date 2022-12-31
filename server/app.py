import os
from flask import Flask, request, jsonify, session, send_file
from flask_cors import CORS
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from config import AppConfig
from models import get_uuid, db, User, Product, Order, Order_Item


UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config.from_object(AppConfig)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)
CORS(app, supports_credentials=True)

Session(app)

with app.app_context():
    db.create_all()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/user")
@app.route("/user/<username>/products")
def user_session(username=None):
    if username is None:
        userId = session.get("user_id")
        if userId is None:
            return jsonify({"error": "Unauthorized"}), 401

        user = User.query.filter_by(id=userId).first()
        if user is not None:
            return jsonify({
                "id": user.id,
                "username": user.username,
                "created": user.created
            })
        return "Error"
    else:
        productList = []
        user = User.query.filter_by(username=username).first()
        products = Product.query.filter_by(user_id=user.id)

        for product in products:
            productList.append(product.serialize())
        return productList


@app.route("/register", methods=["POST"])
def register():
    formData = request.get_json()

    print(formData)

    if len(formData["username"]) < 4:
        return jsonify({"error": "Username must be at least 4 characters"}), 403

    check_duplicate_user = User.query.filter_by(
        username=formData["username"]).first()

    if check_duplicate_user is not None:
        return jsonify({"error": "Username already taken!"}), 403

    haskKey = generate_password_hash(formData["password"])

    user = User(username=formData["username"], hash=haskKey)
    db.session.add(user)
    db.session.commit()

    session["user_id"] = user.id
    session["cart"] = []

    return jsonify({
        "status": "success!"
    })


@app.route("/login", methods=["POST"])
def login():
    session.clear()

    formData = request.get_json()

    user = User.query.filter_by(username=formData["username"]).first()

    if user is None:
        return jsonify({"error": "Incorrect Username"}), 401
    elif not check_password_hash(user.hash, formData["password"]):
        return jsonify({"error": "Incorrect password"}), 401

    session["user_id"] = user.id
    session["cart"] = []

    return jsonify({
        "status": "success"
    })


@app.route("/logout")
def logout():
    session.clear()
    return jsonify({
        "status": "success"
    })


@app.route("/cart", methods=["GET", "POST"])
def cart():
    if request.method == "GET":
        if session["cart"] is not None:
            return session["cart"]
        return {
            "status": "empty"
        }


@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    if request.method == "POST":
        if 'cart' in session:
            product = request.get_json()

            if product in session['cart']:
                return jsonify({
                    "error": "Item already in cart!"
                }), 400

            session["cart"].append(product)
            session.modified = True

            return jsonify({
                "status": "added"
            })
        else:
            return jsonify({
                "status": "error"
            }), 400


@app.route("/remove-from-cart/<index>")
def remove_from_cart(index):
    del session['cart'][int(index)]
    session.modified = True

    return jsonify({
        "Status": "deleted"
    })


@app.route("/checkout", methods=["POST"])
def checkout():
    products = request.get_json()
    if len(products) >= 1:
        sellToOrder = Order(user_id=session['user_id'], status="Bought")
        db.session.add(sellToOrder)
        db.session.commit()
        for i in range(len(products)):
            user = User.query.filter_by(id=products[i]['user_id']).first()
            buyFromOrder = Order(user_id=user.id, status="Sold")
            db.session.add(buyFromOrder)
            db.session.commit()

            order_item_buyer = Order_Item(order_id=buyFromOrder.id,
                                          product_id=products[i]['id'], price=products[i]['price'], title=products[i]['title'], image=products[i]['image'])

            order_item_seller = Order_Item(order_id=buyFromOrder.id,
                                           product_id=products[i]['id'], price=products[i]['price'], title=products[i]['title'], image=products[i]['image'])

            db.session.add(order_item_buyer)
            db.session.add(order_item_seller)
            db.session.commit()

            buyFromOrder.items.append(order_item_seller)
            sellToOrder.items.append(order_item_buyer)

            product = Product.query.filter_by(id=products[i]['id']).first()
            db.session.delete(product)

            db.session.commit()

        session['cart'] = []

        return "Success"


@app.route("/get-orders")
def get_orders():
    orders = Order.query.filter_by(user_id=session['user_id'])

    orderList = []
    order_items = []

    for order in orders:
        obj = {
            "id": order.id,
            "user_id": order.user_id,
            "status": order.status,
            "created": order.created,
            "items": []
        }

        for i in range(len(order.items)):
            item = {
                "id": order.items[i].id,
                "order_id": order.items[i].order_id,
                "title": order.items[i].title,
                "image": order.items[i].image,
            }
            obj['items'].append(item)

        orderList.append(obj)

    return orderList


@app.route('/add-product', methods=["POST"])
def add_product():
    if request.method == "POST":
        if 'file' not in request.files:
            return jsonify({
                "error": "No file part!"
            }), 401
        file = request.files['file']

        title = request.form['title']
        price = int(request.form['price'])
        category = request.form['category']
        description = request.form['description']

        if file.filename == "":
            return jsonify({
                "error": "No file selected!"
            })

        if file and allowed_file(file.filename):
            name = get_uuid()
            file_type = file.filename.split('.')[-1]
            file.filename = name + '.' + file_type
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            product = Product(user_id=session["user_id"], title=title, price=price,
                              category=category, description=description, image=filename)

            db.session.add(product)
            db.session.commit()

        return jsonify({
            "status": "success"
        })


@ app.route('/remove-product/<id>')
def remove_product(id):
    if session["user_id"]:
        product = Product.query.filter_by(id=id).first()

        if product.user_id == session["user_id"]:
            db.session.delete(product)
            db.session.commit()
            return jsonify({
                "status": "deleted"
            })
    return jsonify({
        "error": "Unauthorised request"
    }), 401


@ app.route('/products')
@ app.route('/products/<id>')
def product(id=None):
    if id is None:
        productList = []
        products = Product.query.all()

        for i in range(len(products)):
            productList.append(products[i].serialize())
        return productList
    else:
        product = Product.query.filter_by(id=id).first()

        return product.serialize()


@ app.route('/image/<filename>', methods=["GET"])
def get_image(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    return send_file(file_path)
