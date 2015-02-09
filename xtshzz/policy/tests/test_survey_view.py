#-*- coding: UTF-8 -*-
from Products.CMFCore.utils import getToolByName
from xtshzz.policy.testing import POLICY_INTEGRATION_TESTING,FunctionalTesting

from plone.app.testing import TEST_USER_ID, login, logout, TEST_USER_NAME, \
    TEST_USER_PASSWORD,SITE_OWNER_NAME,SITE_OWNER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest2 as unittest
from plone.namedfile.file import NamedImage
from plone import namedfile
import os
import datetime

def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')

class TestProductlView(unittest.TestCase):
    
    layer = POLICY_INTEGRATION_TESTING
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('dexterity.membrane.memberfolder', 'memberfolder1')
           # 社团经手人账号     
        portal['memberfolder1'].invokeFactory('dexterity.membrane.organizationmember', 'member1',
                             email="12@qq.com",
                             last_name=u"唐",
                             first_name=u"岳军",
                             title = u"tangyuejun",
                             password="391124",
                             confirm_password ="391124",
                             orgname = "orgnization1",
                             homepae = 'http://315ok.org/',
                             bonus = 10,
                             description="I am member1")         
        # 监管单位经手人账号
        portal['memberfolder1'].invokeFactory('dexterity.membrane.sponsormember', '100',
                             email="100@qq.com",
                             last_name=u"唐",
                             first_name=u"岳军",
                             title = u"tangyuejun",
                             password="391124",
                             confirm_password ="391124",
                             orgname =u"government1",
                             homepae = 'http://315ok.org/',
                             bonus = 10,
                             description="I am member1")
        # 民政局经手人账号
        portal['memberfolder1'].invokeFactory('dexterity.membrane.sponsormember', '200',
                             email="200@qq.com",
                             last_name=u"唐",
                             first_name=u"岳军",
                             title = u"tangyuejun",
                             password="391124",
                             confirm_password ="391124",
                             orgname =u"minzhengju",
                             homepae = 'http://315ok.org/',
                             bonus = 10,
                             description="I am member1")
                    
        portal.invokeFactory('my315ok.socialorgnization.orgnizationfolder', 'orgnizationfolder1',
                             title="productfolder1",description="demo productfolder")     
     
        # 社会组织
        portal['orgnizationfolder1'].invokeFactory('my315ok.socialorgnization.orgnization','orgnization1',
                                                   title=u"宝庆商会",
                                                   description=u"运输业",
                                                   address=u"建设北路",
                                                   register_code="8341",
                                                   supervisor=u"交通局",
                                                   organization_type="minfei",
                                                   legal_person=u"张建明",
                                                   passDate =datetime.datetime.today(),
                                                   belondto_area='yuhuqu', 
                                                   )
#建立监管单位   ：交通局 government1     
        portal['orgnizationfolder1'].invokeFactory('my315ok.socialorgnization.governmentorgnization','government1',
                                                   title=u"交通局",
                                                   description=u"运输业",
                                                   operator="100@qq.com",)

#建民政局    id hard code as:‘minzhengju’                                               ) 
        portal['orgnizationfolder1'].invokeFactory('my315ok.socialorgnization.governmentorgnization','minzhengju',
                                                   title=u"民政局",
                                                   description=u"民政局",
                                                   operator="200@qq.com",

                                                   ) 
               
#        logout()
#        login(portal, '12@qq.com')
        portal['orgnizationfolder1']['orgnization1'].invokeFactory('my315ok.socialorgnization.orgnizationsurvey','survey1',
                                                   title=u"宝庆商会",
                                                   description=u"运输业",
                                                   annual_survey="hege",
                                                   year="2013",

                                                   )        


        data = getFile('demo.txt').read()
        item = portal['orgnizationfolder1']['orgnization1']['survey1']
        item.image = NamedImage(data, 'image/gif', u'image.gif')
        item.report = namedfile.NamedBlobFile(data,filename=u"demo.txt")

               
        self.portal = portal     
        import transaction
        transaction.commit()
        
    def test_draft_view(self):

        app = self.layer['app']
        portal = self.layer['portal']
        
        wf = getToolByName(portal, 'portal_workflow')

        wt = wf.dexterity_membrane_workflow
        dummy = portal['memberfolder1']['member1']

        wf.notifyCreated(dummy)

        chain = wf.getChainFor(dummy)
        self.failUnless(chain[0] =='dexterity_membrane_workflow')

        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'pending')        
        wf.doActionFor(dummy, 'approve', comment='foo' )
#        import pdb
#        pdb.set_trace()
        


#启用监管账号

        dummy = portal['memberfolder1']['100']

        wf.notifyCreated(dummy)

        chain = wf.getChainFor(dummy)
        self.failUnless(chain[0] =='dexterity_membrane_workflow')

        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'pending')        
        wf.doActionFor(dummy, 'approve', comment='foo' )                

#启用民政局经手账号

        dummy = portal['memberfolder1']['200']

        wf.notifyCreated(dummy)

        chain = wf.getChainFor(dummy)
        self.failUnless(chain[0] =='dexterity_membrane_workflow')

        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'pending')        
        wf.doActionFor(dummy, 'approve', comment='foo' ) 
               
        browser = Browser(app)
        browser.handleErrors = False
#        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
#        
#        import transaction
#        transaction.commit()
        # login in from login page
        browser.open(portal.absolute_url() + '/login_form')
        browser.getControl(name='__ac_name').value = SITE_OWNER_NAME
        browser.getControl(name='__ac_password').value = SITE_OWNER_PASSWORD
        browser.getControl(name='submit').click()
        import transaction
        transaction.commit()                
#        import pdb
#        pdb.set_trace()
        obj = portal['orgnizationfolder1']['orgnization1']['survey1']
        page = obj.absolute_url() + '/draftview'
        browser.open(page)

#        监管单位经手
        outstr = '100@qq.com'
        
        self.assertTrue(outstr in browser.contents)
        outstr = u'民政局'.encode('utf-8')
        
        self.assertTrue(outstr in browser.contents)        
        
