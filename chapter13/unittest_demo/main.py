# unittest导入
import unittest

# 定义测试类
class UnitTestForAdd(unittest.TestCase):
    # 测试用例运行之前
    def setUp(self) -> None:
        print('前置条件')

    # 测试用例运行之后
    def tearDown(self) -> None:
        print('后置条件')
        # 定义测试用例


    def test_add(self):
        self.assertEqual(3,3)

if __name__ == '__main__':
    unittest.main()