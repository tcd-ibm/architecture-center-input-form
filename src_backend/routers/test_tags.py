import pytest

pytestmark = pytest.mark.anyio


# Tests for GET /tags

class TestGetTags:

    async def test_get_tags_empty(self, client):
        # TEST
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = []
        assert response.json() == expected_response_body

    async def test_get_tags(self, client, adminClient):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id
        response = await adminClient.post('/categories', json={ "categoryName": "cat2" })
        assert response.status_code == 200
        cat2Id = (response.json())['categoryId']
        assert cat2Id
        response = await adminClient.post('/categories', json={ "categoryName": "cat3" })
        assert response.status_code == 200
        cat3Id = (response.json())['categoryId']
        assert cat3Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat3Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id
        response = await adminClient.post('/tags', 
            json={ "tagName": "tag2", "tagNameShort": "tag2s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag2Id = (response.json())['tagId']
        assert tag2Id
        response = await adminClient.post('/tags', 
            json={ "tagName": "tag3", "tagNameShort": "tag3s", "categoryId": cat3Id })
        assert response.status_code == 200
        tag3Id = (response.json())['tagId']
        assert tag3Id
        response = await adminClient.post('/tags', 
            json={ "tagName": "tag4", "tagNameShort": "tag4s", "categoryId": cat3Id })
        assert response.status_code == 200
        tag4Id = (response.json())['tagId']
        assert tag4Id
        response = await adminClient.post('/tags', 
            json={ "tagName": "tag5", "tagNameShort": "tag5s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag5Id = (response.json())['tagId']
        assert tag5Id

        # TEST
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': [
                    { "tagId": tag2Id, "tagName": "tag2", "tagNameShort": "tag2s", "categoryId": cat1Id},
                    { "tagId": tag5Id, "tagName": "tag5", "tagNameShort": "tag5s", "categoryId": cat1Id}
                ]
            },
            {
                'categoryId': cat2Id,
                'categoryName': 'cat2',
                'tags': []
            },
            {
                'categoryId': cat3Id,
                'categoryName': 'cat3',
                'tags': [
                    { "tagId": tag1Id, "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat3Id },
                    { "tagId": tag3Id, "tagName": "tag3", "tagNameShort": "tag3s", "categoryId": cat3Id },
                    { "tagId": tag4Id, "tagName": "tag4", "tagNameShort": "tag4s", "categoryId": cat3Id }
                ]
            }
        ]
        assert response.json() == expected_response_body


# Tests for GET /tags/{id}

class TestGetTagsId:

    async def test_get_tag_not_found(self, client):
        # TEST
        response = await client.get('/tags/1')
        assert response.status_code == 404

    async def test_get_tag(self, client, adminClient):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id

        # TEST
        response = await client.get(f'/tags/{str(tag1Id)}')
        assert response.status_code == 200
        expected_response_body = { 
            "tagId": tag1Id, 
            "tagName": "tag1", 
            "tagNameShort": "tag1s", 
            "categoryId": cat1Id
        }
        assert response.json() == expected_response_body


# Tests for POST /tags

class TestPostTags:

    async def test_post_tag_no_body(self, adminClient, client):
        # TEST
        response = await adminClient.post('/tags')
        assert response.status_code == 400 or response.status_code == 422

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = []
        assert response.json() == expected_response_body

    async def test_post_tag_empty_body(self, adminClient, client):
        # TEST
        response = await adminClient.post('/tags', json={})
        assert response.status_code == 400 or response.status_code == 422

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = []
        assert response.json() == expected_response_body

    async def test_post_tag_no_tag_name(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        # TEST
        response = await adminClient.post('/tags', 
            json={ "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 400 or response.status_code == 422

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': []
            }
        ]
        assert response.json() == expected_response_body

    async def test_post_tag_empty_tag_name(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        # TEST
        response = await adminClient.post('/tags', 
            json={ "tagName": "", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 400 or response.status_code == 422

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': []
            }
        ]
        assert response.json() == expected_response_body

    async def test_post_tag_no_tag_short_name(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        # TEST
        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "categoryId": cat1Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': [
                    { "tagId": tag1Id, "tagName": "tag1", "tagNameShort": "tag1", "categoryId": cat1Id }
                ]
            }
        ]
        assert response.json() == expected_response_body

    async def test_post_tag_empty_tag_short_name(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        # TEST
        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "", "categoryId": cat1Id })
        assert response.status_code == 400 or response.status_code == 422

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': []
            }
        ]
        assert response.json() == expected_response_body

    async def test_post_tag_no_category_id(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        # TEST
        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s" })
        assert response.status_code == 400 or response.status_code == 422

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': []
            }
        ]
        assert response.json() == expected_response_body

    async def test_post_tag_empty_category_id(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        # TEST
        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": "" })
        assert response.status_code == 400 or response.status_code == 422

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': []
            }
        ]
        assert response.json() == expected_response_body

    async def test_post_tag_invalid_category_id(self, adminClient, client):
        # TEST
        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": 123 })
        assert response.status_code == 400 or response.status_code == 422

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = []
        assert response.json() == expected_response_body

    async def test_post_tag_repeated_tag_name(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id
        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id

        # TEST
        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1snew", "categoryId": cat1Id })
        assert response.status_code == 400 or response.status_code == 422

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': [
                    { "tagId": tag1Id, "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id }
                ]
            }
        ]
        assert response.json() == expected_response_body

    async def test_post_tag_repeated_short_tag_name(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id
        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id

        # TEST
        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1new", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 400 or response.status_code == 422

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': [
                    { "tagId": tag1Id, "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id }
                ]
            }
        ]
        assert response.json() == expected_response_body

    async def test_post_tag_repeated_names(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id

        # TEST
        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 400 or response.status_code == 422

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': [
                    { "tagId": tag1Id, "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id }
                ]
            }
        ]
        assert response.json() == expected_response_body

    async def test_post_tag_array_body(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        # TEST
        response = await adminClient.post('/tags', 
            json=[ { "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id } ])
        assert response.status_code == 400 or response.status_code == 422

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': []
            }
        ]
        assert response.json() == expected_response_body

    async def test_post_tag(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id
        response = await adminClient.post('/categories', json={ "categoryName": "cat2" })
        assert response.status_code == 200
        cat2Id = (response.json())['categoryId']
        assert cat2Id

        # TEST
        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat2Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id
        response = await adminClient.post('/tags', 
            json={ "tagName": "tag2", "tagNameShort": "tag2s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag2Id = (response.json())['tagId']
        assert tag2Id
        response = await adminClient.post('/tags', 
            json={ "tagName": "tag3", "tagNameShort": "tag3s", "categoryId": cat2Id })
        assert response.status_code == 200
        tag3Id = (response.json())['tagId']
        assert tag3Id

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': [
                    { "tagId": tag2Id, "tagName": "tag2", "tagNameShort": "tag2s", "categoryId": cat1Id },
                ]
            },
            {
                'categoryId': cat2Id,
                'categoryName': 'cat2',
                'tags': [
                    { "tagId": tag1Id, "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat2Id },
                    { "tagId": tag3Id, "tagName": "tag3", "tagNameShort": "tag3s", "categoryId": cat2Id },
                ]
            }
        ]
        assert response.json() == expected_response_body

    async def test_post_tag_as_user(self, userClient, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        # TEST
        response = await userClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 403

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': []
            }
        ]
        assert response.json() == expected_response_body

    async def test_post_tag_as_anon(self, client, adminClient):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        # TEST
        response = await client.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 401

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': []
            }
        ]
        assert response.json() == expected_response_body

    async def test_post_tag_response_body(self, adminClient):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        # TEST
        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag1Id = (response.json())['categoryId']
        assert tag1Id
        expected_response_body = {
                'tagId': tag1Id,
                'tagName': 'tag1',
                'tagNameShort': 'tag1s',
                'categoryId': cat1Id
            }
        assert response.json() == expected_response_body


