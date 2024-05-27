from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Doctorinfo, DoctorScheduling, DoctorSubscribeinfo
from typing import Optional
from db.async_database import async_context_get_db

class PayOrderServeries:

    @staticmethod
    async def get_order_info_dno_orderid_visituopenid_state(async_session: AsyncSession, dno, visit_uopenid,
                                                            orderid)->DoctorSubscribeinfo:
        query = select(DoctorSubscribeinfo)
        # 查询当前医生排班信息归属
        query = query.where(DoctorSubscribeinfo.dno == dno, DoctorSubscribeinfo.visit_uopenid == visit_uopenid,
                            DoctorSubscribeinfo.orderid == orderid)
        _result = await async_session.execute(query)
        # 如果查询时整个模型的需要.scalar()
        # 如果是查询指定选择某些字段的是则不需要.scalar()
        # .scalar() 和 _result.scalars().first() 是一样效果
        return _result.scalars().first()



    @staticmethod
    async def get_doctor_info(async_session: AsyncSession, dno)->Doctorinfo:

        query = select( Doctorinfo.dnname,
                    Doctorinfo.pic,
                    Doctorinfo.dno,
                    Doctorinfo.rank,
                    Doctorinfo.fee,
                    Doctorinfo.destag,
                    Doctorinfo.describe)
        # 查询当前医生排班信息归属
        query = query.where(Doctorinfo.dno == dno)
        _result = await async_session.execute(query)
        return _result.first()



    @staticmethod
    async def get_doctor_scheduling_info_info_order(async_session: AsyncSession, dno, nsindex) -> DoctorScheduling:
        query = select(DoctorScheduling.dnotime,
                       DoctorScheduling.ampm,
                       DoctorScheduling.tiempm,
                       DoctorScheduling.dnotime,
                       DoctorScheduling.tiemampmstr,
                       )
        # 查询当前医生排班信息归属
        query = query.where(DoctorScheduling.dno == dno, DoctorScheduling.nsindex == nsindex)
        _result = await async_session.execute(query)
        return _result.first()

    @staticmethod
    async def get_order_info_byvisit_uopenid_state(async_session: AsyncSession, visit_uopenid, statue=1):
        '''
        判断是否存在存在未支付的订单
        :param async_session:  数据库会话对象
        :param visit_uopenid: 当前用户opendi
        :param statue: 订单状态（1:订单就绪，还没支付 2：已支付成功 3：取消订单
        :return:
        '''
        # # 判断是否存在
        #  stmt = select(User).where(User.name == 'sandy').exists()
        query = select(DoctorSubscribeinfo.id)
        # 查询当前医生排班信息归属
        query = query.where(DoctorSubscribeinfo.statue == statue, DoctorSubscribeinfo.visit_uopenid == visit_uopenid)
        _result = await async_session.execute(query)
        return _result.first()

    @staticmethod
    async def creat_order_info(async_session: AsyncSession, **kwargs):
        '''
        开始创建订单内容，并添加到数据库
        :param async_session:
        :param kwargs:
        :return:
        '''
        new_order = DoctorSubscribeinfo(**kwargs)
        async_session.add(new_order)
        await async_session.commit()
        # result.rowcount 1:成功 0 失败
        return new_order

    @staticmethod
    async def get_order_info_byorder_dno_state(async_session: AsyncSession, dno, orderid):
        # # 判断是否存在
        #  stmt = select(User).where(User.name == 'sandy').exists()
        query = select(DoctorSubscribeinfo.statue, DoctorSubscribeinfo.dno, DoctorSubscribeinfo.nsindex)
        _result = await async_session.execute(
            query.where(DoctorSubscribeinfo.dno == dno, DoctorSubscribeinfo.orderid == orderid))
        doctor_result: Optional[DoctorSubscribeinfo] = _result.first()
        return doctor_result

    @staticmethod
    async def updata_order_info_byorder_dno(async_session: AsyncSession, dno, orderid, visit_uopenid, **updata):
        # # 判断是否存在
        #  stmt = select(User).where(User.name == 'sandy').exists()
        query = update(DoctorSubscribeinfo)
        query = query.where(DoctorSubscribeinfo.dno == dno,
                            DoctorSubscribeinfo.orderid == orderid,
                            DoctorSubscribeinfo.visit_uopenid == visit_uopenid)
        result = await async_session.execute(query.values(updata))
        await async_session.commit()
        # result.rowcount 1:更新成功 0 更新失败
        return result.rowcount


if __name__ == '__main__':
    import asyncio
    async def sdsdf():
        async with async_context_get_db() as session:
            asdas = await PayOrderServeries.get_order_info_dno_orderid_visituopenid_state(session,
                                                                                          dno='10001',
                                                                                          visit_uopenid='orE7I56mAt_dvtRoXkMw-hY8FkwM',
                                                                                          orderid='2207081548588935269')
            print(asdas.orderid)


    # asyncio.run(sdsdf())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sdsdf())
