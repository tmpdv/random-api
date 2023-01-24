import re
import json
import io

from pydantic import BaseModel
from typing import Union

from db.models import User

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


class UserCreateForm:
    def __init__(self, body: bytes):
        body_json = json.load(io.BytesIO(body.replace(b"'", b'"')))
        self.login = body_json['login']
        self.email = body_json['email']
        self.password = body_json['password']
        self.password_repeat = body_json['password_repeat']
        self.errors = []

    def validate(self):
        if not self.login:
            self.errors.append("Login is required")
        else:
            if not len(self.login) >= 3:
                self.errors.append("Login should contain not less than 3 symbols")
        if not self.email:
            self.errors.append("Email is required")
        else:
            if not re.search(regex, self.email):
                self.errors.append(f"Email should match regex: ${regex}")
        if not self.password:
            self.errors.append("Password is required")
        else:
            if not self.password_repeat:
                self.errors.append("Password repeat is required")
            else:
                if not self.password == self.password_repeat:
                    self.errors.append("Passwords not match")


class UserDTO:
    def __init__(self, user: User):
        self.id = user.id
        self.login = user.login
        self.email = user.email


class TokenData(BaseModel):
    login: Union[str, None] = None


class Token(BaseModel):
    access_token: str
    token_type: str
