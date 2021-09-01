from flask import Flask
from flask import jsonify
from flask import request
from flask.helpers import make_response
from methods import Token, Restricted
from flask_sqlalchemy import SQLAlchemy
import pymysql
import hashlib

app = Flask(__name__)
login = Token()
protected = Restricted()

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://secret:noPow3r@bootcamp-tht.sre.wize.mx:3306/bootcamp_tht'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
users = db.Table('users', db.metadata, autoload=True, autoload_with=db.engine)
qs = db.session.query(users).all()


# Just a health check
@app.route("/")
def url_root():
    for row in qs:
        print(row.username)
    return "Ok"


# Just a health check
@app.route("/_health")
def url_health():
    return "OK"


# e.g. http://127.0.0.1:8000/login
@app.route("/login", methods=['POST'])
def url_login():
    username = request.form['username']
    password = request.form['password']
    for row in qs:
        if username == row.username:
            salt = f"{password}{row.salt}"
            hashed=hashlib.sha512(salt.encode('ascii')).hexdigest()
            if hashed == row.password:
                role = row.role
                res = {
                    "data": login.generate_token(username, role)
                }
                return jsonify(res)
    return make_response("Username/Password combination is incorrect", 403)


# # e.g. http://127.0.0.1:8000/protected
@app.route("/protected")
def url_protected():
    auth_token = request.headers.get('Authorization')
    res = {
        "data": protected.access_data(auth_token)
    }
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8000)
