import pytest

pytestmark = pytest.mark.anyio


# Tests for POST /categories

class TestPostCategories:

    async def test_post_category_no_body(self, adminClient, client):
        # TEST
        response = await adminClient.post('/categories')
        assert response.status_code == 400 or response.status_code == 422

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = []
        assert response.json() == expected_response_body

    async def test_post_category_empty_body(self, adminClient, client):
        # TEST
        response = await adminClient.post('/categories', json={})
        assert response.status_code == 400 or response.status_code == 422

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = []
        assert response.json() == expected_response_body

    async def test_post_category_empty_category_name(self, adminClient, client):
        # TEST
        response = await adminClient.post('/categories', json={ "categoryName": "" })
        assert response.status_code == 400 or response.status_code == 422

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = []
        assert response.json() == expected_response_body

    async def test_post_category_array_body(self, adminClient, client):
        # TEST
        response = await adminClient.post('/categories', json=[ { "categoryName": "cat1" } ])
        assert response.status_code == 400 or response.status_code == 422

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = []
        assert response.json() == expected_response_body

    async def test_post_category(self, adminClient, client):
        # TEST
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id
        response = await adminClient.post('/categories', json={ "categoryName": "cat2" })
        assert response.status_code == 200
        cat2Id = (response.json())['categoryId']
        assert cat2Id

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
                'tags': []
            }
        ]
        assert response.json() == expected_response_body

    async def test_post_category_existing_name(self, adminClient, client):
        # TEST
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
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

    async def test_post_category_as_user(self, userClient, client):
        # TEST
        response = await userClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 401

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = []
        assert response.json() == expected_response_body

    async def test_post_category_as_anon(self, client):
        # TEST
        response = await client.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 401

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = []
        assert response.json() == expected_response_body

    async def test_post_category_response_body(self, adminClient):
        # TEST
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id
        expected_response_body = {
            'categoryId': cat1Id,
            'categoryName': 'cat1'
        }
        assert response.json() == expected_response_body


#Tests for PATCH /categories

