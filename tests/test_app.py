import pytest
from fastapi import Depends, FastAPI, testclient
from firebase_admin import App, _DEFAULT_APP_NAME

from fastapi_firebase import app as fire


@pytest.fixture()
def app():
    _app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

    @_app.get("/")
    def read_app(app: App = Depends(fire.firebase_app)):
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
    fire.setup(app)

    with client:
        response = client.get("/")

    assert response.json() == fire._app_name(app)
