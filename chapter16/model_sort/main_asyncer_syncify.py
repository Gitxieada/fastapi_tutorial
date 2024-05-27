from fastapi import FastAPI

app = FastAPI()

from pydantic import BaseModel
from typing import Optional


class Item(BaseModel):

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        # 对当前__fields__重新进行排序
        cls.__fields__ = {key: cls.__fields__[key] for key in sorted(cls.__fields__.keys())}
        return instance

    desc: Optional[str] = None
    price: str
    age: str
    aname: str


@app.post('/items/', response_model=Item)
async def getitem(item: Item):
    return item


if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", reload=True)
