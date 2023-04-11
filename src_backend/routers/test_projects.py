import pytest

pytestmark = pytest.mark.anyio


async def setup_project_request_data(adminClient) -> dict[str, str]:
    response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
    assert response.status_code == 200
    cat1Id = (response.json())['categoryId']
    assert cat1Id
    response = await adminClient.post('/tags', 
        json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
    assert response.status_code == 200
    tag1Id = (response.json())['tagId']
    assert tag1Id
    response = await adminClient.post('/tags', 
        json={ "tagName": "tag2", "tagNameShort": "tag2s", "categoryId": cat1Id })
    assert response.status_code == 200
    tag2Id = (response.json())['tagId']
    assert tag2Id
    response = await adminClient.post('/tags', 
        json={ "tagName": "tag3", "tagNameShort": "tag3s", "categoryId": cat1Id })
    assert response.status_code == 200
    tag3Id = (response.json())['tagId']
    assert tag3Id

    request_data = {
        'title': 'title1',
        'link': 'https://example.com',
        'completionDate': '2011-10-05T14:48:00.000Z',
        'description': 'description1',
        'content': 'content1',
        'tags': f'{tag2Id}, {tag3Id}, {tag1Id}'
    }

    return request_data


# Tests for GET /projects/{id}

class TestGetProjectsId:

    async def test_not_found_invalid_uuid(self, client, userClient, adminClient):
        # TEST
        response = await client.get('/projects/invaliduuid')
        assert response.status_code == 404
        response = await userClient.get('/projects/invaliduuid')
        assert response.status_code == 404
        response = await adminClient.get('/projects/invaliduuid')
        assert response.status_code == 404

    async def test_not_found_valid_uuid(self, client, userClient, adminClient):
        # TEST
        response = await client.get('/projects/f8c1147d-b1c0-4dbb-b4c2-7191ff78ac99')
        assert response.status_code == 404
        response = await userClient.get('/projects/f8c1147d-b1c0-4dbb-b4c2-7191ff78ac99')
        assert response.status_code == 404
        response = await adminClient.get('/projects/f8c1147d-b1c0-4dbb-b4c2-7191ff78ac99')
        assert response.status_code == 404

    async def test_live_no_additional_info(self, client, userClient, adminClient):
        # PRECONDITIONS
        request_data = await setup_project_request_data(adminClient)
        response = await adminClient.post('/projects', data=request_data)
        assert response.status_code == 200
        projectId = (response.json())['id']
        assert projectId
        response = await adminClient.patch(f'/projects/{projectId}', data={ 'is_live': True })
        assert response.status_code == 200

        # TEST
        expected_response_body = {
            'id': projectId,
            'title': 'title1',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': [
                {'tagId': 1, 'tagName': 'tag1', 'tagNameShort': 'tag1s', 'categoryId': 1}, 
                {'tagId': 2, 'tagName': 'tag2', 'tagNameShort': 'tag2s', 'categoryId': 1}, 
                {'tagId': 3, 'tagName': 'tag3', 'tagNameShort': 'tag3s', 'categoryId': 1}
            ]
        }

        response = await client.get(f'/projects/{projectId}')
        assert response.status_code == 200
        assert response.json() == expected_response_body

        response = await userClient.get(f'/projects/{projectId}')
        assert response.status_code == 200
        assert response.json() == expected_response_body

        response = await adminClient.get(f'/projects/{projectId}')
        assert response.status_code == 200
        assert response.json() == expected_response_body

    async def test_live_additional_info_as_anon(self, client, userClient, adminClient):
        # PRECONDITIONS
        request_data = await setup_project_request_data(adminClient)
        response = await adminClient.post('/projects', data=request_data)
        assert response.status_code == 200
        projectId = (response.json())['id']
        assert projectId
        response = await adminClient.patch(f'/projects/{projectId}', data={ 'is_live': True })
        assert response.status_code == 200

        # TEST
        request_params = { 'additional_info': True }
        response = await client.get(f'/projects/{projectId}', params=request_params)
        assert response.status_code == 401

    async def test_live_additional_info_as_user(self, userClient, adminClient):
        # PRECONDITIONS
        request_data = await setup_project_request_data(adminClient)
        response = await adminClient.post('/projects', data=request_data)
        assert response.status_code == 200
        projectId = (response.json())['id']
        assert projectId
        response = await adminClient.patch(f'/projects/{projectId}', data={ 'is_live': True })
        assert response.status_code == 200

        # TEST
        request_params = { 'additional_info': True }
        response = await userClient.get(f'/projects/{projectId}', params=request_params)
        assert response.status_code == 403

    async def test_live_additional_info_as_user_self(self, userClient, adminClient):
        # PRECONDITIONS
        request_data = await setup_project_request_data(adminClient)
        response = await userClient.post('/projects', data=request_data)
        assert response.status_code == 200
        projectId = (response.json())['id']
        assert projectId
        response = await adminClient.patch(f'/projects/{projectId}', data={ 'is_live': True })
        assert response.status_code == 200

        # TEST
        request_params = { 'additional_info': True }
        response = await userClient.get(f'/projects/{projectId}', params=request_params)
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': [
                {'tagId': 1, 'tagName': 'tag1', 'tagNameShort': 'tag1s', 'categoryId': 1}, 
                {'tagId': 2, 'tagName': 'tag2', 'tagNameShort': 'tag2s', 'categoryId': 1}, 
                {'tagId': 3, 'tagName': 'tag3', 'tagNameShort': 'tag3s', 'categoryId': 1}
            ],
            'is_live': True
        }
        assert response.json() == expected_response_body

    async def test_live_additional_info_as_admin(self, adminClient, userClient):
        # PRECONDITIONS
        request_data = await setup_project_request_data(adminClient)
        response = await userClient.post('/projects', data=request_data)
        assert response.status_code == 200
        projectId = (response.json())['id']
        assert projectId
        response = await adminClient.patch(f'/projects/{projectId}', data={ 'is_live': True })
        assert response.status_code == 200

        # TEST
        request_params = { 'additional_info': True }
        response = await adminClient.get(f'/projects/{projectId}', params=request_params)
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': [
                {'tagId': 1, 'tagName': 'tag1', 'tagNameShort': 'tag1s', 'categoryId': 1}, 
                {'tagId': 2, 'tagName': 'tag2', 'tagNameShort': 'tag2s', 'categoryId': 1}, 
                {'tagId': 3, 'tagName': 'tag3', 'tagNameShort': 'tag3s', 'categoryId': 1}
            ],
            'is_live': True,
            'user': {
                'email': 'user@user.com',
                'id': 'ec33e02c-ec82-4f4d-88be-23b2cdb6f097'
            },
            'visit_count': 0
        }
        assert response.json() == expected_response_body

    async def test_not_live_as_anon(self, client, adminClient):
        # PRECONDITIONS
        request_data = await setup_project_request_data(adminClient)
        response = await adminClient.post('/projects', data=request_data)
        assert response.status_code == 200
        projectId = (response.json())['id']
        assert projectId

        # TEST
        response = await client.get(f'/projects/{projectId}')
        assert response.status_code == 401

    async def test_not_live_as_user(self, userClient, adminClient):
        # PRECONDITIONS
        request_data = await setup_project_request_data(adminClient)
        response = await adminClient.post('/projects', data=request_data)
        assert response.status_code == 200
        projectId = (response.json())['id']
        assert projectId

        # TEST
        response = await userClient.get(f'/projects/{projectId}')
        assert response.status_code == 403

    async def test_not_live_as_user_self(self, userClient, adminClient):
        # PRECONDITIONS
        request_data = await setup_project_request_data(adminClient)
        response = await userClient.post('/projects', data=request_data)
        assert response.status_code == 200
        projectId = (response.json())['id']
        assert projectId

        # TEST
        response = await userClient.get(f'/projects/{projectId}')
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': [
                {'tagId': 1, 'tagName': 'tag1', 'tagNameShort': 'tag1s', 'categoryId': 1}, 
                {'tagId': 2, 'tagName': 'tag2', 'tagNameShort': 'tag2s', 'categoryId': 1}, 
                {'tagId': 3, 'tagName': 'tag3', 'tagNameShort': 'tag3s', 'categoryId': 1}
            ]
        }
        assert response.json() == expected_response_body

    async def test_not_live_as_admin(self, adminClient, userClient):
        # PRECONDITIONS
        request_data = await setup_project_request_data(adminClient)
        response = await userClient.post('/projects', data=request_data)
        assert response.status_code == 200
        projectId = (response.json())['id']
        assert projectId

        # TEST
        response = await adminClient.get(f'/projects/{projectId}')
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': [
                {'tagId': 1, 'tagName': 'tag1', 'tagNameShort': 'tag1s', 'categoryId': 1}, 
                {'tagId': 2, 'tagName': 'tag2', 'tagNameShort': 'tag2s', 'categoryId': 1}, 
                {'tagId': 3, 'tagName': 'tag3', 'tagNameShort': 'tag3s', 'categoryId': 1}
            ]
        }
        assert response.json() == expected_response_body


