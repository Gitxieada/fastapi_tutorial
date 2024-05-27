import pytest

# 字典列表
data = ["superadmin", "admin", "common"]
data2 = ["superadmin2", "admin2", "common2"]

@pytest.mark.parametrize("request_data", data)
def test_get_user_role(request_data):
    print(f"获取当前用户角色:{request_data}")

@pytest.mark.parametrize("data",data)
@pytest.mark.parametrize("data2",data2)
def test_a(data,data2):
    print(f"测试参数组合，data:{data},data2:{data}")


if __name__ == "__main__":
    pytest.main()
