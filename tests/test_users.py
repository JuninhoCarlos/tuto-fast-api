from http import HTTPStatus

from fast_zero.schemas import UserSchemaPublic


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
    assert response.json() == {'users': []}


def test_list_users_with_users(client, user):
    user_schema = UserSchemaPublic.model_validate(user).model_dump()

    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
        json={'username': 'update', 'email': 'update@example.com', 'password': 'psw'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'update',
        'email': 'update@example.com',
    }


def test_update_user_not_found(client, token):
    response = client.put(
        '/users/100',
        headers={'Authorization': f'Bearer {token}'},
        json={'username': 'update', 'email': 'update@example.com', 'password': 'psw'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_delete_user(client, user, token):
    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client, token):
    response = client.delete('/users/100', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user_wrong_user(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
