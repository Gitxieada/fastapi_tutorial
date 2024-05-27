import random

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cprofile.profiler import CProfileMiddleware

app = FastAPI()

# app.add_middleware(CProfileMiddleware)
# app.add_middleware(CProfileMiddleware, enable=True, print_each_request = True, strip_dirs = False, sort_by='cumulative')
app.add_middleware(CProfileMiddleware, enable=True, server_app = app, filename='.prof', strip_dirs = False, sort_by='cumulative')
import asyncio
@app.get("/")
async def main():
    def randomlist(n):
        lists = []
        l = [random.random() for i in range(n)]
        l.sort()
        for v in l:
            lists.append(v)
        return lists

    await asyncio.sleep(10)
    randomlist(10)
    return {"message": "Hello World"}



if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
