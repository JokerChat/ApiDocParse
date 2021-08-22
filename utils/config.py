# -*- coding: UTF-8 -*-




class DoMain(object):
    """域名配置"""
    RAP = 'https://rap2api.bluemoon.com.cn'

class UrlConfig(DoMain):
    """Url配置"""
    RAP_CODE_URL = DoMain.RAP + '/captcha?t=1626914290792'
    RAP_LOGIN_URL = DoMain.RAP + '/account/login'
    RAP_PROJRCT_URL = DoMain.RAP + '/repository/get'


class Account(object):
    RAP = {
    "email": "fangjunjie@bluemoon.com.cn",
    "password": "fangjunjie1996"
  }
    OCR = [
        {
            "app_id": "24586169",
            "api_key": "1W3ZkAMpCb9qDty3acKg13XK",
            "secret_key": "wBjeMXGV7o4QtfEhZfkB71OX3BA6TgyU"
        }
    ]