# Tests for POST /projects

class TestPostProjects:
    
    async def test_as_anon(self, client, adminClient):
        # PRECONDITIONS
        request_data = await setup_project_request_data(adminClient)

        # TEST
        response = await client.post('/projects', data=request_data)
        assert response.status_code == 401

    async def test_as_user(self, userClient, adminClient):
        # PRECONDITIONS
        request_data = await setup_project_request_data(adminClient)

        # TEST
        response = await userClient.post('/projects', data=request_data)
        assert response.status_code == 200
        projectId = (response.json())['id']
        assert projectId

        # POSTCONDITIONS
        response = await adminClient.get(f'/projects/{projectId}', params={ 'additional_info': True })
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': [
                {'categoryId': 1, 'tagId': 1, 'tagName': 'tag1', 'tagNameShort': 'tag1s'}, 
                {'categoryId': 1, 'tagId': 2, 'tagName': 'tag2', 'tagNameShort': 'tag2s'}, 
                {'categoryId': 1, 'tagId': 3, 'tagName': 'tag3', 'tagNameShort': 'tag3s'}
            ],
            'is_live': False,
            'user': {
                'email': 'user@user.com',
                'id': 'ec33e02c-ec82-4f4d-88be-23b2cdb6f097'
            },
            'visit_count': 0
        }
        assert response.json() == expected_response_body

    async def test_as_admin(self, adminClient):
        # PRECONDITIONS
        request_data = await setup_project_request_data(adminClient)

        # TEST
        response = await adminClient.post('/projects', data=request_data)
        assert response.status_code == 200
        projectId = (response.json())['id']
        assert projectId

        # POSTCONDITIONS
        response = await adminClient.get(f'/projects/{projectId}', params={ 'additional_info': True })
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': [
                {'categoryId': 1, 'tagId': 1, 'tagName': 'tag1', 'tagNameShort': 'tag1s'}, 
                {'categoryId': 1, 'tagId': 2, 'tagName': 'tag2', 'tagNameShort': 'tag2s'}, 
                {'categoryId': 1, 'tagId': 3, 'tagName': 'tag3', 'tagNameShort': 'tag3s'}
            ],
            'is_live': False,
            'user': {
                'email': 'admin@admin.com',
                'id': '170b76ca-9cdb-4d3b-af35-f3c0202d7357'
            },
            'visit_count': 0
        }
        assert response.json() == expected_response_body

    async def test_empty_fields(self, adminClient):
        # PRECONDITIONS
        request_data_copy = await setup_project_request_data(adminClient)

        # TEST
        request_data = request_data_copy.copy()
        request_data['title'] = None
        response = await adminClient.post('/projects', data=request_data)
        assert response.status_code == 400 or response.status_code == 422

        request_data = request_data_copy.copy()
        request_data['title'] = ''
        response = await adminClient.post('/projects', data=request_data)
        assert response.status_code == 400 or response.status_code == 422

        request_data = request_data_copy.copy()
        request_data['link'] = None
        response = await adminClient.post('/projects', data=request_data)
        assert response.status_code == 400 or response.status_code == 422

        request_data = request_data_copy.copy()
        request_data['link'] = ''
        response = await adminClient.post('/projects', data=request_data)
        assert response.status_code == 400 or response.status_code == 422

        request_data = request_data_copy.copy()
        request_data['completionDate'] = None
        response = await adminClient.post('/projects', data=request_data)
        assert response.status_code == 400 or response.status_code == 422

        request_data = request_data_copy.copy()
        request_data['completionDate'] = ''
        response = await adminClient.post('/projects', data=request_data)
        assert response.status_code == 400 or response.status_code == 422

        request_data = request_data_copy.copy()
        request_data['description'] = None
        response = await adminClient.post('/projects', data=request_data)
        assert response.status_code == 400 or response.status_code == 422

        request_data = request_data_copy.copy()
        request_data['description'] = ''
        response = await adminClient.post('/projects', data=request_data)
        assert response.status_code == 400 or response.status_code == 422

        request_data = request_data_copy.copy()
        request_data['content'] = None
        response = await adminClient.post('/projects', data=request_data)
        assert response.status_code == 400 or response.status_code == 422

        request_data = request_data_copy.copy()
        request_data['content'] = ''
        response = await adminClient.post('/projects', data=request_data)
        assert response.status_code == 400 or response.status_code == 422

    async def test_invalid_link(self, adminClient):
        # PRECONDITIONS
        request_data = await setup_project_request_data(adminClient)

        # TEST
        request_data['link'] = 'invalidlink'
        response = await adminClient.post('/projects', data=request_data)
        assert response.status_code == 400 or response.status_code == 422

    async def test_invalid_completion_date(self, adminClient):
        # PRECONDITIONS
        request_data = await setup_project_request_data(adminClient)

        # TEST
        request_data['completionDate'] = 'invalidcompletiondate'
        response = await adminClient.post('/projects', data=request_data)
        assert response.status_code == 400 or response.status_code == 422

    async def test_response_body(self, adminClient):
        # PRECONDITIONS
        request_data = await setup_project_request_data(adminClient)

        # TEST
        response = await adminClient.post('/projects', data=request_data)
        assert response.status_code == 200
        projectId = (response.json())['id']
        assert projectId
        expected_response_body = {
            'id': projectId,
            'title': 'title1',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': [
                {'categoryId': 1, 'tagId': 1, 'tagName': 'tag1', 'tagNameShort': 'tag1s'}, 
                {'categoryId': 1, 'tagId': 2, 'tagName': 'tag2', 'tagNameShort': 'tag2s'}, 
                {'categoryId': 1, 'tagId': 3, 'tagName': 'tag3', 'tagNameShort': 'tag3s'}
            ],
            'is_live': False
        }
        assert response.json() == expected_response_body

        # # POSTCONDITIONS
        # response = await adminClient.get(f'/projects/{projectId}', params={ 'additional_info': True })
        # assert response.status_code == 200
        # expected_response_body = {
        #     'id': projectId,
        #     'title': 'title1',
        #     'link': 'https://example.com',
        #     'description': 'description1',
        #     'date': '2011-10-05T14:48:00',
        #     'content': 'content1',
        #     'tags': [
        #         {'categoryId': 1, 'tagId': 1, 'tagName': 'tag1', 'tagNameShort': 'tag1s'}, 
        #         {'categoryId': 1, 'tagId': 2, 'tagName': 'tag2', 'tagNameShort': 'tag2s'}, 
        #         {'categoryId': 1, 'tagId': 3, 'tagName': 'tag3', 'tagNameShort': 'tag3s'}
        #     ],
        #     'is_live': False,
        #     'user': {
        #         'email': 'admin@admin.com',
        #         'id': '170b76ca-9cdb-4d3b-af35-f3c0202d7357'
        #     },
        #     'visit_count': 0
        # }
        # assert response.json() == expected_response_body