# Tests for PATCH /tags/{id}

class TestPatchTagsId:

    async def test_patch_tag_no_body(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id

        # TEST
        response = await adminClient.patch(f'/tags/{str(tag1Id)}')
        assert response.status_code == 400 or response.status_code == 422

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': [
                    { "tagId": tag1Id, "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id },
                ]
            }
        ]
        assert response.json() == expected_response_body
   
    async def test_patch_tag_empty_body(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id

        # TEST
        response = await adminClient.patch(f'/tags/{str(tag1Id)}', json={})
        assert response.status_code == 400 or response.status_code == 422

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': [
                    { "tagId": tag1Id, "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id },
                ]
            }
        ]
        assert response.json() == expected_response_body

    async def test_patch_tag_with_id_in_body(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id
        response = await adminClient.post('/categories', json={ "categoryName": "cat2" })
        assert response.status_code == 200
        cat2Id = (response.json())['categoryId']
        assert cat2Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id

        # TEST
        response = await adminClient.patch(f'/tags/{str(tag1Id)}', 
            json={ "tagId": 123, "tagName": "tag1new", "tagNameShort": "tag1snew", "categoryId": cat2Id })
        assert response.status_code == 200

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': []
            },
            {
                'categoryId': cat2Id,
                'categoryName': 'cat2',
                'tags': [
                    { "tagId": tag1Id, "tagName": "tag1new", "tagNameShort": "tag1snew", "categoryId": cat2Id },
                ]
            }
        ]
        assert response.json() == expected_response_body

    async def test_patch_tag_empty_name(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id
        response = await adminClient.post('/categories', json={ "categoryName": "cat2" })
        assert response.status_code == 200
        cat2Id = (response.json())['categoryId']
        assert cat2Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id

        # TEST
        response = await adminClient.patch(f'/tags/{str(tag1Id)}', 
            json={ "tagName": "", "tagNameShort": "tag1snew", "categoryId": cat2Id })
        assert response.status_code == 400 or response.status_code == 422

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': [
                    { "tagId": tag1Id, "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id }
                ]
            },
            {
                'categoryId': cat2Id,
                'categoryName': 'cat2',
                'tags': []
            }
        ]
        assert response.json() == expected_response_body

    async def test_patch_tag_empty_short_name(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id
        response = await adminClient.post('/categories', json={ "categoryName": "cat2" })
        assert response.status_code == 200
        cat2Id = (response.json())['categoryId']
        assert cat2Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id

        # TEST
        response = await adminClient.patch(f'/tags/{str(tag1Id)}', 
            json={ "tagName": "tag1new", "tagNameShort": "", "categoryId": cat2Id })
        assert response.status_code == 400 or response.status_code == 422

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': [
                    { "tagId": tag1Id, "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id }
                ]
            },
            {
                'categoryId': cat2Id,
                'categoryName': 'cat2',
                'tags': []
            }
        ]
        assert response.json() == expected_response_body

    async def test_patch_tag_empty_category_id(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id
        response = await adminClient.post('/categories', json={ "categoryName": "cat2" })
        assert response.status_code == 200
        cat2Id = (response.json())['categoryId']
        assert cat2Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id

        # TEST
        response = await adminClient.patch(f'/tags/{str(tag1Id)}', 
            json={ "tagName": "tag1new", "tagNameShort": "tag1snew", "categoryId": "" })
        assert response.status_code == 400 or response.status_code == 422

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': [
                    { "tagId": tag1Id, "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id }
                ]
            },
            {
                'categoryId': cat2Id,
                'categoryName': 'cat2',
                'tags': []
            }
        ]
        assert response.json() == expected_response_body

    async def test_patch_tag_invalid_category_id(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id
        response = await adminClient.post('/categories', json={ "categoryName": "cat2" })
        assert response.status_code == 200
        cat2Id = (response.json())['categoryId']
        assert cat2Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id

        # TEST
        response = await adminClient.patch(f'/tags/{str(tag1Id)}', 
            json={ "tagName": "tag1new", "tagNameShort": "tag1snew", "categoryId": 123 })
        assert response.status_code == 400 or response.status_code == 422

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': [
                    { "tagId": tag1Id, "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id }
                ]
            },
            {
                'categoryId': cat2Id,
                'categoryName': 'cat2',
                'tags': []
            }
        ]
        assert response.json() == expected_response_body

    async def test_patch_tag_repeated_name(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id
        response = await adminClient.post('/categories', json={ "categoryName": "cat2" })
        assert response.status_code == 200
        cat2Id = (response.json())['categoryId']
        assert cat2Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag2", "tagNameShort": "tag2s", "categoryId": cat2Id })
        assert response.status_code == 200
        tag2Id = (response.json())['tagId']
        assert tag2Id

        # TEST
        response = await adminClient.patch(f'/tags/{str(tag1Id)}', 
            json={ "tagName": "tag2", "tagNameShort": "tag1snew", "categoryId": cat2Id })
        assert response.status_code == 400 or response.status_code == 422

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': [
                    { "tagId": tag1Id, "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id }
                ]
            },
            {
                'categoryId': cat2Id,
                'categoryName': 'cat2',
                'tags': [
                    { "tagId": tag2Id, "tagName": "tag2", "tagNameShort": "tag2s", "categoryId": cat2Id }
                ]
            }
        ]
        assert response.json() == expected_response_body

    async def test_patch_tag_repeated_short_name(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id
        response = await adminClient.post('/categories', json={ "categoryName": "cat2" })
        assert response.status_code == 200
        cat2Id = (response.json())['categoryId']
        assert cat2Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag2", "tagNameShort": "tag2s", "categoryId": cat2Id })
        assert response.status_code == 200
        tag2Id = (response.json())['tagId']
        assert tag2Id

        # TEST
        response = await adminClient.patch(f'/tags/{str(tag1Id)}', 
            json={ "tagName": "tag1new", "tagNameShort": "tag2s", "categoryId": cat2Id })
        assert response.status_code == 400 or response.status_code == 422

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': [
                    { "tagId": tag1Id, "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id }
                ]
            },
            {
                'categoryId': cat2Id,
                'categoryName': 'cat2',
                'tags': [
                    { "tagId": tag2Id, "tagName": "tag2", "tagNameShort": "tag2s", "categoryId": cat2Id }
                ]
            }
        ]
        assert response.json() == expected_response_body

    async def test_patch_tag_repeated_names(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id
        response = await adminClient.post('/categories', json={ "categoryName": "cat2" })
        assert response.status_code == 200
        cat2Id = (response.json())['categoryId']
        assert cat2Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag2", "tagNameShort": "tag2s", "categoryId": cat2Id })
        assert response.status_code == 200
        tag2Id = (response.json())['tagId']
        assert tag2Id

        # TEST
        response = await adminClient.patch(f'/tags/{str(tag1Id)}', 
            json={ "tagName": "tag2", "tagNameShort": "tag2s", "categoryId": cat2Id })
        assert response.status_code == 400 or response.status_code == 422

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': [
                    { "tagId": tag1Id, "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id }
                ]
            },
            {
                'categoryId': cat2Id,
                'categoryName': 'cat2',
                'tags': [
                    { "tagId": tag2Id, "tagName": "tag2", "tagNameShort": "tag2s", "categoryId": cat2Id }
                ]
            }
        ]
        assert response.json() == expected_response_body

    async def test_patch_tag_array_body(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id

        # TEST
        response = await adminClient.patch(f'/tags/{str(tag1Id)}', 
            json=[{ "tagName": "tag1new", "tagNameShort": "tag1snew" }])
        assert response.status_code == 400 or response.status_code == 422

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': [
                    { "tagId": tag1Id, "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id },
                ]
            }
        ]
        assert response.json() == expected_response_body

    async def test_patch_tag(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id
        response = await adminClient.post('/categories', json={ "categoryName": "cat2" })
        assert response.status_code == 200
        cat2Id = (response.json())['categoryId']
        assert cat2Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id

        # TEST
        response = await adminClient.patch(f'/tags/{str(tag1Id)}', 
            json={ "tagName": "tag1new", "tagNameShort": "tag1snew", "categoryId": cat2Id })
        assert response.status_code == 200

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': []
            },
            {
                'categoryId': cat2Id,
                'categoryName': 'cat2',
                'tags': [
                    { "tagId": tag1Id, "tagName": "tag1new", "tagNameShort": "tag1snew", "categoryId": cat2Id },
                ]
            }
        ]
        assert response.json() == expected_response_body

    async def test_patch_tag_name(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id
        response = await adminClient.post('/categories', json={ "categoryName": "cat2" })
        assert response.status_code == 200
        cat2Id = (response.json())['categoryId']
        assert cat2Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id

        # TEST
        response = await adminClient.patch(f'/tags/{str(tag1Id)}', 
            json={ "tagName": "tag1new" })
        assert response.status_code == 200

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': [
                    { "tagId": tag1Id, "tagName": "tag1new", "tagNameShort": "tag1s", "categoryId": cat1Id }
                ]
            },
            {
                'categoryId': cat2Id,
                'categoryName': 'cat2',
                'tags': []
            }
        ]
        assert response.json() == expected_response_body

    async def test_patch_tag_short_name(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id
        response = await adminClient.post('/categories', json={ "categoryName": "cat2" })
        assert response.status_code == 200
        cat2Id = (response.json())['categoryId']
        assert cat2Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id

        # TEST
        response = await adminClient.patch(f'/tags/{str(tag1Id)}', 
            json={ "tagNameShort": "tag1snew" })
        assert response.status_code == 200

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': [
                    { "tagId": tag1Id, "tagName": "tag1", "tagNameShort": "tag1snew", "categoryId": cat1Id }
                ]
            },
            {
                'categoryId': cat2Id,
                'categoryName': 'cat2',
                'tags': []
            }
        ]
        assert response.json() == expected_response_body

    async def test_patch_tag_category_id(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id
        response = await adminClient.post('/categories', json={ "categoryName": "cat2" })
        assert response.status_code == 200
        cat2Id = (response.json())['categoryId']
        assert cat2Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id

        # TEST
        response = await adminClient.patch(f'/tags/{str(tag1Id)}', 
            json={ "categoryId": cat2Id })
        assert response.status_code == 200

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': []
            },
            {
                'categoryId': cat2Id,
                'categoryName': 'cat2',
                'tags': [
                    { "tagId": tag1Id, "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat2Id },
                ]
            }
        ]
        assert response.json() == expected_response_body

    async def test_patch_tag_not_found(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id

        # TEST
        response = await adminClient.patch(f'/tags/{str(tag1Id)}123', 
            json={ "tagName": "tag1new", "tagNameShort": "tag1snew" })
        assert response.status_code == 404

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': [
                    { "tagId": tag1Id, "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id },
                ]
            }
        ]
        assert response.json() == expected_response_body

    async def test_patch_tag_as_user(self, userClient, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id

        # TEST
        response = await userClient.patch(f'/tags/{str(tag1Id)}', 
            json={ "tagName": "tag1new", "tagNameShort": "tag1snew" })
        assert response.status_code == 403

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': [
                    { "tagId": tag1Id, "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id },
                ]
            }
        ]
        assert response.json() == expected_response_body

    async def test_patch_tag_as_anon(self, client, adminClient):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id

        # TEST
        response = await client.patch(f'/tags/{str(tag1Id)}', 
            json={ "tagName": "tag1new", "tagNameShort": "tag1snew" })
        assert response.status_code == 401

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': [
                    { "tagId": tag1Id, "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id },
                ]
            }
        ]
        assert response.json() == expected_response_body

    async def test_patch_tag_response_body(self, adminClient):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id

        # TEST
        response = await adminClient.patch(f'/tags/{str(tag1Id)}', json={ "tagName": "tag1new" })
        assert response.status_code == 200
        expected_response_body = { 
            "tagId": tag1Id, 
            "tagName": "tag1new", 
            "tagNameShort": "tag1s", 
            "categoryId": cat1Id 
        }
        assert response.json() == expected_response_body


