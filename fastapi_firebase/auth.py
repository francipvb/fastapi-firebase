import typing

import firebase_admin
import pydantic
from fastapi import Depends, Security
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth

from .app import firebase_app
from .schemes import TokenData

token = HTTPBearer(
    scheme_name="firebaseIdToken",
)


def validate_token(
    token: HTTPAuthorizationCredentials = Security(token),
    app: firebase_admin.App = Depends(firebase_app),
) -> typing.Dict[str, typing.Any]:
    return auth.verify_id_token(token.credentials, app)


def token_info(token: typing.Dict[str, typing.Any] = Depends(validate_token)):
    return pydantic.parse_obj_as(TokenData, token)
