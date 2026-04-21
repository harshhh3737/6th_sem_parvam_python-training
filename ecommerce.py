# E-Commerce Website using Flask
# Features:
# Product Listing
# Cart using Sessions
# Checkout
# SQLite Database
# Admin Panel

from flask import Flask, render_template_string, request, redirect, session, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret123"
DB = "ecommerce.db"

# ---------------- DATABASE ---------------- #

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price REAL,
        stock INTEGER
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer TEXT,
        total REAL
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        product_name TEXT,
        qty INTEGER,
        price REAL
    )
    ''')

    conn.commit()
    conn.close()

def get_products():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    data = cur.fetchall()
    conn.close()
    return data

# ---------------- HOME ---------------- #

@app.route("/")
def home():
    products = get_products()
    html = '''
    <h1>🛒 E-Commerce Store</h1>
    <a href="/cart">View Cart</a> | <a href="/admin">Admin Panel</a>
    <hr>
    {% for p in products %}
        <h3>{{p[1]}}</h3>
        <p>Price: ₹{{p[2]}}</p>
        <p>Stock: {{p[3]}}</p>
        <a href="/add/{{p[0]}}">Add to Cart</a>
        <hr>
    {% endfor %}
    '''
    return render_template_string(html, products=products)

# ---------------- CART ---------------- #

@app.route("/add/<int:id>")
def add_cart(id):
    cart = session.get("cart", {})

    cart[str(id)] = cart.get(str(id), 0) + 1

    session["cart"] = cart
    return redirect("/")

@app.route("/cart")
def cart():
    cart = session.get("cart", {})
    products = get_products()

    cart_items = []
    total = 0

    for p in products:
        pid = str(p[0])
        if pid in cart:
            qty = cart[pid]
            subtotal = qty * p[2]
            total += subtotal
            cart_items.append((p[1], qty, p[2], subtotal))

    html = '''
    <h1>🛒 Shopping Cart</h1>
    <a href="/">Continue Shopping</a><br><br>

    {% for item in cart_items %}
        <p>{{item[0]}} | Qty: {{item[1]}} | ₹{{item[2]}} each | ₹{{item[3]}}</p>
    {% endfor %}

    <h3>Total: ₹{{total}}</h3>

    <a href="/checkout">Proceed to Checkout</a>
    '''
    return render_template_string(html, cart_items=cart_items, total=total)

# ---------------- CHECKOUT ---------------- #

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart = session.get("cart", {})
    if not cart:
        return "Cart is empty"

    if request.method == "POST":
        customer = request.form["customer"]

        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        products = get_products()

        total = 0
        items = []

        for p in products:
            pid = str(p[0])
            if pid in cart:
                qty = cart[pid]
                subtotal = qty * p[2]
                total += subtotal
                items.append((p[1], qty, p[2]))

        cur.execute("INSERT INTO orders(customer,total) VALUES (?,?)",
                    (customer, total))
        order_id = cur.lastrowid

        for item in items:
            cur.execute('''
            INSERT INTO order_items(order_id,product_name,qty,price)
            VALUES (?,?,?,?)
            ''', (order_id, item[0], item[1], item[2]))

        conn.commit()
        conn.close()

        session.pop("cart", None)

        return f"<h2>Order Placed Successfully!</h2><p>Total ₹{total}</p><a href='/'>Home</a>"

    return '''
    <h1>Checkout</h1>
    <form method="post">
        Enter Name: <input type="text" name="customer" required>
        <button type="submit">Place Order</button>
    </form>
    '''

# ---------------- ADMIN PANEL ---------------- #

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        stock = request.form["stock"]

        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("INSERT INTO products(name,price,stock) VALUES (?,?,?)",
                    (name, price, stock))
        conn.commit()
        conn.close()

        return redirect("/admin")

    products = get_products()

    html = '''
    <h1>⚙️ Admin Panel</h1>
    <a href="/">Home</a><br><br>

    <form method="post">
        Product Name: <input name="name" required><br><br>
        Price: <input name="price" required><br><br>
        Stock: <input name="stock" required><br><br>
        <button type="submit">Add Product</button>
    </form>

    <hr>
    <h2>Products</h2>

    {% for p in products %}
        <p>{{p[1]}} | ₹{{p[2]}} | Stock: {{p[3]}}</p>
    {% endfor %}
    '''
    return render_template_string(html, products=products)

# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    init_db()
    app.run(debug=True)