# -*- coding: utf-8 -*-

import yaml
import zipfile
import uuid
import time
from utils.FILE_PATH import DOWNLOAD_PATH

class ToYaml(object):

    @classmethod
    def to_yaml(cls, name, data_list):
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
    result = ToYaml.to_yaml(407,{})
    print(result)