#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

from __future__ import print_function, absolute_import

import subprocess
from modules.exploit import TSExploit



__all__ = ['TangScan']


class TangScan(TSExploit):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.info = {
            "name": "bind 畸形tkey漏洞，可以远程导致DNS拒绝服务",
            "product": "bind",
            "product_version": "9.1.0 -> 9.8.x, 9.9.0->9.9.7-P1, 9.10.0->9.10.2-P2",
            "desc": "bind 畸形tkey漏洞，可以远程导致DNS拒绝服务",
            "license": self.license.TS,
            "author": "PyNerd",
            "ref": [
                {self.ref.url: "http://drops.wooyun.org/运维安全/123123"}
            ],
            "type": self.type.patch,
            "severity": self.severity.high,
            "privileged": False,
            "disclosure_date": "2010-01-01",
            "create_date": "2014-12-25"
        }

        self.register_option({
            "host": {
                "default": "",
                "required": True,
                "choices": [],
                "convert": self.convert.str_field,
                "desc": '''
                    目标主机
                '''
            },
            "port": {
                "default": 53,
                "required": False,
                "choices": [],
                "convert": self.convert.int_field,
                "desc": '''
                    目标端口
                '''
            }
        })

        self.register_result({
            "status": False,
            "data": {
                "dns_info": {
                    "banner": ""
                }
            },
            "description": "",
            "error": "",
        })

    def verify(self):
        version = ['9.1.0','9.1.0b1','9.1.0b2','9.1.0b3','9.1.0rc1',
        '9.1.1','9.1.1rc1','9.1.1rc2','9.1.1rc3','9.1.1rc4','9.1.1rc5',
        '9.1.1rc6','9.1.1rc7','9.1.2','9.1.2rc1','9.1.3-P2','9.1.3-P3',
        '9.1.3','9.1.3rc1','9.1.3rc2','9.1.3rc3','9.2.0','9.2.0a1','9.2.0a2',
        '9.2.0a3','9.2.0b1','9.2.0b2','9.2.0rc1','9.2.0rc2','9.2.0rc3','9.2.0rc4',
        '9.2.0rc5','9.2.0rc6','9.2.0rc7','9.2.0rc7','9.2.0rc8','9.2.0rc9','9.2.0rc10',
        '9.2.1','9.2.1rc1','9.2.1rc2','9.2.2-P2','9.2.2-P3','9.2.2','9.2.2rc1','9.2.3',
        '9.2.3rc1','9.2.3rc2','9.2.3rc3','9.2.3rc4','9.2.4','9.2.4rc2','9.2.4rc3','9.2.4rc4',
        '9.2.4rc5','9.2.4rc6','9.2.4rc7','9.2.4rc8','9.2.5','9.2.5beta2','9.2.5rc1','9.2.6-P1',
        '9.2.6-P2','9.2.6','9.2.6b1','9.2.6b2','9.2.6rc1','9.2.7','9.2.7b1','9.2.7rc1','9.2.7rc2',
        '9.2.7rc3','9.2.8-P1','9.2.8','9.2.9','9.2.9b1','9.2.9rc1','9.3.0','9.3.0beta2','9.3.0beta3',
        '9.3.0beta4','9.3.0rc1','9.3.0rc2','9.3.0rc3','9.3.0rc4','9.3.1','9.3.1beta2','9.3.1rc1','9.3.2-P1',
        '9.3.2-P2','9.3.2','9.3.2b1','9.3.2rc1','9.3.3','9.3.3b1','9.3.3rc1','9.3.3rc2','9.3.3rc3','9.3.4-P1',
        '9.3.4','9.3.5-P1','9.3.5-P2-W1','9.3.5-P2-W2','9.3.5-P2','9.3.5','9.3.5b1','9.3.5rc1','9.3.5rc2',
        '9.3.6-P1','9.3.6','9.3.6b1','9.3.6rc1','9.4-ESV-R1','9.4-ESV-R2','9.4-ESV-R3','9.4-ESV-R4-P1','9.4-ESV-R5',
        '9.4-ESV-R5b1','9.4-ESV-R5rc1','9.4-ESV','9.4-ESVb1','9.4.0','9.4.0a5','9.4.0a6','9.4.0b1','9.4.0b2','9.4.0b3',
        '9.4.0b4','9.4.0rc1','9.4.0rc2','9.4.1-P1','9.4.1','9.4.2-P1','9.4.2-P2-W1','9.4.2-P2-W2','9.4.2-P2','9.4.2',
        '9.4.2b1','9.4.2rc1','9.4.2rc2','9.4.3-P1','9.4.3-P2','9.4.3-P3','9.4.3-P4','9.4.3-P5','9.4.3','9.4.3b1','9.4.3b2',
        '9.4.3b3','9.4.3rc1','9.4.3rc1','9.5.0-P1','9.5.0-P2-W1','9.5.0-P2-W2','9.5.0-P2','9.5.0','9.5.0a5','9.5.0a6','9.5.0a7',
        '9.5.0b1','9.5.0b2','9.5.0b3','9.5.0rc1','9.5.1-P1','9.5.1-P2','9.5.1-P3','9.5.1','9.5.1b1','9.5.1b2','9.5.1b3',
        '9.5.1rc1','9.5.1rc2','9.5.2-P1','9.5.2-P2','9.5.2-P3','9.5.2-P4','9.5.2','9.5.2b1','9.5.2rc1','9.5.3b1',
        '9.5.3rc1','9.6-ESV-R1','9.6-ESV-R2','9.6-ESV-R3','9.6-ESV-R4-P1','9.6-ESV-R4-P3','9.6-ESV-R4','9.6-ESV-R5-P1',
        '9.6-ESV-R5','9.6-ESV-R5b1','9.6-ESV-R5rc1','9.6-ESV-R6','9.6-ESV-R6b1','9.6-ESV-R6rc1','9.6-ESV-R6rc2','9.6-ESV-R7-P1',
        '9.6-ESV-R7-P2','9.6-ESV-R7-P3','9.6-ESV-R7-P4','9.6-ESV-R7','9.6-ESV-R8','9.6-ESV-R8b1','9.6-ESV-R8rc1','9.6-ESV-R9-P1',
        '9.6-ESV-R9','9.6-ESV-R9b1','9.6-ESV-R9b2','9.6-ESV-R9rc1','9.6-ESV-R9rc2','9.6-ESV-R10-P1','9.6-ESV-R10-P2',
        '9.6-ESV-R10','9.6-ESV-R10b1','9.6-ESV-R10rc1','9.6-ESV-R10rc2','9.6-ESV-R11-W1','9.6-ESV-R11','9.6-ESV-R11b1',
        '9.6-ESV-R11rc1','9.6-ESV-R11rc2','9.6-ESV','9.6.0-P1','9.6.0','9.6.0a1','9.6.0b1','9.6.0rc1','9.6.0rc2',
        '9.6.1-P1','9.6.1-P2','9.6.1-P3','9.6.1','9.6.1b1','9.6.1rc1','9.6.2-P1','9.6.2-P2','9.6.2-P3',
        '9.6.2','9.6.2b1','9.6.2rc1','9.6.3','9.6.3b1','9.6.3rc1','9.7.0-P1','9.7.0-P2','9.7.0','9.7.0a1','9.7.0a2',
        '9.7.0a3','9.7.0b1','9.7.0b2','9.7.0b3','9.7.0rc1','9.7.0rc2','9.7.1-P1','9.7.1-P2','9.7.1','9.7.1b1',
        '9.7.1rc1','9.7.2-P1','9.7.2-P2','9.7.2-P3','9.7.2','9.7.2b1','9.7.2rc1','9.7.3-P1','9.7.3-P3','9.7.3',
        '9.7.3b1','9.7.3rc1','9.7.4-P1','9.7.4','9.7.4b1','9.7.4rc1','9.7.5','9.7.5b1','9.7.5rc1','9.7.5rc2',
        '9.7.6-P1','9.7.6-P2','9.7.6-P3','9.7.6-P4','9.7.6','9.7.7','9.7.7b1','9.7.7rc1','9.8.0-P1','9.8.0-P2',
        '9.8.0-P4','9.8.0','9.8.0a1','9.8.0b1','9.8.0rc1','9.8.1-P1','9.8.1','9.8.1b1','9.8.1b2','9.8.1b3','9.8.1rc1',
        '9.8.2','9.8.2b1','9.8.2rc1','9.8.2rc2','9.8.3-P1','9.8.3-P2','9.8.3-P3','9.8.3-P4','9.8.3','9.8.4-P1',
        '9.8.4-P2','9.8.4','9.8.4b1','9.8.4rc1','9.8.5-P1','9.8.5-P2','9.8.5','9.8.5b1','9.8.5b2','9.8.5rc1','9.8.5rc2',
        '9.8.6-P1','9.8.6-P2','9.8.6','9.8.6b1','9.8.6rc1','9.8.6rc2','9.8.7-P1','9.8.7-W1','9.8.7','9.8.7b1','9.8.7rc1',
        '9.8.7rc2','9.8.8','9.8.8b1','9.8.8b2','9.8.8rc1','9.8.8rc2','9.9.0','9.9.0a1','9.9.0a2','9.9.0a3','9.9.0b1','9.9.0b2','9.9.0rc1','9.9.0rc2','9.9.0rc3',
        '9.9.0rc4','9.9.1-P1','9.9.1-P2','9.9.1-P3','9.9.1-P4','9.9.1','9.9.2-P1','9.9.2-P2','9.9.2','9.9.2b1','9.9.2rc1','9.9.3-P1','9.9.3-P2','9.9.3','9.9.3b1',
        '9.9.3b2','9.9.3rc1','9.9.3rc2','9.9.4-P1','9.9.4-P2','9.9.4','9.9.4b1','9.9.4rc1','9.9.4rc2','9.9.5-P1','9.9.5-W1','9.9.5','9.9.5b1',
        '9.9.5rc1','9.9.5rc2','9.9.6-P1','9.9.6-P2','9.9.6','9.9.6b1','9.9.6b2','9.9.6rc1','9.9.6rc2','9.9.7-P1',
        '9.10.0','9.10.0a1','9.10.0a2','9.10.0b1','9.10.0b2','9.10.0rc1','9.10.0rc2','9.10.1-P1','9.10.1-P2','9.10.1','9.10.1b1',
        '9.10.1b2','9.10.1rc1','9.10.1rc2','9.10.2-P1','9.10.2-P2','9.3.6-P1-RedHat-9.3.6-4.P1.el5','9.8.2rc1-RedHat-9.8.2-0.17.rc1.el6_4.6']

        host = self.option.host

        try:
            banner = subprocess.Popen(['dig','@'+ host,'txt','version.bind','chaos','+short'], stdout=subprocess.PIPE).communicate()[0]
            banner = banner.replace('"','').strip('\r\n')
            if banner in version:
                  self.result.status = True
                  self.result.result = banner
                  self.result.description = "目标 {host} 的 bind 版本号: {banner}".format(
            host=self.option.host,
            banner=banner
        )
        except Exception, e:
               self.result.error = "域名解析发生错误: {error}".format(error=str(e))
               return
               

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    from modules.main import main
    main(TangScan())
