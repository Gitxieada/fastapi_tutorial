import pytest

data = ["superadmin", "admin","common"]

@pytest.fixture(scope="function",name='user_role_fixture', params=data,autouse=True)
def user_role(request):
    print("当前用例使用的参数：",request.param)
    return request.param

def test_get_user_role(user_role_fixture):
    print(f"获取当前用户角色:{user_role_fixture}")


if __name__ == "__main__":
    pytest.main()