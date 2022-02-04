import typing

import firebase_admin
from fastapi import Depends, Security

from fastapi.security.http import HTTPBearer
from firebase_admin import auth

from .app import firebase_app

token = HTTPBearer(scheme_name="firebaseIdToken")


def validated_token(
    token: str = Security(token),
    app: firebase_admin.App = Depends(firebase_app),
) -> typing.Dict[str, typing.Any]:
    return auth.verify_id_token(token, app)
