from fastapi import Depends
from db.async_database import depends_get_db_session
from db.async_database import AsyncSession
from exts.responses.json_response import Success, Fail
from ..api import router_userorders
from ..schemas import SubscribeOrderCheckForm
from ..repository import Serveries


@router_userorders.put("/unpay_reserve_order", summary='取消订单支付')
async def callbadk(forms: SubscribeOrderCheckForm, db_session: AsyncSession = Depends(depends_get_db_session)):
    # 检测订单的状态
    doctor_nsnum_info_result = await Serveries.get_order_info_byorder_dno_state(db_session, dno=forms.dno,
                                                                                orderid=forms.orderid)
    if not doctor_nsnum_info_result:
        return Fail(api_code=200, result=None, message='暂无此订单记录信息！')

    if doctor_nsnum_info_result.statue == 3:
        pass
        # 订单状态（1:订单就绪，还没支付 2：已支付成功 3：取消订单 4：超时未支付订单）
        return Fail(api_code=200, result=None, message='订单已操作过取消！请勿重复操作！')

    if doctor_nsnum_info_result.statue == 4:
        pass
        # 订单状态（1:订单就绪，还没支付 2：已支付成功 3：取消订单 4：超时未支付订单）
        return Fail(api_code=200, result=None, message='订单已过有效期！不可操作！')

    if doctor_nsnum_info_result.statue == 2:
        pass
        # 订单状态（1:订单就绪，还没支付 2：已支付成功 3：取消订单 4：超时未支付订单）
        return Fail(api_code=200, result=None, message='该订单已支付成功！如需取消,请申请操作退款！')

    if doctor_nsnum_info_result.statue == 5:
        pass
        # 订单状态（1:订单就绪，还没支付 2：已支付成功 3：取消订单 4：超时未支付订单）
        return Fail(api_code=200, result=None, message='该订单处于申请退款状态,请勿重复操作！')

        # 更新没有支付的成功的订单的，状态！
    isok = await Serveries.updata_order_info_byorder_dno_olny(db_session, dno=forms.dno,
                                                              orderid=forms.orderid,
                                                              visit_uopenid=forms.visit_uopenid,
                                                              statue=3
                                                              )

    return Success(api_code=200, result=None, message='订单取消成功') if isok else Fail(api_code=200, result=None,
                                                                                  message='订单取消失败')
