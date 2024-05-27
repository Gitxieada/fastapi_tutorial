from functools import wraps

from fastapi import FastAPI,Request
from fastapi.responses import PlainTextResponse
from fastapi.params import Body


app = FastAPI()


@app.post("/get/access_token")
def access_token(request:Request,name=Body(...)):
    # print(reques.body())
    from asgiref.sync import async_to_sync
    body = async_to_sync(request.body)()
    print(body)
    return PlainTextResponse(body.decode(encoding='utf-8'))


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host="127.0.0.1", port=8100, debug=True, reload=True)