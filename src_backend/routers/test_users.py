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
        # response = await adminClient.get("/users", params={"per_page": -1, "page": 0})
        # assert response.status_code == 422
        # PROBLEM HERE

        # response = await adminClient.get("/users", params={"per_page": 10, "page": 0})
        # assert response.status_code == 422
        # PROBLEM HERE

        # response = await adminClient.get("/users", params={"per_page": 10, "page": -1})
        # assert response.status_code == 422
        # PROBLEM HERE 



    # add new user and some projects, test get users with additional data as admin
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
    # test delete a different user as admin
    # test delete self as admin (should fail and return 400 or 422)
    # test delete self as user
    # test delete a different user as user (should fail and return 403)
    # test delete user without logging in (should fail and return 401)
    # test delete user with invalid id (should fail and return 404)
    # test delete cascade behaviour (deleting a user should delete all associated projects)