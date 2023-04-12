import pytest

pytestmark = pytest.mark.anyio

class TestStatistics:

    async def test_permissions(self, client, userClient, adminClient):
        response = await client.get('/statistics/visits')
        assert response.status_code == 401
        response = await userClient.get('/statistics/visits')
        assert response.status_code == 403
        response = await adminClient.get('/statistics/visits')
        assert response.status_code == 200

        params = { 'num_days': 5 }
        response = await client.get('/statistics/projectupdates/count', params=params)
        assert response.status_code == 401
        response = await userClient.get('/statistics/projectupdates/count', params=params)
        assert response.status_code == 403
        response = await adminClient.get('/statistics/projectupdates/count', params=params)
        assert response.status_code == 200

        params = { 'n': 5 }
        response = await client.get('/statistics/tags/popular', params=params)
        assert response.status_code == 401
        response = await userClient.get('/statistics/tags/popular', params=params)
        assert response.status_code == 403
        response = await adminClient.get('/statistics/tags/popular', params=params)
        assert response.status_code == 200
        