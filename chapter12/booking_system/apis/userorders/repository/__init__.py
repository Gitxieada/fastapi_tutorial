import asyncio

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult
from db.models import Doctorinfo, DoctorSubscribeinfo, DoctorScheduling
from db.async_database import async_context_get_db
from typing import Optional






class Serveries:

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
    async def updata_order_info_byorder_dno_olny(async_session: AsyncSession, dno, visit_uopenid, orderid, **updata):
        response = update(DoctorSubscribeinfo).where(DoctorSubscribeinfo.dno == dno,
                                                     DoctorSubscribeinfo.visit_uopenid == visit_uopenid,
                                                     DoctorSubscribeinfo.orderid == orderid)
        result = await async_session.execute(response.values(updata))
        await async_session.commit()
        return result.rowcount

    @staticmethod
    async def updata_order_info_byorder_dno_olny_dict(async_session: AsyncSession, dno, visit_uopenid, orderid,
                                                      updata={}):
        response = update(DoctorSubscribeinfo).where(DoctorSubscribeinfo.dno == dno,
                                                     DoctorSubscribeinfo.visit_uopenid == visit_uopenid,
                                                     DoctorSubscribeinfo.orderid == orderid)
        result = await async_session.execute(response.values(**updata))
        await async_session.commit()
        return result.rowcount

    @staticmethod
    async def get_order_info_list_by_visit_uopenid_select(async_session: AsyncSession, visit_uopenid, statue=1) -> list:
        query_subscribe_info = select(
            DoctorSubscribeinfo.orderid,
            # 订单状态（1:订单就绪，还没支付 2：已支付成功 3：取消订单 4:超时自动取消）
            DoctorSubscribeinfo.statue,
            DoctorSubscribeinfo.dno,
            DoctorSubscribeinfo.visittime,
            DoctorSubscribeinfo.visitday,
            DoctorSubscribeinfo.payfee,
            DoctorSubscribeinfo.visit_statue,
            Doctorinfo.dnname,
            Doctorinfo.addr,
            Doctorinfo.rank,
            Doctorinfo.pic
        ).outerjoin_from(DoctorSubscribeinfo, Doctorinfo, DoctorSubscribeinfo.dno == Doctorinfo.dno) \
            .filter(DoctorSubscribeinfo.visit_uopenid == visit_uopenid,
                    DoctorSubscribeinfo.statue == statue,
                    )

        _subscribe_info_result:AsyncResult = await async_session.execute(query_subscribe_info)
        _rows = _subscribe_info_result.mappings()
        return [_row for _row in _rows]

        # 几个关键的属性值信息：
        # _row默认只是输出了self._data
        # 如果需要对应的键则是self._fields或_keymap
        # 如果是直接的返回字典的话_asdict 或_mapping 但是_asdict 其实是return dict(self._mapping)
        # 第一种方式
        # from sqlalchemy.engine.row import Row
        # 第二张方式:
        # from sqlalchemy.engine.row import Row
        # _rows = _subscribe_info_result.all()
        # return [item._mapping for item in _rows]




    @staticmethod
    async def get_order_info_list_by_visit_uopenid_detailt(async_session: AsyncSession, visit_uopenid, orderid,
                                                           dno) -> dict:
        query_subscribe_info = select(
            DoctorSubscribeinfo.orderid,
            # 订单状态（1:订单就绪，还没支付 2：已支付成功 3：取消订单 4:超时自动取消）
            DoctorSubscribeinfo.statue,
            DoctorSubscribeinfo.dno,
            DoctorSubscribeinfo.visittime,
            DoctorSubscribeinfo.visitday,
            DoctorSubscribeinfo.payfee,
            DoctorSubscribeinfo.visit_statue,
            Doctorinfo.addr,
            Doctorinfo.dnname,
            Doctorinfo.rank,
            Doctorinfo.pic,
            DoctorSubscribeinfo.create_time,
            DoctorSubscribeinfo.visit_uname,
            DoctorSubscribeinfo.visit_uphone,
            DoctorSubscribeinfo.visit_usex,
            DoctorSubscribeinfo.visit_uage,
        ).outerjoin_from(DoctorSubscribeinfo, Doctorinfo, DoctorSubscribeinfo.dno == Doctorinfo.dno) \
            .filter(DoctorSubscribeinfo.visit_uopenid == visit_uopenid,
                    DoctorSubscribeinfo.orderid == orderid,
                    DoctorSubscribeinfo.dno == dno
                    )
        _subscribe_info_result = await async_session.execute(query_subscribe_info)
        _row = _subscribe_info_result.first()
        return {} if not _row else _row._mapping
        # return {} if not _row else {
        #     'orderid': _row[0],
        #     'statue': _row[1],
        #     'dno': _row[2],
        #     'visittime': _row[3],
        #     'visitday': _row[4],
        #     'payfee': _row[5],
        #     'visit_statue': _row[6],
        #     'dnname': _row[7],
        #     'addr': _row[8],
        #     'rank': _row[9],
        #     'pic': _row[10],
        #     'create_time': _row[11],
        #     'visit_uname': _row[12],
        #     'visit_uphone': _row[13],
        #     'visit_usex': _row[14],
        #     'visit_uage': _row[15]
        # }


if __name__ == '__main__':
    async def sdsdf():
        async with async_context_get_db() as session:
            asdas = await Serveries.get_order_info_list_by_visit_uopenid_select(session,
                                                                                visit_uopenid='orE7I59UwXdWzfSK9QGK2fHGtPZ8')
            print(asdas)


    # asyncio.run(sdsdf())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sdsdf())
