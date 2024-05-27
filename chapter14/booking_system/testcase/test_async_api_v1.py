# import pytest
#
# @pytest.mark.anyio
# @pytest.mark.parametrize('anyio_backend', ['asyncio'])
# async def test_index(async_client):
#     res = await async_client.get("/index")
#     assert res.status_code == 200
#     assert type(res.status_code) == int
#
# @pytest.mark.anyio
# @pytest.mark.parametrize('anyio_backend', ['asyncio'])
# async def test_index2(async_client):
#     res = await async_client.get("/index2")
#     assert res.status_code == 200
#     assert type(res.status_code) == int

import pytest

@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_doctor_list(async_client):
    res = await async_client.get("/api/v1/doctor_list")
    assert res.status_code == 200
    assert type(res.status_code) == int


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_hospital_info(async_client):
    res = await async_client.get("/api/v1/hospital_info")
    assert res.status_code == 200
    assert type(res.status_code) == int
