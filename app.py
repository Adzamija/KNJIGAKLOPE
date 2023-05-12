import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from recipe import login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///recipe.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
# Data
list_of_rec = db.execute("SELECT * FROM blog")

# Homepage, index
@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
# Login function
def login():

    # Clearing session, forgets users_id
    session.clear()

    # Post method
    if request.method == "POST":

        # Checking is there any input in the email and password fields
        if not request.form.get("email") or not request.form.get("password"):
            # This alert needs to be shown, so alert message is true
            alert = True
            text = "Fill the input fields"
            return render_template("login.html", alert = alert, text = text)

        # Checking the email and password from DB
        # DB should have id, email, hash - password
        rows = db.execute("SELECT * FROM users WHERE email=?", request.form.get("email"))

        # Checking is the email in DB and unique, and password

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            # The email is not unique or the password is not correct
            alert = True
            text = "Email or password are not correct"
            return render_template("login.html", alert = alert, text = text)

        # If everything is fine, session gets the user_id
        session["user_id"] = rows[0]["id"]
        name = rows[0]["firstname"]

        return redirect(url_for('mydash', name=name))


    # Get method
    else:
        session.clear()
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
# Register function
def register():

    # Clearing session, forgets users_id
    session.clear()

    # Post method
    if request.method == "POST":

        # Checking is there all inputs for registration
        if not request.form.get("firstname") or not request.form.get("email") or not request.form.get("password") or not request.form.get("confirmation"):
            # Return alert for inputs
            alert = True
            text = "Fill the input fields"
            return render_template("register.html", alert = alert, text = text)

        # Checking first name
        if not request.form.get("firstname").isalpha():
            # If the first name is not string with JUST letters from a to z, return the alert
            alert = True
            text = "First name should have just letters from A to z (a to z)"
            return render_template("register.html", alert = alert, text = text)
        # Email
        elif "@" not in request.form.get("email"):
            # Checking is it valid email or not
            alert = True
            text = "Check the Email"
            return render_template("register.html", alert = alert, text = text )

        # Password [checking is password same as confirmation password]
        if request.form.get("password") != request.form.get("confirmation"):
            alert = True
            text = "The passwords are not the same"
            return render_template("register.html", alert = alert, text = text)

        # The number of chars for password is min 8, and for firstname is min 3
        if len(request.form.get("password")) < 8 or len(request.form.get("firstname")) < 3:
            # Return the alert, this alert should be different then alerts for field
            alert = True
            text = "The name should have at least 3 chars, and password should have at least 8 chars"
            return render_template("register.html", alert = alert, text = text )

        # Checking do we have the same email in DB
        email = db.execute("SELECT * FROM users WHERE email=?", request.form.get("email"))

        # If there is the same user return alert
        if email:
            alert = True
            text = "The user have already account, try to log in"
            return render_template("register.html", alert = alert, text = text)

        # Hashing the password
        hash_password = generate_password_hash(request.form.get("password"),method='pbkdf2:sha256', salt_length=8)

        # If is everything fine, insert the new user in to the DB
        db.execute("INSERT INTO users(firstname, email, hash) VALUES(?, ?, ?)", request.form.get("firstname"), request.form.get("email"), hash_password)

        # Rows
        rows = db.execute("SELECT * FROM users WHERE email=?", request.form.get("email"))
        session["user_id"] = rows[0]["id"]
        name = rows[0]["firstname"]

        # After inserting into DB, redirecting the user to the login page
        return render_template("mydashboard.html", name = name)

    else:
        # If user uses the GET method
        return render_template("register.html")

# Logout
@app.route("/logout")
def logout():
    # Log out the user, clearing the session and ID
    session.clear()
    # Redirecting user to the page / THIS NEEDS TO BE CHANGED, MAYBE REDIRECTING TO THE HOMEPAGE OR LOGIN PAGE WE WILL SEE
    return redirect("/")

# Dashboard
@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    if request.method == "GET":
        id = session["user_id"]
        name = db.execute("SELECT firstname FROM users WHERE id=?", id)
        klopa = db.execute("SELECT * FROM recipes WHERE name = 'Home bread'")
        recipe = klopa[0]["name"]
        picture = klopa[0]["image"]
        description = klopa[0]["description"]
        ingridients = klopa[0]["ingridients"]
        instructions = klopa[0]["instructions"]
        return render_template("extend-dash.html", name = name[0]["firstname"], recipe = recipe, picture = picture, description = description, ingridents = ingridients, instructions = instructions)


# User dashboard
@app.route("/mydash", methods=["GET", "POST"])
@login_required
def mydash():
    if request.method == "POST":
        return render_template("mydashboard.html")
    else:
        id = session["user_id"]
        name = db.execute("SELECT firstname FROM users WHERE id=?", id)
        length = len(list_of_rec)
        return render_template("mydash.html", name = name[0]["firstname"], weekly = list_of_rec, length = length)


