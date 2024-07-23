from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from fast_zero.app import app


@pytest.fixture()
def client():
    return TestClient(app)


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={'username': 'junin', 'email': 'junin@example.com', 'password': 'pwd'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'username': 'junin', 'email': 'junin@example.com'}


def test_list_user(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [{'username': 'junin', 'email': 'junin@example.com'}]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={'username': 'update', 'email': 'update@example.com', 'password': 'psw'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'update',
        'email': 'update@example.com',
    }


def test_update_user_not_found(client):
    response = client.put(
        '/users/100',
        json={'username': 'update', 'email': 'update@example.com', 'password': 'psw'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        'detail': 'User not found',
    }


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/users/100')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
