from fastapi import Depends
from db.async_database import depends_get_db_session
from db.async_database import AsyncSession
from exts.responses.json_response import Success, Fail
from ..api import router_userorders
from ..schemas import UserOrderIonfoListForm
from ..repository import Serveries

@router_userorders.post("/user_order_list", summary='用户自己订单列表')
async def callbadk(forms: UserOrderIonfoListForm, db_session: AsyncSession = Depends(depends_get_db_session)):
    # 检测用户的有消息
    # 判断当前用户是否已经被拉黑啦，禁用了！
    result = await Serveries.get_order_info_list_by_visit_uopenid_select(db_session,visit_uopenid=forms.visit_uopenid,statue=forms.statue)
    # is_reserve -属性 1:表示可以点击预约  2：有排班记录，但是已预约满
    return Success(api_code=200, result=result, message='查询成功') if result else Fail(api_code=200, result=None, message='无此订单状态列表信息！')
