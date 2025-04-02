from flask import Flask,render_template,request,redirect, url_for
import bleach
from flask_limiter import Limiter, RateLimitExceeded
from flask_limiter.util import get_remote_address
import user_management as dbHandler

app = Flask(__name__)
app.secret_key = "change_this_please" #change this and softcode it
ALLOWED_TAGS = ['b', 'i', 'br', 'p', 'span', 'a', 'ul', 'ol', 'li', 'strong', 'em']
ALLOWED_ATTRIBUTES = {'a': ['href', 'title', 'target']}
limiter = Limiter(app, default_limits=["6 per minute"])
LoggedIn=False

@app.route("/success.html", methods=["POST", "GET"])
@limiter.limit("1 per minute",error_message='Too many feedback attempts. Please try again later.')
def addFeedback():
    if LoggedIn:
        if request.method == "GET" and request.args.get("url"):
            url = request.args.get("url", "")
            return redirect(url, code=302)
        if request.method == "POST":
            feedback = request.form["feedback"]
            sanitized_feedback = bleach.clean(feedback, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
            dbHandler.insertFeedback(sanitized_feedback)
            dbHandler.listFeedback()
            return redirect(url_for('addFeedback'), code=303)
        else:
            dbHandler.listFeedback()
            return render_template("/success.html", state=True, value="Back")
    else:
        return redirect("/")

@app.route("/signup.html", methods=["POST", "GET"])
@limiter.limit("1 per minute",error_message='Too many signup attempts. Please try again later.')
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
@limiter.limit("6 per minute",error_message='Too many login attempts. Please try again later.')
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
            LoggedIn=True
            return render_template("/success.html", value=username, state=isLoggedIn)
        else:
            return render_template("/index.html")
    else:
        return render_template("/index.html")
    
@app.errorhandler(RateLimitExceeded)
def handle_rate_limit_exceeded(e):
    return jsonify({'message': 'Too many requests. Please try again later.'}), 429   

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
