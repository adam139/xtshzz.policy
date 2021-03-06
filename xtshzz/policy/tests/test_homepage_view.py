# -*- coding: UTF-8 -*-
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.namedfile.file import NamedBlobFile
from plone.namedfile.file import NamedBlobImage
from plone.namedfile.file import NamedImage
from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
from xtshzz.policy.testing import FunctionalTesting

import os
import unittest


def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')


class TestView(unittest.TestCase):

    layer = FunctionalTesting

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        import datetime
#        import pdb
#        pdb.set_trace()
        start = datetime.datetime.today()
        end = start + datetime.timedelta(7)
        portal.invokeFactory(
            'dexterity.membrane.memberfolder',
            'memberfolder1')

        portal['memberfolder1'].invokeFactory('dexterity.membrane.organizationmember', 'member1',
                                              email="12@qq.com",
                                              last_name=u"唐",
                                              first_name=u"岳军",
                                              title=u"tangyuejun",
                                              password="391124",
                                              confirm_password="391124",
                                              homepae='http://315ok.org/',

                                              description="I am member1")
        portal['memberfolder1'].invokeFactory('dexterity.membrane.organizationmember', 'member2',
                                              email="13@qq.com",
                                              last_name=u"唐",
                                              first_name=u"岳军",
                                              title=u"tangyuejun",
                                              password="391124",
                                              confirm_password="391124",
                                              homepae='http://315ok.org/',

                                              description="I am member1")

        portal['memberfolder1'].invokeFactory('dexterity.membrane.organizationmember', 'member3',
                                              email="14@qq.com",
                                              last_name=u"唐",
                                              first_name=u"岳军",
                                              title=u"tangyuejun",
                                              password="391124",
                                              confirm_password="391124",
                                              homepae='http://315ok.org/',

                                              description="I am member1")

        portal['memberfolder1'].invokeFactory('dexterity.membrane.organizationmember', 'member4',
                                              email="15@qq.com",
                                              last_name=u"唐",
                                              first_name=u"岳军",
                                              title=u"tangyuejun",
                                              password="391124",
                                              confirm_password="391124",
                                              homepae='http://315ok.org/',

                                              description="I am member1")

        portal['memberfolder1'].invokeFactory('dexterity.membrane.organizationmember', 'member5',
                                              email="16@qq.com",
                                              last_name=u"唐",
                                              first_name=u"岳军",
                                              title=u"tangyuejun",
                                              password="391124",
                                              confirm_password="391124",
                                              homepae='http://315ok.org/',

                                              description="I am member1")

        data = getFile('image.jpg').read()
        item = portal['memberfolder1']['member1']
        item.photo = NamedImage(data, 'image/jpg', u'image.jpg')

        portal.invokeFactory('my315ok.socialorgnization.orgnizationfolder', 'orgnizationfolder1',
                             title="productfolder1", description="demo productfolder")

        # 社会组织
        portal['orgnizationfolder1'].invokeFactory('my315ok.socialorgnization.orgnization', 'orgnization1',
                                                   title=u"宝庆商会",
                                                   description=u"运输业",
                                                   address=u"建设北路",
                                                   register_code="8341",
                                                   supervisor=u"交通局",
                                                   organization_type="minfei",
                                                   legal_person=u"张建明",
                                                   passDate=datetime.datetime.today(),
                                                   belondto_area='yuhuqu',
                                                   )
# 建立监管单位   ：交通局 government1
        portal['orgnizationfolder1'].invokeFactory('my315ok.socialorgnization.governmentorgnization', 'government1',
                                                   title=u"交通局",
                                                   description=u"运输业",
                                                   operator="100@qq.com",)

# 建民政局    id hard code as:‘minzhengju’                                               )
        portal['orgnizationfolder1'].invokeFactory('my315ok.socialorgnization.governmentorgnization', 'minzhengju',
                                                   title=u"民政局",
                                                   description=u"民政局",
                                                   operator="200@qq.com",

                                                   )

#        logout()
#        login(portal, '12@qq.com')
        portal['orgnizationfolder1']['orgnization1'].invokeFactory('my315ok.socialorgnization.orgnizationsurvey', 'survey1',
                                                                   title=u"宝庆商会",
                                                                   description=u"运输业",
                                                                   annual_survey="hege",
                                                                   year="2013",

                                                                   )

        data = getFile('demo.txt').read()
        item = portal['orgnizationfolder1']['orgnization1']['survey1']
#         item.image = NamedImage(data, 'image/gif', u'image.gif')
        item.report = NamedBlobFile(data, filename=u"demo.txt")