# Favorites page
@app.route("/favorites", methods=["GET"])
@login_required
def favorites():
    if request.method == "GET":
        id = session["user_id"]
        name = db.execute("SELECT firstname FROM users WHERE id=?", id)

        favorites= db.execute("SELECT * FROM recipes WHERE user_id=?", id)
        length = len(favorites)
        return render_template("favorites.html", name = name[0]["firstname"], favorites=favorites, length=length)

# Submiting the recipe
@app.route("/submit", methods=["GET", "POST"])
@login_required
def submit():
    id = session["user_id"]
    name = db.execute("SELECT firstname FROM users WHERE id=?", id)
    if request.method == "POST":
        # All fields must be populated
        if not request.form.get("recipe-name") or not request.form.get("recipe-image") or not request.form.get("recipe-description") or not request.form.get("recipe-ingridients") or not request.form.get("recipe-instructions"):
            error = True
            text = "All fields in the form must be popluated"
            return render_template("submit.html", name = name[0]["firstname"], error = error, text = text)

        # Inserting in to the DB
        db.execute("INSERT INTO recipes (name, image, description, ingridients, instructions, user_id) VALUES (?, ?, ?, ?, ?, ?)", request.form.get("recipe-name"), request.form.get("recipe-image"), request.form.get("recipe-description"), request.form.get("recipe-ingridients"), request.form.get("recipe-instructions"), id)


        klopa = db.execute("SELECT * FROM recipes WHERE name=?", request.form.get("recipe-name"))
        recipe = klopa[0]["name"]
        picture = klopa[0]["image"]
        description = klopa[0]["description"]
        ingridients = klopa[0]["ingridients"]
        instructions = klopa[0]["instructions"]

        return render_template("extend-dash.html", name = name[0]["firstname"], recipe = recipe, picture = picture, description = description, ingridents = ingridients, instructions = instructions)


    else:
        return render_template("submit.html", name = name[0]["firstname"])

# Breakfast filter
@app.route("/breakfast")
@login_required
def breakfast():
    length = len(list_of_rec)
    new_list = []
    for n in range(0, length):
        if list_of_rec[n]['type'] == "Breakfast":
            new_list.append(list_of_rec[n])
    type="Breakfast"
    id = session["user_id"]
    name = db.execute("SELECT firstname FROM users WHERE id=?", id)
    return render_template("bfast.html", weekly = list_of_rec, length = length, type=type, name = name[0]["firstname"])

# Lunch filter
@app.route("/launch")
@login_required
def launch():
    length = len(list_of_rec)
    new_list = []
    for n in range(0, length):
        if list_of_rec[n]['type'] == "Launch":
            new_list.append(list_of_rec[n])
    type="Launch"
    id = session["user_id"]
    name = db.execute("SELECT firstname FROM users WHERE id=?", id)
    return render_template("laun.html", weekly = list_of_rec, length = length, type=type, name = name[0]["firstname"])

# DInner
@app.route("/dinner")
@login_required
def dinner():
    length = len(list_of_rec)
    new_list = []
    for n in range(0, length):
        if list_of_rec[n]['type'] == "Dinner":
            new_list.append(list_of_rec[n])
    type="Dinner"
    id = session["user_id"]
    name = db.execute("SELECT firstname FROM users WHERE id=?", id)
    return render_template("din.html", weekly = list_of_rec, length = length, type=type, name = name[0]["firstname"])


@app.route("/blog/<int:num>")
@login_required
def blog(num):
    id = int(num) + 1
    klopa = db.execute("SELECT * FROM blog WHERE id=?", id)
    recipe = klopa[0]["name"]
    picture = klopa[0]["image"]
    description = klopa[0]["description"]
    ingridients = klopa[0]["ingridients"]
    type = klopa[0]["type"]
    nav_link = type.lower()
    user_id = session["user_id"]
    name = db.execute("SELECT firstname FROM users WHERE id=?", user_id)
    return render_template("blog.html", num=num, recipe = recipe, picture = picture, description = description, ingridents = ingridients, type = type, nav = nav_link, name=name[0]['firstname'])


@app.route("/myrecipes")
@login_required
def myrecip():
    # Name for page
    user_id = session["user_id"]
    name = db.execute("SELECT firstname FROM users WHERE id=?", user_id)
    # My recepies for page
    myrec= db.execute("SELECT * FROM recipes WHERE user_id=?", user_id)
    length = len(myrec)
    return render_template("my-recipes.html", name=name[0]['firstname'], myrec=myrec, length=length)


@app.route("/myrec/<int:num>")
@login_required
def myrec(num):
    user_id = int(session["user_id"])
    id = int(num) + 1
    myrec = db.execute("SELECT * FROM recipes WHERE id=? AND user_id=?", id, user_id)
    recipe = myrec[0]["name"]
    picture = myrec[0]["image"]
    description = myrec[0]["description"]
    ingridients = myrec[0]["ingridients"]
    instructions = myrec[0]["instructions"]
    name = db.execute("SELECT firstname FROM users WHERE id=?", user_id)
    return render_template("myrec.html", num=num, recipe = recipe, picture = picture, description = description, ingridents = ingridients, instructions=instructions, name=name[0]['firstname'])



@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(401)
def page_not_found(error):
    return render_template('401.html'), 401

