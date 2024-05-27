from fastapi import FastAPI,Request
from fastapi.responses import PlainTextResponse
from fastapi.params import Body
from fastapi.background import  BackgroundTasks
from asyncer import asyncify,syncify

app = FastAPI()

@app.post("/get/access_token")
def access_token(request:Request,name=Body(...)):
    body = syncify(request.body)()
    print(body)
    return PlainTextResponse(body.decode(encoding='utf-8'))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host="127.0.0.1", port=8100, debug=True, reload=True)

