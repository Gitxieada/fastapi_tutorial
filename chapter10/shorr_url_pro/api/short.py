from fastapi import APIRouter, Depends,BackgroundTasks
from fastapi.responses import RedirectResponse, PlainTextResponse
from dependencies import get_db_session
from db.database import AsyncSession
from servies.short import ShortServeries

router_short = APIRouter(tags=["短链访问"])


@router_short.get('/{short_tag}')
async def short_redirect(*,short_tag: str, db_session: AsyncSession = Depends(get_db_session),taks:BackgroundTasks):
    data = await ShortServeries.get_short_url(db_session, short_tag)
    if not data:
        return PlainTextResponse("没有对应短链信息记录")
    data.visits_count=data.visits_count+1
    taks.add_task(ShortServeries.update_short_url,db_session,short_url_id=data.id,visits_count=data.visits_count)
    return RedirectResponse(url=data.long_url)