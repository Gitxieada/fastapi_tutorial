import pytest


@pytest.fixture(scope="session", autouse=True)
def action_01():
    print("session-类型作用域-前置条件")
    yield
    print("session-类型作用域-后置条件")


@pytest.fixture(scope="module", autouse=True)
def action_02():
    print("module-类型作用域-前置条件")
    yield
    print("module-类型作用域-后置条件")


# 生效的范围,类级别，每个类才会执行一次
@pytest.fixture(scope="class", autouse=True)
def action_03():
    print("class-类型作用域-前置条件")
    yield
    print("class-类型作用域-后置条件")

