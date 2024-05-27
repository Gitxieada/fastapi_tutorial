#!/usr/bin/evn python
# coding=utf-8
# + + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + +
#        ┏┓　　　┏┓+ +
# 　　　┏┛┻━━━┛┻┓ + +
# 　　　┃　　　　　　 ┃ 　
# 　　　┃　　　━　　　┃ ++ + + +
# 　　 ████━████ ┃+
# 　　　┃　　　　　　 ┃ +
# 　　　┃　　　┻　　　┃
# 　　　┃　　　　　　 ┃ + +
# 　　　┗━┓　　　┏━┛
# 　　　　　┃　　　┃　　　　　　　　　　　
# 　　　　　┃　　　┃ + + + +
# 　　　　　┃　　　┃　　　　Codes are far away from bugs with the animal protecting　　　
# 　　　　　┃　　　┃ + 　　　　神兽保佑,代码无bug　　
# 　　　　　┃　　　┃
# 　　　　　┃　　　┃　　+　　　　　　　　　
# 　　　　　┃　 　　┗━━━┓ + +
# 　　　　　┃ 　　　　　　　┣┓
# 　　　　　┃ 　　　　　　　┏┛
# 　　　　　┗┓┓┏━┳┓┏┛ + + + +
# 　　　　　　┃┫┫　┃┫┫
# 　　　　　　┗┻┛　┗┻┛+ + + +
# + + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + +"""
"""
Author = zyx
@Create_Time: 2018/2/27 18:07
@version: v1.0.0
@Contact: 308711822@qq.com
@File: ordernum_helper.py
@文件功能描述:
"""
import time
import random


def order_num_1(package_id=12345, user_num=56789):
    # 商品id后1位+下单时间的年月日12+用户2后四位+随机数3位
    local_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))[2:]
    result = str(package_id)[-2:] + local_time + str(user_num)[-2:] + str(random.randint(100, 999))
    return result


def order_num_2(package_id=12345, user_num=56789):
    # 商品id后2位+下单时间的年月日12+用户2后四位+随机数4位
    local_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))[2:]
    result = str(package_id)[-2:] + local_time + str(user_num)[-2:] + str(random.randint(1000, 9999))
    return result


def order_num_3(user_num=56789):
    # 商品id后2位+下单时间的年月日12+用户2后四位+随机数4位
    local_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))[2:]
    result =f'{local_time}{str(user_num)[-2:] }{random.randint(10000, 99999)}'
    return result


def order_num_srt(user_num='56789'):
    # 商品id后2位+下单时间的年月日12+用户2后四位+随机数4位
    local_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))[2:]
    result =str(user_num)[-2:] + str(random.randint(100, 999)) + local_time +  str(random.randint(1000, 9999))
    return result
