import fastapi
import pydantic
import typing
import abc

class PluginBase(abc.ABC):

    def __init__(self,app: fastapi.FastAPI = None,config: pydantic.BaseSettings = None):
        if app is not None:
            self.init_app(app)

    @abc.abstractmethod
    def init_app(self,app: fastapi.FastAPI,config: pydantic.BaseSettings = None,*args,**kwargs) -> None:
        raise NotImplementedError('需要实现初始化')
