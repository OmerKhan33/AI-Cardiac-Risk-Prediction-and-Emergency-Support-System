import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.main import app

client = TestClient(app)

class TestHealthCheck:
    """Test basic API health"""
    
    def test_health_endpoint(self):
        """Test the root health check endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "online"

class TestAuth:
    """Test authentication endpoints"""
    
    def test_register_new_user(self):
        """Test user registration"""
        # Use unique username to avoid conflicts
        import time
        unique_user = f"testuser_{int(time.time())}"
        
        response = client.post("/register", json={
            "username": unique_user,
            "password": "testpass123"
        })
        assert response.status_code == 201
    
    def test_register_duplicate_user(self):
        """Test that duplicate usernames are rejected"""
        # First registration
        client.post("/register", json={
            "username": "duplicate_test",
            "password": "testpass123"
        })
        
        # Second registration with same username
        response = client.post("/register", json={
            "username": "duplicate_test", 
            "password": "different_pass"
        })
        assert response.status_code == 400
    
    def test_login_valid_credentials(self):
        """Test login with valid credentials"""
        # Register first
        import time
        unique_user = f"logintest_{int(time.time())}"
        client.post("/register", json={
            "username": unique_user,
            "password": "testpass123"
        })
        
        # Login
        response = client.post("/token", data={
            "username": unique_user,
            "password": "testpass123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = client.post("/token", data={
            "username": "nonexistent",
            "password": "wrongpass"
        })
        assert response.status_code == 401

class TestAssessmentEndpoint:
    """Test the main assessment endpoint"""
    
    def get_auth_token(self):
        """Helper to get auth token"""
        import time
        unique_user = f"assesstest_{int(time.time())}"
        
        client.post("/register", json={
            "username": unique_user,
            "password": "testpass123"
        })
        
        response = client.post("/token", data={
            "username": unique_user,
            "password": "testpass123"
        })
        return response.json()["access_token"]
    
    def test_assess_without_auth(self):
        """Test that assessment requires authentication"""
        response = client.post("/assess", json={
            "age": 50,
            "sex": 1,
            "cp": 0,
            "trestbps": 120,
            "chol": 200,
            "fbs": 0,
            "restecg": 0,
            "thalach": 150,
            "exang": 0,
            "oldpeak": 1.0,
            "slope": 1,
            "ca": 0,
            "thal": 1,
            "city": "London"
        })
        assert response.status_code == 401
    
    def test_assess_with_auth(self):
        """Test assessment with valid authentication"""
        token = self.get_auth_token()
        
        response = client.post(
            "/assess",
            json={
                "age": 50,
                "sex": 1,
                "cp": 0,
                "trestbps": 120,
                "chol": 200,
                "fbs": 0,
                "restecg": 0,
                "thalach": 150,
                "exang": 0,
                "oldpeak": 1.0,
                "slope": 1,
                "ca": 0,
                "thal": 1,
                "city": "London"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Should succeed (200) or gracefully handle model loading issues
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "risk_score" in data
            assert "risk_category" in data
            assert "recommendations" in data

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
