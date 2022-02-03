import typing
from unittest import mock

import firebase_admin
import pytest
from fastapi import Depends, FastAPI, testclient

from fastapi_firebase import app as fire


@pytest.fixture()
def app():
    _app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

    @_app.get("/")
    def read_app(app: firebase_admin.App = Depends(fire.firebase_app)):
        return app.name

    return _app


@pytest.fixture()
def client(app: FastAPI):
    return testclient.TestClient(app)


def test_app_dep_uninitialized(client: testclient.TestClient):
    with client:
        with pytest.raises(fire.NotInitializedError):
            client.get("/")


def test_initialized(client: testclient.TestClient, app: FastAPI):
    fire.setup_firebase(app)

    with client:
        response = client.get("/")

    assert response.json() == fire._app_name(app)


@pytest.mark.parametrize("credential_data", ("./cert.json", {"test": "hello"}))
@mock.patch("firebase_admin.credentials.Certificate")
def test_setup_succeeds(certificate, app: FastAPI, client: testclient.TestClient, credential_data):
    fire.setup_firebase(app, credential_data)
    certificate.assert_called_with(credential_data)


@pytest.mark.parametrize(
    "credential_data,exc_class,raised_exc,",
    (
        ("./cert.json", IOError, fire.CredentialsNotLoadedError),
        ({"test": "hello"}, ValueError, fire.InvalidCredentialsError),
    ),
)
@mock.patch("firebase_admin.credentials.Certificate")
def test_setup_raises_invalid_credentials(
    certificate: mock.Mock,
    app: FastAPI,
    client: testclient.TestClient,
    credential_data,
    exc_class: typing.Type[Exception],
    raised_exc: typing.Type[Exception],
):
    certificate.side_effect = exc_class
    with pytest.raises(raised_exc):
        fire.setup_firebase(app, credential_data)


@mock.patch("fastapi_firebase.app.initialize_app")
def test_failed_initialize(initialize: mock.Mock, app: app, client: testclient.TestClient):
    initialize.side_effect = ValueError
    fire.setup_firebase(app)

    with pytest.raises(ValueError):
        with client:
            initialize.assert_called()


@mock.patch("fastapi_firebase.app.delete_app")
def test_failed_delete(delete: mock.Mock, app: app, client: testclient.TestClient):
    delete.side_effect = ValueError()
    fire.setup_firebase(app)

    with pytest.raises(ValueError):
        with client:
            delete.assert_not_called()


def test_not_initialized():
    with pytest.raises(fire.NotInitializedError):
        fire.firebase_app()
