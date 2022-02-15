import pydantic


class AppSettings(pydantic.BaseSettings):
    PORT: int = pydantic.Field(8000)
    HOST: pydantic.IPvAnyAddress = pydantic.Field("0.0.0.0")


settings = AppSettings()
