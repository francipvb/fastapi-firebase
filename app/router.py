from fastapi import APIRouter, Depends
import typing
from fastapi_firebase.auth import validated_token

router = APIRouter()


@router.get("/current-token")
def validate_token(data: typing.Dict[str, typing.Any] = Depends(validated_token)):
    return data
