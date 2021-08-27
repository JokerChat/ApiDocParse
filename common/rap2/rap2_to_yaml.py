# -*- coding: utf-8 -*-
# @Author       :junjie
# @Time         :2021/7/31 16:44
# @FileName     :rap2_to_yaml.py
#IDE            :PyCharm

import yaml
import zipfile
import uuid
import time
from utils.FILE_PATH import DOWNLOAD_PATH
from common.rap2.rap2_parse import Rap2Parse

class RapToYaml(object):

    @classmethod
    def to_yaml(cls, id, cookies=None, module=None):
        #获取接口文档的数据
        data_list, name = Rap2Parse.api_data(id, cookies, module)
        #设置文件名
        file_name = f"{name}-{uuid.uuid4().hex}.zip"
        #创建一个zip文件对象，压缩时mode为w
        with zipfile.ZipFile(f"{DOWNLOAD_PATH}/{file_name}", 'w') as z:
            #分模块写入数据
            for data in data_list:
                time_str = str(round(time.time() * 1000))
                #避免重复,拼接时间戳
                yaml_name = f"{data['modules']}-{time_str}.yaml"
                yaml_path = f"{DOWNLOAD_PATH}/{yaml_name}"
                with open(yaml_path, "w", encoding="utf-8") as f:
                    #default_flow_style 关闭flow流格式
                    #sort_keys 关闭ascii排序
                    #allow_unicode 支持写入中文
                    yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
                #第一个参数为文件路径，第二个参数为添加到zip后保存的名称
                z.write(yaml_path,yaml_name)
        return file_name



if __name__ == '__main__':
    result = RapToYaml.to_yaml(407)
    print(result)