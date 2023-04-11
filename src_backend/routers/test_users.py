import json
import pytest

pytestmark = pytest.mark.anyio


# Tests for GET /users

class TestGetUsers:
    # TODO write tests

    # test get users
    # add new user, test get users
    async def test_get_users(self, client, adminClient):

        # Add a new user
        add_new_user = {
        'email': 'newuser@email.com',
        'password': 'newuserpassword'
        }
        response = await client.post("/users", json=add_new_user)
        assert response.status_code == 200

        # Get users
        response = await adminClient.get('/users')
        assert response.status_code == 200

        # Check number of users > 0
        all_users = json.loads(response.content)
        assert len(all_users)>0

        # Check if correct user was added to emails 
        all_emails = [user['email'] for user in all_users]
        assert add_new_user['email'] in all_emails


    # add a few users, test pagination
    async def test_pagination(self, client, adminClient):

        # Add some users for testing
        new_users = [
            {'email': 'email@email.com', 'password': 'password'},
            {'email': 'email1@email.com', 'password': 'password1'},
            {'email': 'email2@email.com', 'password': 'password2'},
            {'email': 'email3@email.com', 'password': 'password3'},
            {'email': 'email4@email.com', 'password': 'password4'},
            {'email': 'email5@email.com', 'password': 'password5'},
            {'email': 'email6@email.com', 'password': 'password6'},
            {'email': 'email7@email.com', 'password': 'password7'},
            {'email': 'email8@email.com', 'password': 'password8'},
            {'email': 'email9@email.com', 'password': 'password9'},
        ]
        for user in new_users:
            response = await client.post('/users', json=user)
            assert response.status_code == 200
            assert 'access_token' in response.json()

        # Test pagination with valid values
        response = await adminClient.get('/users?page=1&per_page=1')
        assert response.status_code == 200

        # Test first page 
        response = await adminClient.get('/users', params={'per_page': 10, 'page': 1})
        assert response.status_code == 200
        # 10 users per page
        assert len(response.json()) == 10
        # Check users = 10 new users + adminClient + client
        assert response.headers['X-Total-Count'] == '12'
        
        # Test second page (empty)
        response = await adminClient.get('/users', params={'per_page': 10, 'page': 2})
        assert response.status_code == 200
        # Remaining two users on page
        assert len(response.json()) == 2
        assert response.headers['X-Total-Count'] == '12'

        # Test tird page 
        # test pagination with page > number of pages
        response = await adminClient.get('/users', params={'per_page': 10, 'page': 3})
        assert response.status_code == 200
        # No users on page
        assert len(response.json()) == 0
        assert response.headers['X-Total-Count'] == '12'

        # test pagination with invalid values
        response = await adminClient.get("/users", params={"per_page": -1, "page": 0})
        assert response.status_code == 200
        # Defaults to minimum

    # async def test_admin(self, client, adminClient):

        # add new user and some projects, test get users with additional data as admin
        # Add a new user
            #add_new_user = {
             #   'email': 'newuser@email.com',
                #  'password': 'newuserpassword'
                #}
            #response = await client.post('/users', json=add_new_user)
            #assert response.status_code == 200
            #access_token = response.json()['access_token']
            #assert response.status_code == 200

        # Add  some projects
            #project_data = {
            #     'title': 'Project',
            #     'link': 'http://github.com',
            #     'completionDate': '2023-04-11',
            #     'description': 'Test project to test users',
            #     'content': 'Content content content'
            # }
            # headers = { 'Authorization': 'Bearer newuser@email.com' } 
            # response = await client.post('/projects', headers=headers, data= project_data)
            # assert response.status_code == 200
            # project_id = response.json()['id']

            # # Check project params are ok
            # response = await adminClient.get(f'/projects')
            # assert response.status_code == 200
            # assert response.json()['title'] == 'Project'
            # assert response.json()['link'] == 'http://github.com'
            # assert response.json()['completionDate'] == '2023-04-11'
            # assert response.json()['description'] == 'Test project to test users'
            # assert response.json()['content'] == 'Content content content'
            # assert len(response.json()['tags']) == 3

    # test get users with additional data as regular user (should fail and return 403)
    # test get users with additional data without logging in (should fail and return 401)


# Tests for GET /users/{id}

class TestGetUsersId:
    pass
    # TODO write tests
    # test get a different user as admin
    # test get self as admin
    # test get self as user
    # test get a different user as user (should fail and return 403)
    # test get user without logging in (should fail and return 401)
    # test get user with invalid id (should fail and return 404)


# Tests for POST /users

class TestPostUsers:
    pass
    # TODO write tests


# Tests for PATCH /users/{id}

class TestPatchUsersId:
    pass
    # TODO write tests


# Tests for DELETE /users/{id}

class TestDeleteUsersId:
    pass
    # TODO write tests
    
    async def test_deleting_users(self, client, adminClient, userClient):
        # test delete a different user as admin

        # Add a new user
        add_new_user = {
        'email': 'newuser@email.com',
        'password': 'newuserpassword'
        }

        response = await adminClient.post('/users', json=add_new_user)
        assert response.status_code == 200
        user_id = str(response.json()['id'])
        assert response.status_code == 200

        # delete another user by admin
        response = await adminClient.delete(f'/users/{user_id}')
        assert response.status_code == 204

        # test delete user with invalid id (should fail and return 404)
        user_id1 = 'f0f75371-e71f-41ae-a28b-f1956c14f829' # random uuid
        response  = await adminClient.delete(f'/users/{user_id1}')
        assert response.status_code == 404

        # test delete a different user as user (should fail and return 403)
        response = await userClient.delete(f'/users/{user_id}')
        assert response.status_code == 403

        # test delete user without logging in (should fail and return 401)
        response = await client.delete(f'/users/{user_id}')
        assert response.status_code == 401 

        # Delete yourself as admin
        #admin_id = '170b76ca-9cdb-4d3b-af35-f3c0202d7357'
        #response = await adminClient.delete(f'/users/{admin_id}')
        #assert response.status_code == 400 or response.status_code == 422

        # test delete self as user
        userClient_id = 'ec33e02c-ec82-4f4d-88be-23b2cdb6f097'
        response = await userClient.delete(f'/users/{userClient_id}')
        assert response.status_code == 204

        # test delete cascade behaviour (deleting a user should delete all associated projects)