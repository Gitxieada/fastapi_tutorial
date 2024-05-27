import pytest


@pytest.mark.parametrize("role_name,age", [("superadmin",45), ("admin",4), ("common",6)])
class TestGetUserRole:
    def test_get_user_role(self,role_name,age):
        print(f"获取当前用户角色:{role_name,age}")

if __name__ == "__main__":
    pytest.main()