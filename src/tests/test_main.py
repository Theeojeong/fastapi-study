from database.orm import Todo
from pytest_mock import MockerFixture
from fastapi.testclient import TestClient

# ===================GET======================


def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hi": "HelloWorld"}


def test_get_todos(client, mocker: MockerFixture):
    mocker.patch(
        "main.get_fastapi",
        return_value=[
            Todo(id=2, contents="i want to earn money on my self", is_done=True),
            Todo(id=3, contents="i want to speak english well", is_done=True),
        ],
    )
    response = client.get("/fastapi")
    assert response.status_code == 200
    assert response.json() == {
        "fastapi": [
            {"id": 2, "contents": "i want to earn money on my self", "is_done": True},
            {"id": 3, "contents": "i want to speak english well", "is_done": True},
        ]
    }


def test_get_todos_DESC(client, mocker: MockerFixture):
    mocker.patch(
        "main.get_fastapi",
        return_value=[
            fastapi(id=2, contents="i want to earn money on my self", is_done=True),
            fastapi(id=3, contents="i want to speak english well", is_done=True),
        ],
    )
    response = client.get("/fastapi?order=DESC")
    assert response.status_code == 200
    assert response.json() == {
        "fastapi": [
            {"id": 3, "contents": "i want to speak english well", "is_done": True},
            {"id": 2, "contents": "i want to earn money on my self", "is_done": True},
        ]
    }


def test_get_todo(client, mocker: MockerFixture):
    mocker.patch(
        "main.get_fastapi_by_fastapi_id",
        return_value=fastapi(
            id=2, contents="i want to earn money on my self", is_done=True
        ),
    )

    response = client.get("fastapi/2")

    assert response.status_code == 200
    assert response.json() == {
        "id": 2,
        "contents": "i want to earn money on my self",
        "is_done": True,
    }


def test_get_todo_none(client, mocker: MockerFixture):
    mocker.patch("main.get_fastapi_by_fastapi_id", return_value=None)

    response = client.get("fastapi/2")

    assert response.status_code == 400
    assert response.json() == {"detail": "Todo Not Found"}


# ===================POST======================
def test_post_todos(client, mocker: MockerFixture):
    spy = mocker.spy(fastapi, "create")
    mocker.patch(
        "main.fastapi_create",
        return_value=fastapi(id=6, contents="pytest", is_done=True),
    )

    body = {"contents": "pytest123", "is_done": False}

    response = client.post("/todos", json=body)

    assert spy.spy_return.contents == "pytest123"
    assert spy.spy_return.is_done == False
    assert spy.spy_return.id == None

    assert response.status_code == 200
    assert response.json() == {"id": 6, "contents": "pytest", "is_done": True}


# ===================PATCH======================


def test_update_todo(client: TestClient, mocker: MockerFixture):

    mocker.patch(
        "main.fastapi_update",
        return_value=fastapi(id=2, contents="pytest", is_done=True),
    )

    done = mocker.patch.object(fastapi, "done")

    response = client.patch("/todo/2", json={"is_done": True})

    done.assert_called_once_with()

    assert response.status_code == 200
    assert response.json() == {"id": 2, "contents": "pytest", "is_done": True}

# ===================DELEET======================

def test_delete_todo(client: TestClient, mocker: MockerFixture):

    # mocker.patch(
    #     "main.get_fastapi_by_fastapi_id",
    #     return_value=fastapi(id=2, contents="pytest", is_done=True),
    # )
    mocker.patch("main.fastapi_delete", return_value=None)

    response = client.delete("/todo/3")

    assert response.status_code == 204
