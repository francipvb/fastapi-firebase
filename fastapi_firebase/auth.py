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
    bearerFormat="JWT",
    description="The firebase Id token, provided by client SDK.",
)
_failed_auth_headers = {"WWW-Authenticate": "Bearer"}


def validate_token(
    credential: typing.Optional[HTTPAuthorizationCredentials] = Security(token),
    app: firebase_admin.App = Depends(firebase_app),
) -> typing.Optional[typing.Dict[str, typing.Any]]:
    if credential is None:
        return None

    try:
        return auth.verify_id_token(credential.credentials, app)
    except auth.RevokedIdTokenError:
        raise fastapi.HTTPException(403, "The token has been revoked.")
    except auth.ExpiredIdTokenError:
        raise fastapi.HTTPException(403, "The token has expired.")
    except auth.InvalidIdTokenError:
        raise fastapi.HTTPException(401, "Invalid token received.", _failed_auth_headers)
    except auth.UserDisabledError:
        raise fastapi.HTTPException(403, "The user has been disabled.")


def token_info(token: typing.Optional[typing.Dict[str, typing.Any]] = Depends(validate_token)):
    if token is None:
        return None

    return pydantic.parse_obj_as(TokenData, token)


def required_token_info(info: TokenData = fastapi.Depends(token_info)):
    if info is None:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"www-authenticate": "Bearer"},
        )

    return info
