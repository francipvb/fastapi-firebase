import typing
import logging
from fastapi import FastAPI
from firebase_admin import App, credentials, delete_app, initialize_app

log = logging.getLogger()


class NotInitializedError(Exception):
    pass


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

    return initialize_app(**kwargs)


def setup(
    app: FastAPI,
    **kwargs: typing.Any,
):
    _app: App = None

    @app.on_event("startup")
    def _setup_app():
        nonlocal _app
        try:
            _app = _initialize_app(app_name=_app_name(app), **kwargs)
        except Exception as ex:
            log.exception(
                "Error while trying to initialize the firebase SDK with provided args.",
                stack_info=True,
                exc_info=ex,
            )
            raise

        app.dependency_overrides[firebase_app] = lambda: _app
        log.info("Firebase sdk initialized and attached.")

    @app.on_event("shutdown")
    def _delete_app():
        nonlocal _app
        del app.dependency_overrides[firebase_app]
        try:
            delete_app(_app)
            _app = None
        except Exception as ex:
            log.exception("Error while deleting the firebase app.", exc_info=ex)


def firebase_app():
    """Return the initialized firebase app instance.

    Raises:
        NotInitializedError: If the firebase SDK is not initialized yet.

    Returns:
        App: The firebase app instance.
    """
    raise NotInitializedError("The firebase application was not initialized.")


def _app_name(app: FastAPI):
    return f"fb_app_{hash(app)}"
