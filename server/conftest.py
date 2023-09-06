import pytest
from rest_framework.test import APIClient
from users.models import User


@pytest.fixture
def user():
    return User.objects.create_user("test_username", "test@user.app", "test_password")


@pytest.fixture
def auth_client(user):
    pass

@pytest.fixture
def client(user):
    return APIClient()