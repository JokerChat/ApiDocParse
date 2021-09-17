# -*- coding: UTF-8 -*-

import uvicorn
from app import app
from starlette.staticfiles import StaticFiles

#挂载静态文件夹
app.mount("/static", StaticFiles(directory="static"), name="static")



if __name__ == "__main__":
    #reload 修改后自动重载
    #debug  开启debug模式
    uvicorn.run(app='main:app', host="0.0.0.0",port=8080,reload=True,debug=False)