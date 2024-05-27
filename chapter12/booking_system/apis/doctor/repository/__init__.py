from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Doctorinfo, DoctorScheduling,DoctorSubscribeinfo
from typing import Optional
from utils.datatime_helper import str_to_datatime, datatime_to_str, datetime


class DoctorServeries:

    @staticmethod
    async def get_doctor_list_infos(async_session: AsyncSession, enable: int = 1):
        # options(Doctor.dno,Doctor.dnname,Doctor.fee,Doctor.pic,Doctor.rank)
        # query =select(Doctor).with_only_columns(Doctor.dno,Doctor.dnname,Doctor.fee,Doctor.pic,Doctor.rank)
        # # 判断是否存在
        #  stmt = select(User).where(User.name == 'sandy').exists()
        query = select(Doctorinfo.dno, Doctorinfo.dnname, Doctorinfo.fee, Doctorinfo.pic, Doctorinfo.rank)
        _result = await async_session.execute(query.where(Doctorinfo.enable == enable))
        # 调用.scalars()这样会返回的是标量值，不是ROW==
        return _result.all()

    @staticmethod
    async def get_doctor_scheduling_info(async_session: AsyncSession, dno, enable: int = 1, start_time=None):
        '''
        返回预约医生的排班信息
        :param async_session:
        :param enable:
        :param start_time: 当前医生的排班时间起点 默认查询当天的时间排班
        :param end_time:  当前医生的排班截止时间点 默认查询当天的时间排班
        :return:
        '''
        # 获取排班信息
        # 查询出当前医生的信息
        query = select(Doctorinfo.dno, Doctorinfo.dnname, Doctorinfo.destag, Doctorinfo.pic, Doctorinfo.rank, Doctorinfo.describe)
        _result = await async_session.execute(query.where(Doctorinfo.enable == enable, Doctorinfo.dno == dno))
        doctor_result: Optional[Doctorinfo] = _result.first()
        # 再查询当前医生下面分开上午 和下午的排班信息
        doctor_scheduling_result = []
        if doctor_result:
            query = select(DoctorScheduling.nsindex,
                           DoctorScheduling.nsnum,
                           DoctorScheduling.ampm,
                           DoctorScheduling.dnotime,
                           DoctorScheduling.tiempm,
                           DoctorScheduling.nsnumstock,
                           DoctorScheduling.tiemampmstr)
            # 查询当前医生排班信息归属
            query = query.where(DoctorScheduling.enable == enable, DoctorScheduling.dno == dno)

            if start_time:
                # 格式化时间处理
                start_time = str_to_datatime(start_time)
                end_time = str_to_datatime(datatime_to_str((start_time + datetime.timedelta(days=1))))
            else:
                # 格式化时间处理
                start_time = str_to_datatime(datatime_to_str(datetime.datetime.now()))
                end_time = str_to_datatime(datatime_to_str((datetime.datetime.now() + datetime.timedelta(days=1))))


            query = query.where(DoctorScheduling.dnotime >= start_time, DoctorScheduling.dnotime < end_time)

            _result = await async_session.execute(query)
            doctor_scheduling_result = _result.all()
        return doctor_result, doctor_scheduling_result

    @staticmethod
    async def get_doctor_curr_nsindex_scheduling_info(async_session: AsyncSession, dno, nsindex, enable: int = 1):
        query = select(Doctorinfo.dno, Doctorinfo.dnname, Doctorinfo.pic, Doctorinfo.rank, Doctorinfo.addr,Doctorinfo.fee)
        _result = await async_session.execute(query.where(Doctorinfo.enable == enable, Doctorinfo.dno == dno))
        doctor_result: Optional[Doctorinfo] = _result.first()
        # 再查询当前医生下面分开上午 和下午的排班信息
        doctor_nsnuminfo_result: Optional[DoctorScheduling] = None
        if doctor_result:
            query = select(DoctorScheduling.nsindex,
                           DoctorScheduling.ampm,
                           DoctorScheduling.dnotime,
                           DoctorScheduling.nsnum,
                           DoctorScheduling.nsnumstock,
                           DoctorScheduling.tiempm,
                           DoctorScheduling.tiemampmstr)
            # 查询当前医生排班信息归属
            query = query.where(DoctorScheduling.enable == enable, DoctorScheduling.dno == dno,
                                DoctorScheduling.nsindex == nsindex)

            _result = await async_session.execute(query)
            doctor_nsnuminfo_result = _result.first()

        return doctor_result, doctor_nsnuminfo_result

    @staticmethod
    async def updata_nusnum_info_dno(async_session: AsyncSession, dno, nsindex,isup=True):
        response = update(DoctorSubscribeinfo).where(DoctorScheduling.dno == dno, DoctorScheduling.nsindex == nsindex)
        if isup:
            result = await async_session.execute(response.values(use_nsnum=DoctorScheduling.use_nsnum + 1))
        else:
            result = await async_session.execute(response.values(use_nsnum=DoctorScheduling.use_nsnum - 1))
        await async_session.commit()
        return result.rowcount
