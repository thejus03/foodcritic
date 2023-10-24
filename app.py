#importing all required libraries
from cs50 import SQL
from flask import Flask, redirect, render_template, session, request
from flask_session import Session
from helpers import login_required, gpt_ask
from werkzeug.security import check_password_hash, generate_password_hash

#configuring application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///uniplanner.db") # establishes connection to .db file that i created.

# header that ensures that the information is not cached by the website or any other third party. Basically protects sensitive information
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    user_restaurants = db.execute("SELECT * FROM restaurants WHERE user_id =?", session["user_id"])
    if len(user_restaurants)>0:

        return render_template("index.html",user_restaurants=user_restaurants)
    else:
        notice = "--no restaurants rated--"
        return render_template("index.html",notice=notice)
    
@app.route("/add" , methods=["GET", "POST"])
@login_required
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:
        given_restaurant = request.form.get("input-restaurant").lower().capitalize()
        restaurant_info = db.execute("SELECT * FROM restaurants WHERE restaurant_name=?", given_restaurant)
        if len(restaurant_info)!=0:
            notice = "You have already visited this restaurant"
            return render_template("add.html", notice=notice)
        given_rating = round(float(request.form.get("input-rating")),1)
        given_description = request.form.get("input-description")
        given_cusine = request.form.get("input-cusine").lower().capitalize()
        
        
        if given_rating<0 or given_rating>5:
            notice = "Rating must be within 0 to 5!"
            return render_template("add.html",notice=notice)
        
        else:
            db.execute("INSERT INTO restaurants (user_id, rating,restaurant_name,description,cusine) VALUES (?,?,?,?,?)", session["user_id"], given_rating, given_restaurant, given_description, given_cusine)
            return redirect("/")
@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "GET":
        return render_template("search.html")
    else:
        given_question = request.form.get("question").lower().capitalize()
        reply_info = db.execute("SELECT * FROM restaurants WHERE user_id=? AND restaurant_name=? OR cusine=?", session["user_id"], given_question, given_question)
        return render_template("search.html", reply_info=reply_info)


@app.route("/delete", methods=["POST"])
@login_required
def delete():
    delete_rest = request.form.get("restaurant_name")
    db.execute("DELETE FROM restaurants WHERE restaurant_name=? AND user_id=?", delete_rest, session["user_id"])
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    #forget any user before
    session.clear()

    if request.method=="GET":
        return render_template("login.html")
    else:
        provided_username = request.form.get("username")
        user_info = db.execute("SELECT * FROM users WHERE username=?", provided_username)
        if len(user_info)==0:
            notice = "Incorrect username"
            return render_template("login.html", notice=notice)
        
        if len(user_info)==1:
            provided_password = request.form.get("password")
            if check_password_hash(user_info[0]["hash_pass"],provided_password)==True:
                session["user_id"] = user_info[0]["id"]
                return redirect("/")
            
            else:
                notice = "Incorrect password"
                return render_template("login.html", notice=notice)
            

@app.route("/register", methods={"GET", "POST"})
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        given_username = request.form.get("username")
        given_password = request.form.get("password")
        given_confirmation = request.form.get("confirmation")
        if not given_username or not given_password or not given_confirmation:
            notice = "Please enter all fields!"
            return render_template("register.html", notice=notice)
        
        user_info = db.execute("SELECT username FROM users WHERE username=?", given_username)
        if len(user_info)!=0:
            notice = "Username taken"
            return render_template("register.html", notice=notice)
        
        elif given_password != given_confirmation:
            notice = "Passwords do not match!"
            return render_template("register.html", notice=notice)
        elif len(given_password)<8:
            notice = "Password must have at least 8 characters!"
            return render_template("register.html", notice=notice)
        else:
            db.execute("INSERT INTO users (username, hash_pass) VALUES (?, ?)", given_username, generate_password_hash(given_password))
            return redirect("/")


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/ask", methods=["GET", "POST"])
@login_required
def ask():
    if request.method == "GET":
        return render_template("ask.html")
    else:
        question = request.form.get("question")
        if not question:
            return redirect("/ask")
        
        answer_list = gpt_ask(question)
        return render_template("ask.html", answer_list=answer_list)
