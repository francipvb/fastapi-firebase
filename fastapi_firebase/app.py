import typing

from fastapi import FastAPI
from firebase_admin import App, credentials, delete_app, initialize_app


def _initialize_app(
    *,
    app_name: str = None,
    credentials_file: str = None,
    credentials_content: typing.Dict[str, typing.Any] = None,
    firebase_options: typing.Dict[str, typing.Any] = None,
) -> App:
    """Initialize the firebase application

    Args:
        app_name (str, optional): The app name to initialize. Defaults to None.
        credentials_file (str, optional): The credentials file path to use. Defaults to None.
        credentials_content (typing.Dict[str, typing.Any], optional): The credentials decoded
            content. Defaults to None.
        firebase_options (typing.Dict[str, typing.Any], optional): Additional firebase options.
            Defaults to None.

    Returns:
        App: The newly initialized app.

    Raises:
        ValueError: If any validation fails.
    """

    kwargs = {}
    credential: credentials.Base = None
    if credentials_content:
        credential = credentials.Certificate(credentials_content)
    elif credentials_file:
        credential = credentials.Certificate(credentials_file)
    else:
        credential = credentials.ApplicationDefault()
    if credential:
        kwargs["credential"] = credential

    if app_name:
        kwargs["name"] = app_name

    if firebase_options:
        kwargs["options"] = firebase_options

    return initialize_app(name=app_name)


def setup(
    app: FastAPI,
    **kwargs: typing.Any,
):
    _app: App = None

    @app.on_event("startup")
    def _setup_app():
        nonlocal _app
        _app = _initialize_app(**kwargs)

    @app.on_event("shutdown")
    def _delete_app():
        nonlocal _app
        delete_app(_app)
        del _app

    app.dependency_overrides[App] = lambda: _app
