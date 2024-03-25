from app import app
import json



def test_create_user():
    # creates a user
    response = app.test_client().post(
        "/api/user",
        json=json.dumps({'username':'test1','password':'test1'})
    )
    res = json.loads(response.data)
    assert 'User Created Succesfully' in res
    user_id = res[-1]

    #  deletes a user
    response_delete = app.test_client().delete(
        "/api/user",
        json=json.dumps({'user_id':user_id})
    )
    res = json.loads(response_delete.data)
    assert 'User Deleted Succesfully' == res



def test_user_already_created():
    name = "ron"
    # creates a user
    response_create = app.test_client().post(
        "/api/user",
        json=json.dumps({'username':name,'password':'test'})
    )
    res = json.loads(response_create.data)
    assert 'User Created Succesfully' in res
    
    #  creates user with the same name
    user_id = res[-1]
    response_create_dupliate = app.test_client().post(
        "/api/user",
        json=json.dumps({'username':name,'password':'123'})
    )
    res = json.loads(response_create_dupliate.data)
    assert 'User Already Exists' in res
    
    #  deletes the user
    response_delete = app.test_client().delete(
        "/api/user",
        json=json.dumps({'user_id':user_id})
    )
    res = json.loads(response_delete.data)
    assert 'User Deleted Succesfully' == res


def test_user_password_update():
    # creates a user
    response_create = app.test_client().post(
        "/api/user",
        json=json.dumps({'username':'test9','password':'test'})
    )
    res = json.loads(response_create.data)
    assert 'User Created Succesfully' in res
    
    #  update password
    user_id = res[-1]
    response_password_update = app.test_client().patch(
        "/api/user",
        json=json.dumps({'user_id':user_id,'password':'123'})
    )
    res = json.loads(response_password_update.data)
    assert 'User Password Updated Succesfully' in res

    #  delete a user
    response_delete = app.test_client().delete(
        "/api/user",
        json=json.dumps({'user_id':user_id})
    )
    res = json.loads(response_delete.data)
    assert 'User Deleted Succesfully' == res



def test_user_delete():
    #  create a user
    response_create = app.test_client().post(
        "/api/user",
        json=json.dumps({'username':'test5','password':'test'})
    )
    res = json.loads(response_create.data)
    user_id = res[-1]
    assert 'User Created Succesfully' in res

    #  delete a user
    response_delete = app.test_client().delete(
        "/api/user",
        json=json.dumps({'user_id':user_id})
    )
    res = json.loads(response_delete.data)
    assert 'User Deleted Succesfully' == res

def test_task_actions():
    #  create user
    response = app.test_client().post(
        "/api/user",
        json=json.dumps({'username':'test10','password':'test1'})
    )
    res = json.loads(response.data)
    user_id = res[-1]
    assert 'User Created Succesfully' in res

    #  create post
    response = app.test_client().post(
        "/api/task",
        json=json.dumps({'text':'some text','user_id':user_id})
    )
    res = json.loads(response.data)
    task_id = res[-1]
    assert 'Task Created With id' in res

    # update post
    response = app.test_client().patch(
        "/api/task",
        json=json.dumps({'text':'some text','task_id':task_id})
    )
    res = json.loads(response.data)
    
    assert f'Task {task_id} Updated' in res

    # delete post
    response = app.test_client().delete(
        "/api/task",
        json=json.dumps({'task_id':task_id})
    )
    res = json.loads(response.data)
    assert f'Task {task_id} Deleted' in res

#  deletes a user
    response_delete = app.test_client().delete(
        "/api/user",
        json=json.dumps({'user_id':user_id})
    )
    res = json.loads(response_delete.data)
    assert 'User Deleted Succesfully' == res