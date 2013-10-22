from flask import Flask, render_template, request, redirect, session, url_for, flash
import model

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

@app.route("/")
def index():
    if session.get("username"):
        return "User %s is logged in! <a href='logout'>Logout</a>" % session["username"]
    else:
        return render_template("index.html")

@app.route("/", methods=["POST"])
def process_login():
    model.connect_to_db()
    username = request.form.get("username")
    password = request.form.get("password")

    user_id = model.authenticate(username, password)

    print "in app.py, user_id:", user_id

    if user_id != None:
        flash("User authenticated!")
        session['username'] = user_id
    else: 
        flash("Password incorrect, there may be a ferret stampede in progress!")


    return redirect(url_for("index"))


@app.route("/register")
def register():
    model.connect_to_db()
    if session.get("username"):
         # get username by id 
         username = model.get_username_by_id(session["username"])
         return redirect("users/"+username)
    else:
        return render_template("register.html")
    #model.register_new_user(new_username, new_password)

@app.route("/register", methods=["POST"])
def create_account():
    model.connect_to_db()
    username = request.form.get("username")
    password = request.form.get("password")
    model.create_new_user(username, password)

    # TODO automatic login once registration is done
    
    return redirect("user/" + username)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/user/<username>")
def view_user(username):
    model.connect_to_db()
    posts = model.get_user_by_name(username)
    user_id = session.get("username")
    return render_template("wall.html", wall_posts = posts, user_id = user_id)

# this grabs info on the wall of a user's wall
@app.route("/user/<username>", methods=["POST"])
def post_to_wall(username):
    model.connect_to_db()

    # this is a note of who is who
    owner_username = username

    # this is author that will be posting to the owners user wall
    author_user_id = session.get("username")
    new_post = request.form.get("post_content")

    model.make_wall_post(author_user_id, owner_username, new_post)
    return redirect("/user/" + username)



if __name__ == "__main__":
    app.run(debug = True)