# Tests for DELETE /tags/{id}

class TestDeleteTagsId:

    async def test_delete_tag(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id

        # TEST
        response = await adminClient.delete(f'/tags/{str(tag1Id)}')
        assert response.status_code == 204

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': []
            }
        ]
        assert response.json() == expected_response_body

        response = await client.get(f'/tags/{str(tag1Id)}')
        assert response.status_code == 404

    async def test_delete_tag_multiple(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id
        response = await adminClient.post('/categories', json={ "categoryName": "cat2" })
        assert response.status_code == 200
        cat2Id = (response.json())['categoryId']
        assert cat2Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat2Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id
        response = await adminClient.post('/tags', 
            json={ "tagName": "tag2", "tagNameShort": "tag2s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag2Id = (response.json())['tagId']
        assert tag2Id
        response = await adminClient.post('/tags', 
            json={ "tagName": "tag3", "tagNameShort": "tag3s", "categoryId": cat2Id })
        assert response.status_code == 200
        tag3Id = (response.json())['tagId']
        assert tag3Id
        response = await adminClient.post('/tags', 
            json={ "tagName": "tag4", "tagNameShort": "tag4s", "categoryId": cat2Id })
        assert response.status_code == 200
        tag4Id = (response.json())['tagId']
        assert tag4Id
        response = await adminClient.post('/tags', 
            json={ "tagName": "tag5", "tagNameShort": "tag5s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag5Id = (response.json())['tagId']
        assert tag5Id

        # TEST
        response = await adminClient.delete(f'/tags/{str(tag3Id)}')
        assert response.status_code == 204
        response = await adminClient.delete(f'/tags/{str(tag2Id)}')
        assert response.status_code == 204

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': [
                    { "tagId": tag5Id, "tagName": "tag5", "tagNameShort": "tag5s", "categoryId": cat1Id }
                ]
            },
            {
                'categoryId': cat2Id,
                'categoryName': 'cat2',
                'tags': [
                    { "tagId": tag1Id, "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat2Id },
                    { "tagId": tag4Id, "tagName": "tag4", "tagNameShort": "tag4s", "categoryId": cat2Id }
                ]
            }
        ]
        assert response.json() == expected_response_body

        response = await client.get(f'/tags/{str(tag2Id)}')
        assert response.status_code == 404
        response = await client.get(f'/tags/{str(tag3Id)}')
        assert response.status_code == 404

    async def test_delete_tag_not_found(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id

        # TEST
        response = await adminClient.delete(f'/tags/{str(tag1Id)}123')
        assert response.status_code == 404

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': [
                    { "tagId": tag1Id, "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id }
                ]
            }
        ]
        assert response.json() == expected_response_body
        response = await client.get(f'/tags/{str(tag1Id)}')
        assert response.status_code == 200
        expected_response_body = { 
            "tagId": tag1Id, 
            "tagName": "tag1", 
            "tagNameShort": "tag1s", 
            "categoryId": cat1Id 
        }
        assert response.json() == expected_response_body

    async def test_delete_tag_as_user(self, userClient, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id

        # TEST
        response = await userClient.delete(f'/tags/{str(tag1Id)}')
        assert response.status_code == 403

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': [
                    { "tagId": tag1Id, "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id }
                ]
            }
        ]
        assert response.json() == expected_response_body
        response = await client.get(f'/tags/{str(tag1Id)}')
        assert response.status_code == 200
        expected_response_body = { 
            "tagId": tag1Id, 
            "tagName": "tag1", 
            "tagNameShort": "tag1s", 
            "categoryId": cat1Id 
        }
        assert response.json() == expected_response_body

    async def test_delete_tag_as_anon(self, client, adminClient):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        response = await adminClient.post('/tags', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id

        # TEST
        response = await client.delete(f'/tags/{str(tag1Id)}')
        assert response.status_code == 401

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1',
                'tags': [
                    { "tagId": tag1Id, "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat1Id }
                ]
            }
        ]
        assert response.json() == expected_response_body
        response = await client.get(f'/tags/{str(tag1Id)}')
        assert response.status_code == 200
        expected_response_body = { 
            "tagId": tag1Id, 
            "tagName": "tag1", 
            "tagNameShort": "tag1s", 
            "categoryId": cat1Id 
        }
        assert response.json() == expected_response_body
