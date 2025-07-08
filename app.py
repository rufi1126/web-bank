from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "rahasia"  # untuk session

@app.route("/register")
def register():
    return render_template("register.html")


# Halaman Utama
@app.route("/")
def home():
    return render_template("index.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Login sederhana (bisa diganti database)
        if email == "admin@email.com" and password == "123456":
            session["username"] = "Admin"
            session["saldo"] = 1000000
            return redirect(url_for("dashboard"))
        else:
            return "Login gagal. Coba lagi."

    return render_template("login_nya.html")

# Dashboard
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["username"], saldo=session["saldo"])

# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
