import pytest
from app import app, User
import json
from flask_login import FlaskLoginClient


app.test_client_class = FlaskLoginClient

client = app.test_client(user=User.get_by_id(1))


def test_create_user():
    # creates a user
    response = client.post(
        "/api/user",
        json={'username': 'test1', 'password': 'test1', 'admin': 'False'}
    )
    res = json.loads(response.data)
    assert 'User Created Successfully' in res['result']
    user_id = res['result'][-1]

    #  deletes a user
    response_delete = client.delete(
        f"/api/user?user_id={user_id}"
    )
    res = json.loads(response_delete.data)
    assert 'User Deleted Successfully' == res['result']


def test_user_already_created():
    name = "ron"
    # creates a user
    response_create = client.post(
        "/api/user",
        json={'username': name, 'password': 'test', 'admin': 'False'}
    )
    res = json.loads(response_create.data)
    assert 'User Created Successfully' in res['result']

    #  creates user with the same name
    user_id = res['result'][-1]
    response_create_duplicate = client.post(
        "/api/user",
        json={'username': name, 'password': '123', 'admin': 'False'}
    )
    res = json.loads(response_create_duplicate.data)
    assert 'User Already Exists' in res['result']

    #  deletes the user
    response_delete = client.delete(
        f"/api/user?user_id={user_id}"
    )
    res = json.loads(response_delete.data)
    assert 'User Deleted Successfully' == res['result']


def test_user_password_update():
    # creates a user
    response_create = client.post(
        "/api/user",
        json={'username': 'test9', 'password': 'test', 'admin': 'False'}
    )
    res = json.loads(response_create.data)
    assert 'User Created Successfully' in res['result']

    #  update password
    user_id = res['result'][-1]
    response_password_update = client.patch(
        "/api/user",
        json={'user_id': user_id, 'password': '123'}
    )
    res = json.loads(response_password_update.data)
    assert 'User Password Updated Successfully' in res['result']

    #  delete a user
    response_delete = client.delete(
        f"/api/user?user_id={user_id}"
    )
    res = json.loads(response_delete.data)
    assert 'User Deleted Successfully' == res['result']


def test_user_delete():
    #  create a user
    response_create = client.post(
        "/api/user",
        json={'username': 'test5', 'password': 'test', 'admin': 'False'}
    )
    res = json.loads(response_create.data)
    user_id = res['result'][-1]
    assert 'User Created Successfully' in res['result']

    #  delete a user
    response_delete = client.delete(
        f"/api/user?user_id={user_id}"
    )
    res = json.loads(response_delete.data)
    assert 'User Deleted Successfully' == res['result']


def test_note_actions():
    #  create users
    response = client.post(
        "/api/user",
        json={'username': 'test12', 'password': 'test1', 'admin': 'False'}
    )
    res = json.loads(response.data)
    user_id = res['result'][-1]
    assert 'User Created Successfully' in res['result']

    #  create post
    response = client.post(
        "/api/note",
        json={'text': 'some text', 'user_id': user_id}
    )
    res = json.loads(response.data)
    note_id = res['result'][-1]
    assert 'Note Created With id' in res['result']

    # update post
    response = client.patch(
        "/api/note",
        json={'text': 'some text', 'note_id': note_id}
    )
    res = json.loads(response.data)

    assert f'Note {note_id} Updated' in res['result']

    # delete post
    response = client.delete(
        f"/api/note?note_id={note_id}"
    )
    res = json.loads(response.data)
    assert f'Note {note_id} Deleted' in res['result']

#  deletes a user
    response_delete = client.delete(
        f"/api/user?user_id={user_id}"
    )
    res = json.loads(response_delete.data)
    assert 'User Deleted Successfully' == res['result']
