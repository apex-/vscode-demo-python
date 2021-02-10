import json

import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api import app

client = TestClient(app)
__TASK_ID = None

def test_create_task():
    global __TASK_ID
    payload = {
        "title": "some task",
        "description": "pytest task",
        "done": False
    }
    response = client.post("/tasks", json.dumps(payload))
    assert response.status_code == 201
    response_json = response.json()
    assert response_json["title"] == payload["title"]
    assert response_json["description"] == payload["description"]
    assert response_json["done"] == payload["done"]
    assert response_json["id"] >= 1
    __TASK_ID = response_json["id"]

@pytest.mark.depends(on=['test_create_task'])
def test_list_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json) == 1

@pytest.mark.depends(on=['test_create_task'])
def test_update_task():
    global __TASK_ID
    payload = {
        "title": "some task updated",
        "description": "pytest task updated",
        "done": True
    }
    response = client.put(f"/task/{__TASK_ID}", json.dumps(payload))
    assert response.status_code == 200
    response_json = response.json()
    response_json = response.json()
    assert response_json["title"] == payload["title"]
    assert response_json["description"] == payload["description"]
    assert response_json["done"] == payload["done"]
    assert response_json["id"] == __TASK_ID