# Tests for PATCH /projects/{id}

class TestPatchProjectsId:
    
    async def test_toggle_live_as_admin(self, adminClient):
        # PRECONDITIONS
        request_data = {
            'title': 'title1',
            'link': 'https://example.com',
            'completionDate': '2011-10-05T14:48:00.000Z',
            'description': 'description1',
            'content': 'content1'
        }
        response = await adminClient.post('/projects', data=request_data)
        assert response.status_code == 200
        projectId = (response.json())['id']
        assert projectId
        response = await adminClient.get(f'/projects/{projectId}', params={ 'additional_info': True })
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': [],
            'is_live': False,
            'user': {
                'email': 'admin@admin.com',
                'id': '170b76ca-9cdb-4d3b-af35-f3c0202d7357'
            },
            'visit_count': 0
        }
        assert response.json() == expected_response_body

        # TEST
        patch_data = {
            'is_live': True
        }
        response = await adminClient.patch(f'/projects/{projectId}', data=patch_data)
        assert response.status_code == 200

        # POSTCONDITIONS
        response = await adminClient.get(f'/projects/{projectId}', params={ 'additional_info': True })
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': [],
            'is_live': True,
            'user': {
                'email': 'admin@admin.com',
                'id': '170b76ca-9cdb-4d3b-af35-f3c0202d7357'
            },
            'visit_count': 0
        }
        assert response.json() == expected_response_body

    async def test_toggle_live_as_user(self, userClient):
        request_data = {
            'title': 'title1',
            'link': 'https://example.com',
            'completionDate': '2011-10-05T14:48:00.000Z',
            'description': 'description1',
            'content': 'content1'
        }
        response = await userClient.post('/projects', data=request_data)
        assert response.status_code == 200
        projectId = (response.json())['id']
        assert projectId
        response = await userClient.get(f'/projects/{projectId}', params={ 'additional_info': True })
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': [],
            'is_live': False
        }
        assert response.json() == expected_response_body

        # TEST
        patch_data = {
            'is_live': True
        }
        response = await userClient.patch(f'/projects/{projectId}', data=patch_data)
        assert response.status_code == 403

        # POSTCONDITIONS
        response = await userClient.get(f'/projects/{projectId}', params={ 'additional_info': True })
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': [],
            'is_live': False
        }
        assert response.json() == expected_response_body

    async def test_toggle_live_as_anon(self, client, userClient):
        request_data = {
            'title': 'title1',
            'link': 'https://example.com',
            'completionDate': '2011-10-05T14:48:00.000Z',
            'description': 'description1',
            'content': 'content1'
        }
        response = await userClient.post('/projects', data=request_data)
        assert response.status_code == 200
        projectId = (response.json())['id']
        assert projectId
        response = await userClient.get(f'/projects/{projectId}', params={ 'additional_info': True })
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': [],
            'is_live': False
        }
        assert response.json() == expected_response_body

        # TEST
        patch_data = {
            'is_live': True
        }
        response = await client.patch(f'/projects/{projectId}', data=patch_data)
        assert response.status_code == 401

        # POSTCONDITIONS
        response = await userClient.get(f'/projects/{projectId}', params={ 'additional_info': True })
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': [],
            'is_live': False
        }
        assert response.json() == expected_response_body

    async def test_patch_all(self, adminClient):
        # PRECONDITIONS
        request_data = await setup_project_request_data(adminClient)
        response = await adminClient.post('/projects', data=request_data)
        assert response.status_code == 200
        projectId = (response.json())['id']
        assert projectId

        # TEST
        patch_data = {
            'title': 'title1new',
            'link': 'https://example.com/new',
            'description': 'description1new',
            'completionDate': '2022-10-05T14:48:22',
            'content': 'content1new',
            'tags': '2, 3',
            'is_live': True,
            'user': 'shouldbeignored',
            'visit_count': 123456
        }
        response = await adminClient.patch(f'/projects/{projectId}', data=patch_data)

        # POSTCONDITIONS
        response = await adminClient.get(f'/projects/{projectId}', params={ 'additional_info': True })
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1new',
            'link': 'https://example.com/new',
            'description': 'description1new',
            'date': '2022-10-05T14:48:22',
            'content': 'content1new',
            'tags': [
                { 'categoryId': 1, 'tagId': 2, 'tagName': 'tag2', 'tagNameShort': 'tag2s' }, 
                { 'categoryId': 1, 'tagId': 3, 'tagName': 'tag3', 'tagNameShort': 'tag3s' }
            ],
            'is_live': True,
            'user': {
                'email': 'admin@admin.com',
                'id': '170b76ca-9cdb-4d3b-af35-f3c0202d7357'
            },
            'visit_count': 0
        }
        assert response.json() == expected_response_body

    async def test_patch_not_all(self, adminClient):
        # PRECONDITIONS
        request_data = {
            'title': 'title1',
            'link': 'https://example.com',
            'completionDate': '2011-10-05T14:48:00.000Z',
            'description': 'description1',
            'content': 'content1'
        }
        response = await adminClient.post('/projects', data=request_data)
        assert response.status_code == 200
        projectId = (response.json())['id']
        assert projectId

        # TEST
        patch_data = {
            'title': 'title1new',
            'content': 'content1new'
        }
        response = await adminClient.patch(f'/projects/{projectId}', data=patch_data)
        assert response.status_code == 200

        # POSTCONDITIONS
        response = await adminClient.get(f'/projects/{projectId}')
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1new',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1new',
            'tags': []
        }
        assert response.json() == expected_response_body

    async def test_invalid_link(self, adminClient):
        # PRECONDITIONS
        request_data = {
            'title': 'title1',
            'link': 'https://example.com',
            'completionDate': '2011-10-05T14:48:00.000Z',
            'description': 'description1',
            'content': 'content1'
        }
        response = await adminClient.post('/projects', data=request_data)
        assert response.status_code == 200
        projectId = (response.json())['id']
        assert projectId

        # TEST
        patch_data = {
            'link': 'invalidlink',
        }
        response = await adminClient.patch(f'/projects/{projectId}', data=patch_data)
        assert response.status_code == 400 or response.status_code == 422

        # POSTCONDITIONS
        response = await adminClient.get(f'/projects/{projectId}')
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': []
        }
        assert response.json() == expected_response_body

    async def test_invalid_completion_date(self, adminClient):
        # PRECONDITIONS
        request_data = {
            'title': 'title1',
            'link': 'https://example.com',
            'completionDate': '2011-10-05T14:48:00.000Z',
            'description': 'description1',
            'content': 'content1'
        }
        response = await adminClient.post('/projects', data=request_data)
        assert response.status_code == 200
        projectId = (response.json())['id']
        assert projectId

        # TEST
        patch_data = {
            'completionDate': 'invaliddate',
        }
        response = await adminClient.patch(f'/projects/{projectId}', data=patch_data)
        assert response.status_code == 400 or response.status_code == 422

        # POSTCONDITIONS
        response = await adminClient.get(f'/projects/{projectId}')
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': []
        }
        assert response.json() == expected_response_body

    async def test_not_found_invalid_uuid(self, client, userClient, adminClient):
        # TEST
        response = await client.patch('/projects/invaliduuid')
        assert response.status_code == 401
        response = await userClient.patch('/projects/invaliduuid')
        assert response.status_code == 404
        response = await adminClient.patch('/projects/invaliduuid')
        assert response.status_code == 404

    async def test_not_found_valid_uuid(self, client, userClient, adminClient):
        # TEST
        response = await client.patch('/projects/f8c1147d-b1c0-4dbb-b4c2-7191ff78ac99')
        assert response.status_code == 401
        response = await userClient.patch('/projects/f8c1147d-b1c0-4dbb-b4c2-7191ff78ac99')
        assert response.status_code == 404
        response = await adminClient.patch('/projects/f8c1147d-b1c0-4dbb-b4c2-7191ff78ac99')

    async def test_as_admin(self, adminClient, userClient):
        # PRECONDITIONS
        request_data = {
            'title': 'title1',
            'link': 'https://example.com',
            'completionDate': '2011-10-05T14:48:00.000Z',
            'description': 'description1',
            'content': 'content1'
        }
        response = await userClient.post('/projects', data=request_data)
        assert response.status_code == 200
        projectId = (response.json())['id']
        assert projectId
        response = await userClient.get(f'/projects/{projectId}')
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': []
        }
        assert response.json() == expected_response_body

        # TEST
        response = await adminClient.patch(f'/projects/{projectId}', data={ 'title': 'title1new' })
        assert response.status_code == 200

        # POSTCONDITIONS
        response = await userClient.get(f'/projects/{projectId}')
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1new',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': []
        }
        assert response.json() == expected_response_body

    async def test_as_user_self(self, userClient, adminClient):
        # PRECONDITIONS
        request_data = {
            'title': 'title1',
            'link': 'https://example.com',
            'completionDate': '2011-10-05T14:48:00.000Z',
            'description': 'description1',
            'content': 'content1'
        }
        response = await userClient.post('/projects', data=request_data)
        assert response.status_code == 200
        projectId = (response.json())['id']
        assert projectId
        response = await userClient.get(f'/projects/{projectId}')
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': []
        }
        assert response.json() == expected_response_body

        # TEST
        response = await userClient.patch(f'/projects/{projectId}', data={ 'title': 'title1new' })
        assert response.status_code == 200

        # POSTCONDITIONS
        response = await adminClient.get(f'/projects/{projectId}')
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1new',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': []
        }
        assert response.json() == expected_response_body

    async def test_as_user_not_self(self, adminClient, userClient, client):
        # PRECONDITIONS
        request_data = {
            'title': 'title1',
            'link': 'https://example.com',
            'completionDate': '2011-10-05T14:48:00.000Z',
            'description': 'description1',
            'content': 'content1'
        }
        response = await adminClient.post('/projects', data=request_data)
        assert response.status_code == 200
        projectId = (response.json())['id']
        assert projectId
        response = await adminClient.get(f'/projects/{projectId}')
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': []
        }
        assert response.json() == expected_response_body

        # TEST
        response = await userClient.patch(f'/projects/{projectId}', data={ 'title': 'title1new' })
        assert response.status_code == 403

        # POSTCONDITIONS
        response = await adminClient.get(f'/projects/{projectId}')
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': []
        }
        assert response.json() == expected_response_body

    async def test_as_anon(self, adminClient, client):
        # PRECONDITIONS
        request_data = {
            'title': 'title1',
            'link': 'https://example.com',
            'completionDate': '2011-10-05T14:48:00.000Z',
            'description': 'description1',
            'content': 'content1'
        }
        response = await adminClient.post('/projects', data=request_data)
        assert response.status_code == 200
        projectId = (response.json())['id']
        assert projectId
        response = await adminClient.get(f'/projects/{projectId}')
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': []
        }
        assert response.json() == expected_response_body

        # TEST
        response = await client.patch(f'/projects/{projectId}', data={ 'title': 'title1new' })
        assert response.status_code == 401

        # POSTCONDITIONS
        response = await adminClient.get(f'/projects/{projectId}')
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': []
        }
        assert response.json() == expected_response_body

    async def test_response_body(self, adminClient):
        # PRECONDITIONS
        request_data = await setup_project_request_data(adminClient)
        response = await adminClient.post('/projects', data=request_data)
        assert response.status_code == 200
        projectId = (response.json())['id']
        assert projectId

        # TEST
        response = await adminClient.patch(f'/projects/{projectId}', data={ 'title': 'title1new' })
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1new',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': [
                {'categoryId': 1, 'tagId': 1, 'tagName': 'tag1', 'tagNameShort': 'tag1s'}, 
                {'categoryId': 1, 'tagId': 2, 'tagName': 'tag2', 'tagNameShort': 'tag2s'}, 
                {'categoryId': 1, 'tagId': 3, 'tagName': 'tag3', 'tagNameShort': 'tag3s'}
            ],
            'is_live': False
        }
        assert response.json() == expected_response_body

