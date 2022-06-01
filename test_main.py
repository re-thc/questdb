from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_get_wrong_id():
    response = client.get("/questdb/06bd09bc-a617-4863-be37-3dbd07a5d990")
    assert response.status_code == 404
    assert response.json() == {"detail": "QuestDB instance not found"}

def test_full_cycle():
    response = client.post("/questdb")
    assert response.status_code == 200
    instance_id = response.json()["id"]
    response = client.get("/questdb/" + instance_id)
    assert response.status_code == 200
    assert response.json() == {"id": {}}
    response = client.delete("/questdb/" + instance_id)
    assert response.status_code == 200
    assert response.json() == {"ok": True}
    response = client.get("/questdb/" + instance_id)
    assert response.status_code == 404
    assert response.json() == {"detail": "QuestDB instance not found"}