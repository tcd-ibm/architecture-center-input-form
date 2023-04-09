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

        response = await adminClient.post('/admin/tag', 
            json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat3Id })
        assert response.status_code == 200
        tag1Id = (response.json())['tagId']
        assert tag1Id
        response = await adminClient.post('/admin/tag', 
            json={ "tagName": "tag2", "tagNameShort": "tag2s", "categoryId": cat1Id })
        assert response.status_code == 200
        tag2Id = (response.json())['tagId']
        assert tag2Id
        response = await adminClient.post('/admin/tag', 
            json={ "tagName": "tag3", "tagNameShort": "tag3s", "categoryId": cat3Id })
        assert response.status_code == 200
        tag3Id = (response.json())['tagId']
        assert tag3Id
        response = await adminClient.post('/admin/tag', 
            json={ "tagName": "tag4", "tagNameShort": "tag4s", "categoryId": cat3Id })
        assert response.status_code == 200
        tag4Id = (response.json())['tagId']
        assert tag4Id
        response = await adminClient.post('/admin/tag', 
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

        response = await adminClient.post('/admin/tag', 
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
