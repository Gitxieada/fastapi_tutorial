# from uuid import UUID
#
# import pytest
# from fastapi import status
# from httpx import AsyncClient
# import asyncio
#
# pytestmark = pytest.mark.anyio
#
#
#
# async def test_example(event_loop):
#     """No marker!"""
#     await asyncio.sleep(0)
#
#
# async def test_example222(event_loop):
#     """No marker!"""
#     await asyncio.sleep(3)
#
#
# # @pytest.mark.anyio
# async def test_hospital_info(client: AsyncClient):
#     response = await client.get("/api/v1/hospital_info")
#     print('response', response)
#     assert response.status_code == 200
#
#
# async def test_doctor_list(client: AsyncClient):
#     response = await client.get("/api/v1/doctor_list")
#     print('test_doctor_list', response)
#     assert response.status_code == 200

from fastapi.testclient import TestClient



def test_hospitalinfo(client:TestClient):
    res = client.get('/api/v1/hospital_info')
    print('sdsd',res.text)
    assert res.status_code == 200
    assert type(res.status_code) == int

def test_doctorlist(client:TestClient):
    res = client.get('/api/v1/doctor_list')
    print('dsasd',res.text)
    assert res.status_code == 200
    assert type(res.status_code) == int