import pytest
import pytest_asyncio
from httpx import AsyncClient
import asyncio
import sys
from db.async_database import async_engine
# 需要加载当前项目目录。sys.path.append('E://yuanxiao//code//booking_system//booking_system')，
# 不然在项目根目录执行pytest会出现ModuleNotFoundError: No module named 'app'
sys.path.append('E://yuanxiao//code//booking_system//booking_system')
from app import app

# ===========================================同步使用

from typing import Dict, Generator
import pytest
from fastapi.testclient import TestClient
@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


# ===========================================异步使用

# 修改设置优先循环事件
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# 配置使用哪一种模式的异步
@pytest.fixture(
    params=[
        pytest.param(("asyncio", {"use_uvloop": True}), id="asyncio+uvloop"),
    ]
)
def anyio_backend(request):
    return request.param

# 解决当接口中涉及到依赖注入的数据库使用
async def start_db():
    async with async_engine.begin() as conn:
        pass
    await async_engine.dispose()

@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    async with AsyncClient(app=app,base_url="http://test", headers={"Content-Type": "application/json"},) as async_client:
        await start_db()
        yield async_client
        await async_engine.dispose()