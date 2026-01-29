from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "atm_secret_key"

# ATM data (for learning purpose)
BALANCE = 10000
PIN = "1234"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pin = request.form["pin"]
        if pin == PIN:
            session["logged_in"] = True
            session["balance"] = BALANCE
            return redirect(url_for("atm"))
        else:
            return render_template("login.html", error="Invalid PIN")
    return render_template("login.html")


@app.route("/atm", methods=["GET", "POST"])
def atm():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if request.method == "POST":
        action = request.form["action"]
        amount = request.form.get("amount")

        if action == "deposit" and amount:
            session["balance"] += int(amount)

        elif action == "withdraw" and amount:
            if int(amount) <= session["balance"]:
                session["balance"] -= int(amount)

    return render_template("atm.html", balance=session["balance"])


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)

