from unittest import mock

from fastapi.security.http import HTTPAuthorizationCredentials

from fastapi_firebase.auth import validate_token


@mock.patch("firebase_admin.auth.verify_id_token")
def test_verifies_token(verify: mock.Mock):
    credential = HTTPAuthorizationCredentials(credentials="mytoken", scheme="bearer")
    mocked_app = mock.Mock()
    fake = {"id": "myId"}
    verify.return_value = fake
    result = validate_token(credential, mocked_app)
    assert result == fake