# 新闻中心
        portal.invokeFactory('Folder', 'xinwenzhongxin',
                             title=u"新闻中心", description="demo productfolder")
        portal['xinwenzhongxin'].invokeFactory('Folder', 'guanligongzuodongtai',
                                               title=u"管理工作动态", description="demo productfolder")
        portal['xinwenzhongxin'].invokeFactory('Folder', 'shehuizuzhifengcai',
                                               title=u"社会组织风采", description="demo productfolder")
        portal['xinwenzhongxin'].invokeFactory('Folder', 'jingyanjiaoliu',
                                               title=u"经验交流", description="demo productfolder")
        portal['xinwenzhongxin'].invokeFactory('my315ok.products.productfolder', 'tupianxinwen',
                                               title=u"图片新闻", description="demo productfolder")
        portal['xinwenzhongxin']['tupianxinwen'].invokeFactory('my315ok.products.product', 'tupianxinwen1',
                                                               title=u"图片新闻1", description="demo productfolder")
        data = getFile('image.jpg').read()
        item = portal['xinwenzhongxin']['tupianxinwen']['tupianxinwen1']
        item.image = NamedBlobImage(data, 'image/jpg', u'image.jpg')
        item.text = u"图片新闻1"

        portal['xinwenzhongxin']['guanligongzuodongtai'].invokeFactory('Document', 'guanligongzuodongtai1',
                                                                       title=u"管理工作动态1", description="demo productfolder")
        portal['xinwenzhongxin']['jingyanjiaoliu'].invokeFactory('Document', 'jingyanjiaoliu1',
                                                                 title=u"经验交流1", description="demo productfolder")
        portal['xinwenzhongxin']['shehuizuzhifengcai'].invokeFactory('Document', 'shehuizuzhifengcai1',
                                                                     title=u"社会组织风采1", description="demo productfolder")

# 信息公开
        portal.invokeFactory('Folder', 'xinxigongkai',
                             title=u"信息公开", description="demo productfolder")
        portal['xinxigongkai'].invokeFactory('Folder', 'tongzhigonggao',
                                             title=u"通知公告", description="demo productfolder")
        portal['xinxigongkai'].invokeFactory('Folder', 'zhengcefagui',
                                             title=u"政策法规", description="demo productfolder")
        portal['xinxigongkai'].invokeFactory('Folder', 'xingzhengchufagonggao',
                                             title=u"行政处罚公告", description="demo productfolder")
        portal['xinxigongkai']['tongzhigonggao'].invokeFactory('Document', 'guanligotongzhigonggao1',
                                                               title=u"通知公告1", description="demo productfolder")
        portal['xinxigongkai']['zhengcefagui'].invokeFactory('Document', 'zhengcefagui1',
                                                             title=u"政策法规1", description="demo productfolder")
        portal['xinxigongkai']['xingzhengchufagonggao'].invokeFactory('Document', 'xingzhengchufagonggao',
                                                                      title=u"行政处罚公告1", description="demo productfolder")
# 查询集
        portal.invokeFactory('Folder', 'sqls',
                             title=u"查询集", description="demo productfolder")
        query = [{
            'i': 'portal_type',
            'o': 'plone.app.querystring.operation.string.is',
            'v': 'Document',
        }]
        portal['sqls'].invokeFactory('Collection', 'tongzhigonggao',
                                     title=u"通知公告", query=query)
        portal['sqls'].invokeFactory('Collection', 'shehuizuzhidongtai',
                                     title=u"社会组织动态", query=query)
        portal['sqls'].invokeFactory('Collection', 'gongzuodongtai',
                                     title=u"工作动态", query=query)
        portal['sqls'].invokeFactory('Collection', 'hudongjiaoliu',
                                     title=u"互动交流", query=query)
        portal['sqls'].invokeFactory('Collection', 'zhengcefagui',
                                     title=u"政策法规", query=query)
        portal['sqls'].invokeFactory('Collection', 'fuwuxinxi',
                                     title=u"服务信息", query=query)
        portal['sqls'].invokeFactory('Collection', 'xingzhengxukegonggao',
                                     title=u"行政许可公告", query=query)
        portal['sqls'].invokeFactory('Collection', 'nianjianjieguogonggao',
                                     title=u"年检结果公告", query=query)
        portal['sqls'].invokeFactory('Collection', 'chachujieguogonggao',
                                     title=u"查处结果公告", query=query)

        self.portal = portal

    def test_homepage_view(self):

        app = self.layer['app']
        portal = self.layer['portal']

        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader(
            'Authorization', 'Basic %s:%s' %
            (TEST_USER_NAME, TEST_USER_PASSWORD,))

        import transaction
        transaction.commit()
        obj = portal.absolute_url() + '/@@index.html'

        browser.open(obj)

        outstr = u"政策法规1"

        self.assertTrue(outstr in browser.contents)
