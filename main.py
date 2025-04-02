from flask import Flask,render_template,request,redirect
import user_management as dbHandler
import bleach
# Code snippet for logging a message
# app.logger.critical("message")


app = Flask(__name__)
app.secret_key = "change_this_please" #change this and softcode it
ALLOWED_TAGS = ['b', 'i', 'br', 'p', 'span', 'a', 'ul', 'ol', 'li', 'strong', 'em']
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'target'],
}

@app.route("/success.html", methods=["POST", "GET"])
def addFeedback():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        feedback = request.form["feedback"]
        sanitized_feedback = bleach.clean(feedback, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
        dbHandler.insertFeedback(sanitized_feedback)
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")
    else:
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")


@app.route("/signup.html", methods=["POST", "GET"])
def signup():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        DoB = request.form["dob"]
        dbHandler.insertUser(username, password, DoB)
        return render_template("/index.html")
    else:
        return render_template("/signup.html")


@app.route("/index.html", methods=["POST", "GET"])
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        isLoggedIn = dbHandler.retrieveUsers(username, password)
        if isLoggedIn:
            dbHandler.listFeedback()
            return render_template("/success.html", value=username, state=isLoggedIn)
        else:
            return render_template("/index.html")
        print ("1")
    else:
        return render_template("/index.html")



if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=False, host="0.0.0.0", port=5000)
