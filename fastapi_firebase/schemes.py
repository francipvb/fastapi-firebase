import datetime
import pydantic


class TokenData(pydantic.BaseModel):
    provider_id: str
    issuer: pydantic.HttpUrl = pydantic.Field(..., alias="iss")
    audience: str = pydantic.Field(..., alias="aud")
    auth_time: datetime.datetime
    expires_at: datetime.datetime = pydantic.Field(..., alias="exp")
    issued_at: datetime.datetime = pydantic.Field(..., alias="iat")
    user_id: str
    sub: str
