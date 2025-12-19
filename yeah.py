from flask import Flask, request, render_template, make_response,redirect,Response,url_for
import json
from argon2 import PasswordHasher
import os
import base64
import datetime
cookies:dict={}
with open("logins/cookies.json") as f:
    cookies=json.loads(f.read())
hasher = PasswordHasher()
lol = Flask(__name__)
title="Placeholder"
with open("logins/users.json") as f:
    global users
    users: dict = json.loads(f.read())
user = users
dt=datetime.datetime.now()
@lol.route("/")
def home():
    cookie=request.cookies.get("cookie")
    print(f"{cookies.get(cookie,"A new visitor")} has visited the website.")
    if cookies.get(cookie)!=None:
        return render_template("index.html",login=True,username=cookies.get(cookie,"A new visitor"),title=title)
    else:
        return render_template("index.html",title=title)
@lol.route('/favicon.ico')
def favicon():
    with open("static/favicon.ico","rb") as f:
        return f.read()
@lol.route("/blog")
def blog():
    with open("blog/posts.json") as f:
        cookie=request.cookies.get("cookie")
        posts:dict=json.loads(f.read())
        cookie=request.cookies.get("cookie")
        if cookies.get(cookie)!=None:
            return render_template("blog.html",posts=posts,login=True,title=title)
        else:
            return render_template("blog.html",posts=posts,title=title)
@lol.route("/login")
def login():
    cookie=request.cookies.get("cookie")
    if cookies.get(cookie)!=None:
        return redirect("/")
    else:
        return render_template("login.html",title=title)
@lol.route("/signup")
def signup():
    cookie=request.cookies.get("cookie")
    if cookies.get(cookie)!=None:
        return redirect("/")
    else:
        return render_template("signup.html",title=title)
@lol.route("/signout")
def signout():
    cookie=request.cookies.get("cookie")
    with open("logins/cookies.json") as f:
        cookies=json.loads(f.read())
        if cookies.get(cookie)!=None:
            with open("logins/cookies.json","r") as f:
                cookies=json.loads(f.read())
            resp=redirect("/")
            cookies.pop(request.cookies.get("cookie"))
            resp.delete_cookie("cookie")
            with open("logins/cookies.json","w") as f:
                f.write(json.dumps(cookies,indent=2))
            return resp
        else:
            return redirect("/")
@lol.route("/signup_post", methods=["POST"])
def signup_post():
    cookie=request.cookies.get("cookie")
    if cookies.get(cookie)!=None:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            password=hasher.hash(password)
            user[username]={"hash": password}
            with open("logins/users.json","w") as f:
                f.write(json.dumps(user,indent=2))
            return render_template("login.html",title=title)
        else:
            return render_template("signup.html",title=title)
@lol.route("/login_post", methods=["POST"])
def login_post():
    cookie=request.cookies.get("cookie")
    if cookies.get(cookie)!=None:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            try:
                if hasher.verify(user.get(username,"")["hash"],password):
                    byte = os.urandom(32)
                    code = base64.urlsafe_b64encode(byte).rstrip(b"=")
                    currentcookie = code.decode("utf-8")
                    cookies[currentcookie] = username
                    a=make_response(redirect("/")) 
                    with open("logins/cookies.json","w") as f:
                        f.write(json.dumps(cookies,indent=2))
                    a.set_cookie("cookie",f"{currentcookie}",secure=True,httponly=True)
                    return a
            except Exception as e:
                print(e)
                return render_template("login.html",failed=True,title=title)
        else:
            return render_template("login.html",title=title)
@lol.errorhandler(404)
def error(e):
    return render_template("notfound.html",title=title)
if __name__ == "__main__":
    lol.run(debug=True)
