from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi import FastAPI
from starlette.middleware.gzip import GZipMiddleware

app = FastAPI()

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"])

@app.get("/index")
async def truste():
    return {
        'code':200
    }

from fastapi import FastAPI
app.add_middleware(GZipMiddleware, minimum_size=1000)

app = FastAPI()

@app.get("/index")
async def gzip():
    return {
        'code':200
    }

if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
