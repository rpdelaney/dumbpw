import pytest


@pytest.fixture
def fake_secrets(mocker):
    return mocker.patch("secrets")
