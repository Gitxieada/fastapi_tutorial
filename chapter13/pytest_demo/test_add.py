import pytest
from cast_helper import add


class TestMyAddClass:


    def setup(self):
        print("setup前置条件")

    def teardown(self):
        print("teardown后置条件")

    def setup_class(self):
        print("前置条件")

    def teardown_class(self):
        print("后置条件")

    def test_add(self):
        assert 3 == 3

    def test_add_v2(self):
        assert 3 == 5

if __name__ == "__main__":
    pytest.main(['-q'])
