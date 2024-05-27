from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.baidu.com",
    "https://localhost.qq.com",
    "http://localhost",
    "http://localhost:8080",
]

# 添加自定义中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}



if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
