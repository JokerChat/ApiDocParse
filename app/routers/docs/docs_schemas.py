# -*- coding: UTF-8 -*-

from pydantic import BaseModel,validator,Field

#创建数据模型
class Rap2Body(BaseModel):
    projectId : int=Field(..., title="rap2项目id",description="必传")
    moduleName : str=Field(None, title="模块名",description="不传默认全部")
    type : int=Field(..., title="导出格式",description="1-Excel，2-yaml，3-jmx")
    cookies : str=Field(None, title="cookies数据",description="不传使用默认账号")


    @validator('type')
    def typeDict(cls, value):
        if value not in [1, 2, 3]:
            raise ValueError('类型有误')
        return value


    @validator('projectId','type','moduleName')
    def checkEmpty(cls, value):
        if value == '':
            raise ValueError('必须有值')
        return value


class SwaggerBody(BaseModel):
    url : str=Field(..., title="swagger地址",description="必传")
    moduleName : str = Field(None, title="模块名",description="不传默认全部")
    type : int =Field(..., title="导出格式",description="1-Excel，2-yaml，3-jmx")


    @validator('type')
    def typeDict(cls, value):
        if value not in [1, 2, 3]:
            raise ValueError('类型有误')
        return value


    @validator('url','type','moduleName')
    def checkEmpty(cls, value):
        if value == '':
            raise ValueError('必须有值')
        return value