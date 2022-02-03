import typing
import logging
from fastapi import FastAPI
from firebase_admin import App, credentials, delete_app, initialize_app

log = logging.getLogger()


class FastapiFirebaseException(Exception):
    pass


class NotInitializedError(FastapiFirebaseException):
    pass


class InvalidCredentialsError(FastapiFirebaseException):
    pass


class CredentialsNotLoadedError(FastapiFirebaseException):
    pass


def setup_firebase(
    app: FastAPI,
    credential: typing.Union[str, dict, credentials.Base] = None,
    firebase_options: typing.Dict[str, typing.Any] = None,
):
    _app: App = None

    if isinstance(credential, (str, dict)):
        try:
            credential = credentials.Certificate(credential)
        except ValueError as ex:
            raise InvalidCredentialsError(*ex.args)
        except IOError as ex:
            raise CredentialsNotLoadedError(*ex.args)

    @app.on_event("startup")
    def _setup_app():
        nonlocal _app
        try:
            _app = initialize_app(credential, firebase_options, _app_name(app))
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
            raise


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
