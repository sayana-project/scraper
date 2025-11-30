# Test simple de l'API
from src.api.app import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_health():
    """Test de l'endpoint health"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
    print("Test health endpoint OK")

if __name__ == "__main__":
    test_health()
    print("Tous les tests de base passes !")