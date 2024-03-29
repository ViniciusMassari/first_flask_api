import pytest
import requests


BASE_URL = "http://127.0.0.1:5000"

TASK_ID = 1


def test_create_task_endpoint():
    new_task_data = {
        "title": "Nova tarefa",
        "description": "Descrição"
    }

    response = requests.post(f"{BASE_URL}/criar_task", json=new_task_data)
    assert response.status_code == 201
    response_json = response.json()
    assert "message" in response_json
    assert "id" in response_json


def test_get_tasks():
    response = requests.get(BASE_URL + "/tasks")
    assert response.status_code == 200
    response_json = response.json()
    assert "tasks" in response_json
    assert "total_tasks" in response_json


def test_get_task():
    response = requests.get(BASE_URL + f"/task/{TASK_ID}")
    assert response.status_code == 200
    response_json = response.json()

    assert "title" in response_json
    assert "id" in response_json
    assert response_json['id'] == TASK_ID


def test_update_task():

    payload = {
        "completed": True,
        "description": "Nova descrição",
        "title": "Título atualizado"
    }
    response = requests.put(f"{BASE_URL}/task/{TASK_ID}", json=payload)
    assert response.status_code == 200
    response_json = response.json()
    assert "message" in response_json

    # Nova requisição a tarefa especifica
    response = requests.get(f"{BASE_URL}/task/{TASK_ID}")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["title"] == payload["title"]
    assert response_json["description"] == payload["description"]
    assert response_json["completed"] == payload["completed"]


def test_delete_task():
    response = requests.delete(f"{BASE_URL}/task/{TASK_ID}")
    assert response.status_code == 200
    response = requests.get(f"{BASE_URL}/task/{TASK_ID}")
    assert response.status_code == 404
