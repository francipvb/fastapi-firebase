import typing
import fastapi

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
_failed_auth_headers = {"WWW-Authenticate": "Bearer"}


def validate_token(
    credential: HTTPAuthorizationCredentials = Security(token),
    app: firebase_admin.App = Depends(firebase_app),
) -> typing.Dict[str, typing.Any]:
    try:
        return auth.verify_id_token(credential.credentials, app)
    except auth.InvalidIdTokenError:
        raise fastapi.HTTPException(401, "Invalid token received.", _failed_auth_headers)
    except auth.UserDisabledError:
        raise fastapi.HTTPException(403, "The user has been disabled.")
    except auth.RevokedIdTokenError:
        raise fastapi.HTTPException(403, "The token has been revoked.")
    except auth.ExpiredIdTokenError:
        raise fastapi.HTTPException(403, "The token has expired.")


def token_info(token: typing.Dict[str, typing.Any] = Depends(validate_token)):
    return pydantic.parse_obj_as(TokenData, token)
