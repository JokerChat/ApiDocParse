# -*- coding: utf-8 -*-

import json
from lxml import etree

class CreateJmx(object):


    @classmethod
    def jmeter_test_plan(cls, root_xml):
        """
        设置根节点
        :param root_xml: 根节点xml
        :return:
        """
        JmeterTestPlan = root_xml
        JmeterTestPlan.set('version', '1.2')
        JmeterTestPlan.set('properties', '5.0')
        JmeterTestPlan.set('jmeter', '5.1.1 r1855137')
        return etree.SubElement(JmeterTestPlan, 'hashTree')

    @classmethod
    def test_plan(cls, parent_xml, plan_name):
        """

        :param parent_xml: 父节点
        :param plan_name: 测试计划名称
        :return:
        """

        testPlan = etree.SubElement(parent_xml, 'TestPlan')
        testPlan.set("guiclass", "TestPlanGui")
        testPlan.set("testclass", "TestPlan")
        testPlan.set("testname", plan_name)
        testPlan.set("enabled", "true")
        stringProp = etree.SubElement(testPlan, "stringProp")
        stringProp.set("name", "TestPlan.comments")
        stringProp.text = ''
        boolProp1 = etree.SubElement(testPlan, "boolProp")
        boolProp1.set("name", "TestPlan.functional_mode")
        boolProp1.text = "false"
        boolProp2 = etree.SubElement(testPlan, "boolProp")
        boolProp2.set("name", "TestPlan.tearDown_on_shutdown")
        boolProp2.text = "false"
        boolProp3 = etree.SubElement(testPlan, "boolProp")
        boolProp3.set("name", "TestPlan.serialize_threadgroups")
        boolProp3.text = "true"
        elementProp = etree.SubElement(testPlan, "elementProp")
        elementProp.set("name", "TestPlan.user_defined_variables")
        elementProp.set("elementType", "Arguments")
        elementProp.set("guiclass", "ArgumentsPanel")
        elementProp.set("testclass", "Arguments")
        elementProp.set("testname", "User Defined Variables")
        elementProp.set("enabled", "true")
        collectionProp = etree.SubElement(elementProp, "collectionProp")
        collectionProp.set("name", "Arguments.arguments")
        stringProp2 = etree.SubElement(testPlan, "stringProp")
        stringProp2.set("name", "TestPlan.user_define_classpath")
        stringProp2.text = ''
        return etree.SubElement(parent_xml, 'hashTree')



    @classmethod
    def thread_group(cls, parent_xml):
        """

        :param parent_xml: 父节点
        :return:
        """
        theadGroup = etree.SubElement(parent_xml, "ThreadGroup")
        theadGroup.set("guiclass", "ThreadGroupGui")
        theadGroup.set("testclass", "ThreadGroup")
        theadGroup.set("testname", "Thread Group")
        theadGroup.set("enabled", "true")
        stringProp = etree.SubElement(theadGroup, "stringProp")
        stringProp.set("name", "ThreadGroup.on_sample_error")
        stringProp.text = "continue"
        elementProp = etree.SubElement(theadGroup, "elementProp")
        cls.common_api(elementProp,
                   {"name": "ThreadGroup.main_controller", "elementType": "LoopController",
                    "guiclass": "LoopControlPanel",
                    "testclass": "LoopController", "testname": "Loop Controller", "enabled": "true"})
        boolProp = etree.SubElement(elementProp, "boolProp")
        boolProp.set("name", "LoopController.continue_forever")
        boolProp.text = "false"
        stringProp = etree.SubElement(elementProp, "stringProp")
        stringProp.set("name", "LoopController.loops")
        stringProp.text = "1"
        stringProp = etree.SubElement(theadGroup, "stringProp")
        stringProp.set("name", "ThreadGroup.num_threads")
        stringProp.text = "1"
        stringProp = etree.SubElement(theadGroup, "stringProp")
        stringProp.set("name", "ThreadGroup.ramp_time")
        stringProp.text = "1"
        boolProp = etree.SubElement(theadGroup, "boolProp")
        boolProp.set("name", "ThreadGroup.scheduler")
        boolProp.text = "false"
        stringProp = etree.SubElement(theadGroup, "stringProp")
        stringProp.set("name", "ThreadGroup.duration")
        stringProp.text = ''
        stringProp = etree.SubElement(theadGroup, "stringProp")
        stringProp.set("name", "ThreadGroup.delay")
        stringProp.text = ''
        return etree.SubElement(parent_xml, "hashTree")



    @classmethod
    def arguments(cls, parent_xml):
        """
        设置arguments
        :param parent_xml: 父节点
        :return:
        """
        Arguments = etree.SubElement(parent_xml, "ThreadGroup")
        Arguments.set("guiclass", "ArgumentsPanel")
        Arguments.set("testclass", "Arguments")
        Arguments.set("testname", "User defined variables")
        Arguments.set("enabled", "true")
        collectionProp = etree.SubElement(Arguments, "collectionProp")
        collectionProp.set("name", "Arguments.arguments")
        return etree.SubElement(parent_xml, "hashTree")

    @classmethod
    def controller(cls, parent_xml, result):
        """
        创建HTTPsampler
        :param parent_xml: 父节点
        :param result: 接口数据，rap或者swagger
        :return:
        """
        for data in result:
            GenericController = etree.SubElement(parent_xml, "GenericController")
            GenericController.set("guiclass", "LogicControllerGui")
            GenericController.set("testclass", "GenericController")
            GenericController.set("testname", data.get("modules"))
            GenericController.set("enabled", "true")
            stringProp = etree.SubElement(GenericController, "stringProp")
            stringProp.set("name", "TestPlan.comments")
            stringProp.text = data.get("description")
            shashTree = etree.SubElement(parent_xml, "hashTree")
            for sample in data.get("cases_data"):
                HTTPSamplerProxy = etree.SubElement(shashTree, "HTTPSamplerProxy")
                cls.common_api(HTTPSamplerProxy,
                           {"guiclass": "HttpTestSampleGui", "testclass": "HTTPSamplerProxy",
                            "testname": sample.get('title'),
                            "enabled": "true"})
                if sample.get("data").__len__() < 1 and not sample.get("queryData"):
                    elementProp = etree.SubElement(HTTPSamplerProxy, "elementProp")
                    cls.common_api(elementProp, {"name": "HTTPsampler.Arguments", "elementType": "Arguments",
                                             "guiclass": "HTTPArgumentsPanel", "testclass": "Arguments",
                                             "testname": "User Defined Variables", "enabled": "true"})
                    collectionProp = etree.SubElement(elementProp, "collectionProp")
                    collectionProp.set("name", "Arguments.arguments")
                else:
                    boolProp = etree.SubElement(HTTPSamplerProxy, "boolProp")
                    boolProp.set("name", "HTTPSampler.postBodyRaw")
                    boolProp.text = "true"
                    elementProp = etree.SubElement(HTTPSamplerProxy, "elementProp")
                    cls.common_api(elementProp, {"name": "HTTPsampler.Arguments", "elementType": "Arguments"})
                    collectionProp = etree.SubElement(elementProp, "collectionProp")
                    collectionProp.set("name", "Arguments.arguments")
                    elementProp = etree.SubElement(collectionProp, "elementProp")
                    elementProp.set("name", "")
                    elementProp.set("elementType", "HTTPArgument")
                    boolProp = etree.SubElement(elementProp, "boolProp")
                    boolProp.set("name", "HTTPArgument.always_encode")
                    boolProp.text = "false"
                    stringProp = etree.SubElement(elementProp, "stringProp")
                    stringProp.set("name", "Argument.value")
                    # stringProp.text = json.dumps(sample.get("params")).replace("\"", "&quot;")
                    json_data = sample.get("data")
                    stringProp.text = json.dumps(json_data, ensure_ascii=False, indent=4)
                    stringProp = etree.SubElement(elementProp, "stringProp")
                    stringProp.set("name", "Argument.metadata")
                    stringProp.text = "="
                # host
                stringProp = etree.SubElement(HTTPSamplerProxy, "stringProp")
                stringProp.set("name", "HTTPSampler.domain")
                # stringProp.text = data.get("host")
                stringProp.text = data.get("")

                # port
                stringProp = etree.SubElement(HTTPSamplerProxy, "stringProp")
                stringProp.set("name", "HTTPSampler.port")
                # stringProp.text = data.get("port")
                stringProp.text = data.get("")

                # protocol
                stringProp = etree.SubElement(HTTPSamplerProxy, "stringProp")
                stringProp.set("name", "HTTPSampler.protocol")
                # stringProp.text = "http"
                stringProp.text = ""

                # encoding
                stringProp = etree.SubElement(HTTPSamplerProxy, "stringProp")
                stringProp.set("name", "HTTPSampler.contentEncoding")
                stringProp.text = "UTF-8"

                # path
                stringProp = etree.SubElement(HTTPSamplerProxy, "stringProp")
                stringProp.set("name", "HTTPSampler.path")
                stringProp.text = '${baseUrl}' + sample.get("url")

                # method
                stringProp = etree.SubElement(HTTPSamplerProxy, "stringProp")
                stringProp.set("name", "HTTPSampler.method")
                stringProp.text = sample.get("method").upper()

                # follow redirects
                boolProp = etree.SubElement(HTTPSamplerProxy, "boolProp")
                boolProp.set("name", "HTTPSampler.follow_redirects")
                boolProp.text = "true"

                # auto redirects
                boolProp = etree.SubElement(HTTPSamplerProxy, "boolProp")
                boolProp.set("name", "HTTPSampler.auto_redirects")
                boolProp.text = "false"

                # use keepalive
                boolProp = etree.SubElement(HTTPSamplerProxy, "boolProp")
                boolProp.set("name", "HTTPSampler.use_keepalive")
                boolProp.text = "true"

                # DO MULTIPART POST
                boolProp = etree.SubElement(HTTPSamplerProxy, "boolProp")
                boolProp.set("name", "HTTPSampler.DO_MULTIPART_POST")
                boolProp.text = "false"

                # embedded url re
                stringProp = etree.SubElement(HTTPSamplerProxy, "stringProp")
                stringProp.set("name", "HTTPSampler.embedded_url_re")
                stringProp.text = ""

                # connect timeout
                stringProp = etree.SubElement(HTTPSamplerProxy, "stringProp")
                stringProp.set("name", "HTTPSampler.connect_timeout")
                stringProp.text = ""

                # response timeout
                stringProp = etree.SubElement(HTTPSamplerProxy, "stringProp")
                stringProp.set("name", "HTTPSampler.response_timeout")
                stringProp.text = ""

                # comments
                stringProp = etree.SubElement(HTTPSamplerProxy, "stringProp")
                stringProp.set("name", "TestPlan.comments")
                stringProp.text = sample.get("description")
                hash_tree = etree.SubElement(shashTree, "hashTree")




    @classmethod
    def common_api(cls, obj_xml, datas):
        """
        循环set 父节点
        :param obj_xml:
        :param datas:
        :return:
        """
        for key, value in datas.items():
            obj_xml.set(key, value)



    @classmethod
    def conversion(cls, result, file_name):
        """
        转换主函数
        :param result: 接口数据
        :param file_name: 测试计划名
        :return:
        """
        jmeterTestPlan = etree.Element("jmeterTestPlan")
        hashTree = cls.jmeter_test_plan(jmeterTestPlan)
        testPlan = cls.test_plan(hashTree, file_name)
        threadGroup = cls.thread_group(testPlan)
        cls.controller(threadGroup, result)
        etree.tostring(jmeterTestPlan, encoding='UTF-8', pretty_print=True).decode()
        tree = etree.ElementTree(jmeterTestPlan)
        return tree


if __name__ == '__main__':
    pass
