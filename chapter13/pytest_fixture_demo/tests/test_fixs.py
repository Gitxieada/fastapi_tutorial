import pytest


def setup():
    print('setup 用例开始前执行')

def teardown():
    print('teardown 用例结束后执行')

# 定义一个前后置方法
@pytest.fixture
def my_first_fixture():
    print("前置方法")
    yield
    print("后置方法")


# 定义测试用例
def test_cast_1(my_first_fixture):
    print("开始执行cast_1测试用例")
    assert 3 == 3


# 定义测试用例
def test_cast_2(my_first_fixture):
    print("开始执行cast_2测试用例")
    assert 3 == 3


if __name__ == "__main__":
    pytest.main()
