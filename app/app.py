from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "SUPERSECRETKEY"  # intentionally hardcoded (for DevSecOps testing)

# Database location (must already exist)
DATABASE = "data/database.db"

# ---------------------------
# DB Helper Functions
# ---------------------------
def get_db():
    if "_database" not in g:
        g._database = sqlite3.connect(DATABASE)
    return g._database

@app.teardown_appcontext
def close_connection(exception):
    db = g.pop("_database", None)
    if db is not None:
        db.close()

# ---------------------------
# Routes
# ---------------------------
@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]  # intentionally plain text
        role = "user"

        db = get_db()
        try:
            db.execute(
                f"INSERT INTO users(username, password, role) VALUES('{username}','{password}','{role}')"
            )
            db.commit()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            return "Username already exists!"

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        cursor = db.execute(
            f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        )
        user = cursor.fetchone()

        if user:
            session["user"] = user[1]
            session["role"] = user[3]
            return redirect(url_for("dashboard"))
        else:
            return "Invalid credentials!"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        username=session["user"],
        role=session["role"]
    )


@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return "Access denied!"

    db = get_db()
    users = db.execute("SELECT id, username, role FROM users").fetchall()

    return render_template("admin.html", users=users)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------------------
# App Start
# ---------------------------
if __name__ == "__main__":
    # Ensure data folder exists (does NOT create DB schema)
    os.makedirs("data", exist_ok=True)

    app.run(host="0.0.0.0", port=5000, debug=True)
