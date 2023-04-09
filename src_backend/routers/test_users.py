import pytest

pytestmark = pytest.mark.anyio


# Tests for GET /users

class TestGetUsers:
    pass
    # TODO write tests
    # test get users
    # add new user, test get users
    # add a few users, test pagination
    # test pagination with page > number of pages
    # test pagination with invalid values
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