# Tests for DELETE /projects/{id}

class TestDeleteProjectsId:
    
    async def test_not_found_invalid_uuid(self, client, userClient, adminClient):
        # TEST
        response = await client.delete('/projects/invaliduuid')
        assert response.status_code == 401
        response = await userClient.delete('/projects/invaliduuid')
        assert response.status_code == 404
        response = await adminClient.delete('/projects/invaliduuid')
        assert response.status_code == 404

    async def test_not_found_valid_uuid(self, client, userClient, adminClient):
        # TEST
        response = await client.delete('/projects/f8c1147d-b1c0-4dbb-b4c2-7191ff78ac99')
        assert response.status_code == 401
        response = await userClient.delete('/projects/f8c1147d-b1c0-4dbb-b4c2-7191ff78ac99')
        assert response.status_code == 404
        response = await adminClient.delete('/projects/f8c1147d-b1c0-4dbb-b4c2-7191ff78ac99')
        assert response.status_code == 404

    async def test_as_admin(self, adminClient, userClient, client):
        # PRECONDITIONS
        request_data = {
            'title': 'title1',
            'link': 'https://example.com',
            'completionDate': '2011-10-05T14:48:00.000Z',
            'description': 'description1',
            'content': 'content1'
        }
        response = await userClient.post('/projects', data=request_data)
        assert response.status_code == 200
        projectId = (response.json())['id']
        assert projectId
        response = await userClient.get(f'/projects/{projectId}')
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': []
        }
        assert response.json() == expected_response_body

        # TEST
        response = await adminClient.delete(f'/projects/{projectId}')
        assert response.status_code == 204

        # POSTCONDITIONS
        response = await client.get(f'/projects/{projectId}')
        assert response.status_code == 404

    async def test_as_user_self(self, userClient, client):
        # PRECONDITIONS
        request_data = {
            'title': 'title1',
            'link': 'https://example.com',
            'completionDate': '2011-10-05T14:48:00.000Z',
            'description': 'description1',
            'content': 'content1'
        }
        response = await userClient.post('/projects', data=request_data)
        assert response.status_code == 200
        projectId = (response.json())['id']
        assert projectId
        response = await userClient.get(f'/projects/{projectId}')
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': []
        }
        assert response.json() == expected_response_body

        # TEST
        response = await userClient.delete(f'/projects/{projectId}')
        assert response.status_code == 204

        # POSTCONDITIONS
        response = await client.get(f'/projects/{projectId}')
        assert response.status_code == 404

    async def test_as_user_not_self(self, adminClient, userClient, client):
        # PRECONDITIONS
        request_data = {
            'title': 'title1',
            'link': 'https://example.com',
            'completionDate': '2011-10-05T14:48:00.000Z',
            'description': 'description1',
            'content': 'content1'
        }
        response = await adminClient.post('/projects', data=request_data)
        assert response.status_code == 200
        projectId = (response.json())['id']
        assert projectId
        response = await adminClient.get(f'/projects/{projectId}')
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': []
        }
        assert response.json() == expected_response_body

        # TEST
        response = await userClient.delete(f'/projects/{projectId}')
        assert response.status_code == 403

        # POSTCONDITIONS
        response = await adminClient.get(f'/projects/{projectId}')
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': []
        }
        assert response.json() == expected_response_body

    async def test_as_anon(self, adminClient, client):
        # PRECONDITIONS
        request_data = {
            'title': 'title1',
            'link': 'https://example.com',
            'completionDate': '2011-10-05T14:48:00.000Z',
            'description': 'description1',
            'content': 'content1'
        }
        response = await adminClient.post('/projects', data=request_data)
        assert response.status_code == 200
        projectId = (response.json())['id']
        assert projectId
        response = await adminClient.get(f'/projects/{projectId}')
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': []
        }
        assert response.json() == expected_response_body

        # TEST
        response = await client.delete(f'/projects/{projectId}')
        assert response.status_code == 401

        # POSTCONDITIONS
        response = await adminClient.get(f'/projects/{projectId}')
        assert response.status_code == 200
        expected_response_body = {
            'id': projectId,
            'title': 'title1',
            'link': 'https://example.com',
            'description': 'description1',
            'date': '2011-10-05T14:48:00',
            'content': 'content1',
            'tags': []
        }
        assert response.json() == expected_response_body


# Tests for GET /projects/{id}/image

class TestGetProjectsIdImage:

    async def test_not_found_invalid_uuid(self, client, userClient, adminClient):
        # TEST
        response = await client.get('/projects/invaliduuid/image')
        assert response.status_code == 404
        response = await userClient.get('/projects/invaliduuid/image')
        assert response.status_code == 404
        response = await adminClient.get('/projects/invaliduuid/image')
        assert response.status_code == 404

    async def test_not_found_valid_uuid(self, client, userClient, adminClient):
        # TEST
        response = await client.get('/projects/f8c1147d-b1c0-4dbb-b4c2-7191ff78ac99/image')
        assert response.status_code == 404
        response = await userClient.get('/projects/f8c1147d-b1c0-4dbb-b4c2-7191ff78ac99/image')
        assert response.status_code == 404
        response = await adminClient.get('/projects/f8c1147d-b1c0-4dbb-b4c2-7191ff78ac99/image')
        assert response.status_code == 404

    # TODO tests for approved/unapproved projects
