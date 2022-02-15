from fastapi import APIRouter, Depends
import typing
from fastapi_firebase.auth import validate_token

router = APIRouter()


@router.get("/current-token")
def current_token(data: typing.Dict[str, typing.Any] = Depends(validate_token)):
    return data
