# from uuid import UUID
#
import pytest
from httpx import AsyncClient
pytestmark = pytest.mark.anyio

async def test_hospital_info(async_client: AsyncClient):
    response = await async_client.get("/api/v1/hospital_info")
    print('response', response.text)
    assert response.status_code == 200


async def test_doctor_list(async_client: AsyncClient):
    response = await async_client.get("/api/v1/doctor_list")
    print('response', response.text)
    assert response.status_code == 200