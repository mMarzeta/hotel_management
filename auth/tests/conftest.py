from fastapi import FastAPI
from starlette.testclient import TestClient

from endpoints import app

import pytest
import mock
from models import UserModel
import datetime


@pytest.fixture(scope="function")
def client():
    yield TestClient(app)


@pytest.fixture(scope="function")
def fixed_uuid():
    return "4615367b-063d-4487-bbe3-694877695bf0"


@pytest.fixture(scope="function")
def sample_user(fixed_uuid):
    return UserModel(
        id=fixed_uuid,
        username="test_user",
        email="test@email.com",
        tel_number="123123123",
        full_name="John Doe",
        pesel="12013020102",
        address="Main St. 1, 12-123 London",
        hashed_password="hashed password",
        disabled=False,
        created_at=datetime.datetime.strptime("01-01-2020 12:00", format="%d-%m-%y %h:%m")
    )


def mock_get_user(mocker, sample_user):
    user_mock = mock.MagicMock()
    user_mock.get_user = mock.MagicMock(return_value=sample_user)

    return mocker.patch(
        target="oauth2.UserModel",
        new=user_mock
    )
