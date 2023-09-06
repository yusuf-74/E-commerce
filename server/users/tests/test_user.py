import pytest
from ..models import User 

pytestmark = pytest.mark.django_db

class TestUser:
    def test_user_model(self):
        user = User.objects.create_user(username="testuser",password="hommos123", email="test@app.com")
        
        assert user.username == "testuser"
        assert user.email == "test@app.com"
        assert user.is_staff == False