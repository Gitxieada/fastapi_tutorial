from datetime import timedelta
import time

import datetime


def effectiveness_tiempm(tiempm):
    today = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())).replace("-", "")
    todaydate = datetime.datetime.strptime(today, "%Y%m%d %H:%M")  # 字符串转化为date形式
    # 预约时段的时间
    yuyue_day = tiempm.replace("-", "")
    yuyue_daydate = datetime.datetime.strptime(yuyue_day, "%Y%m%d %H:%M:%S")  # 字符串转化为date形式
    # 超出预约时间范围
    if todaydate >= yuyue_daydate:
        return False
    return True



def get_timestamp10():
    """获取当前时间长度为10位长度的时间戳"""
    return int(time.time())


def str_to_datatime(srr_time, strftime="%Y-%m-%d"):
    print('strftimestrftimestrftime',strftime)
    return datetime.datetime.strptime(srr_time, strftime)

str_to_datatime('2021-12-27 10:00:00',strftime='%Y-%m-%d %H:%M:%S')

def datatime_to_str(data_time: datetime.datetime, strftime="%Y-%m-%d"):
    return data_time.strftime(strftime)


def diff_days_for_now_time(srr_time):
    '''
    对比当前的传入日期和当前系统时间的相差的天数
    :param srr_time:
    :return:
    '''
    return (datetime.datetime.strptime(srr_time, "%Y-%m-%d") - datetime.datetime.combine(datetime.datetime.now().date(),
                                                                                         datetime.time())).days


# 获取当前日期
# today=time.strftime('%Y-%m-%d',time.localtime(time.time()))

def currday_time_info():
    return time.strftime('%Y-%m-%d', time.localtime(time.time()))


def currday_time_info_tochane_datetime(today):
    str = today.replace("-", "")
    return datetime.datetime.strptime(str, "%Y%m%d")  # 字符串转化为date形式


def effectiveness_tiempm(tiempm):
    today = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())).replace("-", "")
    todaydate = datetime.datetime.strptime(today, "%Y%m%d %H:%M")  # 字符串转化为date形式
    # 预约时段的时间
    yuyue_day = tiempm.replace("-", "")
    yuyue_daydate = datetime.datetime.strptime(yuyue_day, "%Y%m%d %H:%M:%S")  # 字符串转化为date形式
    # 超出预约时间范围
    if todaydate >= yuyue_daydate:
        return False
    return True


# 根据给定的日期，获取前n天或后n天的日期，n为正数则是以后的n天，n为负数则是以前的n天,不包括当天
def get_day_of_day(str2date, n=0):
    if (n < 0):
        n = abs(n)
        return (str2date - timedelta(days=n))
    else:
        return str2date + timedelta(days=n)


def num_to_string(num):
    numbers = {
        7: "周日",
        1: "周一",
        2: "周二",
        3: "周三",
        4: "周四",
        5: "周五",
        6: "周六"
    }
    return numbers.get(num, None)


def get_7day_info_list(num=6):
    today = currday_time_info()
    ditcs = dict()
    for i in range(num + 1):
        datatime = get_day_of_day(currday_time_info_tochane_datetime(today), i)
        ditcs[datatime.strftime('%Y-%m-%d')] = {
            'weekday': num_to_string(datatime.isoweekday()),
            'datetimeday': datatime.strftime('%Y-%m-%d')
        }
    return ditcs


def get_7day_info_list_only_data(num=6):
    today = currday_time_info()
    ditcs = dict()
    for i in range(num + 1):
        datatime = get_day_of_day(currday_time_info_tochane_datetime(today), i)
        ditcs[datatime.strftime('%Y-%m-%d')] = {}
    return ditcs

