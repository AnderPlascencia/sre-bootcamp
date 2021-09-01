from flask.json import jsonify
import jwt
from flask import jsonify

secret= "my2w7wjd7yXF64FIADfJxNs1oupTGAuW"

class Token:

    def generate_token(self, username, role):
        salt_password = "{password}"
        token = jwt.encode({
            "usename": username,
            "role": role
            }, key=secret)
        return token


class Restricted:

    def access_data(self, authorization):
        token = authorization[7:-1]
        print(type(token))
        data = jwt.decode(token, secret, algorithms=["HS256",])
        print(data)
        return 'test'