class TestPatchCategories:

    async def test_patch_category_no_body(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        # TEST
        response = await adminClient.patch(f'/categories/{str(cat1Id)}')
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

    async def test_patch_category_empty_body(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        # TEST
        response = await adminClient.patch(f'/categories/{str(cat1Id)}', json={})
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

    async def test_patch_category_empty_category_name(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        # TEST
        response = await adminClient.patch(f'/categories/{str(cat1Id)}', json={ "categoryName": "" })
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

    async def test_patch_category_array_body(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        # TEST
        response = await adminClient.patch(f'/categories/{str(cat1Id)}', json=[ { "categoryName": "" } ])
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

    async def test_patch_category(self, adminClient, client):
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
        response = await adminClient.patch(f'/categories/{str(cat1Id)}', json={ "categoryName": "cat1new" })
        assert response.status_code == 200

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1new',
                'tags': []
            },
            {
                'categoryId': cat2Id,
                'categoryName': 'cat2',
                'tags': []
            }
        ]
        assert response.json() == expected_response_body

    async def test_patch_category_with_id_in_body(self, adminClient, client):
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
        response = await adminClient.patch(f'/categories/{str(cat1Id)}', json={ "categoryName": "cat1new", "categoryId": 123 })
        assert response.status_code == 200

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = [
            {
                'categoryId': cat1Id,
                'categoryName': 'cat1new',
                'tags': []
            },
            {
                'categoryId': cat2Id,
                'categoryName': 'cat2',
                'tags': []
            }
        ]
        assert response.json() == expected_response_body

    async def test_patch_category_not_found(self, adminClient, client):
        # TEST
        response = await adminClient.patch('/categories/1', json={ "categoryName": "cat1new" })
        assert response.status_code == 404

        # POSTCONDITIONS
        response = await client.get('/tags')
        assert response.status_code == 200
        expected_response_body = []
        assert response.json() == expected_response_body

    async def test_patch_category_as_user(self, userClient, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        # TEST
        response = await userClient.patch(f'/categories/{str(cat1Id)}', json={ "categoryName": "cat1new" })
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

    async def test_patch_category_as_anon(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        # TEST
        response = await client.patch(f'/categories/{str(cat1Id)}', json={ "categoryName": "cat1new" })
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

    async def test_patch_category_response_body(self, adminClient):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        # TEST
        response = await adminClient.patch(f'/categories/{str(cat1Id)}', json={ "categoryName": "cat1new" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id
        expected_response_body = {
            'categoryId': cat1Id,
            'categoryName': 'cat1new'
        }
        assert response.json() == expected_response_body


# Tests for DELETE /categories

class TestDeleteCategories:

    async def test_delete_category_not_found(self, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        # TEST
        response = await adminClient.delete(f'/categories/{str(cat1Id)}123')
        assert response.status_code == 404

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

    async def test_delete_category(self, adminClient, client):
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
                'tags': []
            },
            {
                'categoryId': cat3Id,
                'categoryName': 'cat3',
                'tags': []
            }
        ]
        assert response.json() == expected_response_body

        # TEST
        response = await adminClient.delete(f'/categories/{str(cat2Id)}')
        assert response.status_code == 204

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
                'categoryId': cat3Id,
                'categoryName': 'cat3',
                'tags': []
            }
        ]
        assert response.json() == expected_response_body

    # TODO fix the endpoint
    # async def test_delete_category_cascade(self, adminClient, client):
    #     # PRECONDITIONS
    #     response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
    #     assert response.status_code == 200
    #     cat1Id = (response.json())['categoryId']
    #     assert cat1Id
    #     response = await adminClient.post('/categories', json={ "categoryName": "cat2" })
    #     assert response.status_code == 200
    #     cat2Id = (response.json())['categoryId']
    #     assert cat2Id
    #     response = await adminClient.post('/categories', json={ "categoryName": "cat3" })
    #     assert response.status_code == 200
    #     cat3Id = (response.json())['categoryId']
    #     assert cat3Id

    #     response = await adminClient.post('/tags', 
    #         json={ "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat3Id })
    #     assert response.status_code == 200
    #     tag1Id = (response.json())['tagId']
    #     assert tag1Id
    #     response = await adminClient.post('/tags', 
    #         json={ "tagName": "tag2", "tagNameShort": "tag2s", "categoryId": cat1Id })
    #     assert response.status_code == 200
    #     tag2Id = (response.json())['tagId']
    #     assert tag2Id
    #     response = await adminClient.post('/tags', 
    #         json={ "tagName": "tag3", "tagNameShort": "tag3s", "categoryId": cat3Id })
    #     assert response.status_code == 200
    #     tag3Id = (response.json())['tagId']
    #     assert tag3Id
    #     response = await adminClient.post('/tags', 
    #         json={ "tagName": "tag4", "tagNameShort": "tag4s", "categoryId": cat3Id })
    #     assert response.status_code == 200
    #     tag4Id = (response.json())['tagId']
    #     assert tag4Id
    #     response = await adminClient.post('/tags', 
    #         json={ "tagName": "tag5", "tagNameShort": "tag5s", "categoryId": cat1Id })
    #     assert response.status_code == 200
    #     tag5Id = (response.json())['tagId']
    #     assert tag5Id

    #     response = await client.get('/tags')
    #     assert response.status_code == 200
    #     expected_response_body = [
    #         {
    #             'categoryId': cat1Id,
    #             'categoryName': 'cat1',
    #             'tags': [
    #                 { "tagId": tag2Id, "tagName": "tag2", "tagNameShort": "tag2s", "categoryId": cat1Id},
    #                 { "tagId": tag5Id, "tagName": "tag5", "tagNameShort": "tag5s", "categoryId": cat1Id}
    #             ]
    #         },
    #         {
    #             'categoryId': cat2Id,
    #             'categoryName': 'cat2',
    #             'tags': []
    #         },
    #         {
    #             'categoryId': cat3Id,
    #             'categoryName': 'cat3',
    #             'tags': [
    #                 { "tagId": tag1Id, "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat3Id },
    #                 { "tagId": tag3Id, "tagName": "tag3", "tagNameShort": "tag3s", "categoryId": cat3Id },
    #                 { "tagId": tag4Id, "tagName": "tag4", "tagNameShort": "tag4s", "categoryId": cat3Id }
    #             ]
    #         }
    #     ]
    #     assert response.json() == expected_response_body

    #     # TEST
    #     response = await adminClient.delete(f'/categories/{str(cat1Id)}')
    #     assert response.status_code == 204

    #     # POSTCONDITIONS
    #     response = await client.get('/tags')
    #     assert response.status_code == 200
    #     expected_response_body = [
    #         {
    #             'categoryId': cat2Id,
    #             'categoryName': 'cat2',
    #             'tags': []
    #         },
    #         {
    #             'categoryId': cat3Id,
    #             'categoryName': 'cat3',
    #             'tags': [
    #                 { "tagId": tag1Id, "tagName": "tag1", "tagNameShort": "tag1s", "categoryId": cat3Id },
    #                 { "tagId": tag3Id, "tagName": "tag3", "tagNameShort": "tag3s", "categoryId": cat3Id },
    #                 { "tagId": tag4Id, "tagName": "tag4", "tagNameShort": "tag4s", "categoryId": cat3Id }
    #             ]
    #         }
    #     ]
    #     assert response.json() == expected_response_body

    #     response = await client.get(f'/tag/{str(tag2Id)}')
    #     assert response.status_code == 404
    #     response = await client.get(f'/tag/{str(tag5Id)}')
    #     assert response.status_code == 404

    async def test_delete_category_as_user(self, userClient, adminClient, client):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        # TEST
        response = await userClient.delete(f'/categories/{str(cat1Id)}')
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

    async def test_delete_category_as_anon(self, client, adminClient):
        # PRECONDITIONS
        response = await adminClient.post('/categories', json={ "categoryName": "cat1" })
        assert response.status_code == 200
        cat1Id = (response.json())['categoryId']
        assert cat1Id

        # TEST
        response = await client.delete(f'/categories/{str(cat1Id)}')
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
