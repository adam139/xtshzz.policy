#-*- coding: UTF-8 -*-
from Products.CMFCore.utils import getToolByName
from xtshzz.policy.testing import POLICY_INTEGRATION_TESTING,FunctionalTesting

from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
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
    
    layer = FunctionalTesting
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))

        portal.invokeFactory('my315ok.socialorgnization.orgnizationfolder', 'orgnizationfolder1',
                             title="productfolder1",description="demo productfolder")     
     
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
        portal['orgnizationfolder1']['orgnization1'].invokeFactory('my315ok.socialorgnization.orgnizationsurvey','survey1',
                                                   title=u"宝庆商会1",
                                                   description=u"运输业",
                                                   annual_survey="hege",
                                                   year="2013",

                                                   )        
        
        portal['orgnizationfolder1'].invokeFactory('my315ok.socialorgnization.orgnization','orgnization2',
                                                   title=u"宝庆商会",
                                                   description=u"运输业",
                                                   address=u"建设北路",
                                                   register_code="834100",
                                                   supervisor=u"交通局",
                                                   organization_type="minfei",
                                                   legal_person=u"张建明",
                                                   passDate =datetime.datetime.today(),
                                                   belondto_area='xiangtanshi', 
                                                   ) 
               
        portal['orgnizationfolder1'].invokeFactory('my315ok.socialorgnization.orgnization','orgnization3',
                                                   title=u"宝庆商会",
                                                   description=u"运输业",
                                                   address=u"建设北路",
                                                   register_code="834100",
                                                   supervisor=u"交通局",
                                                   organization_type="minfei",
                                                   legal_person=u"张建明",
                                                   passDate =datetime.datetime.today(),
                                                   belondto_area='xiangtanshi', 
                                                   ) 

        data = getFile('demo.txt').read()
        item = portal['orgnizationfolder1']['orgnization1']['survey1']
        item.image = NamedImage(data, 'image/gif', u'image.gif')
        item.report = namedfile.NamedBlobFile(data,filename=u"demo.txt")
        data2 = getFile('image.jpg').read()        
        item2 = portal['orgnizationfolder1']['orgnization2']
        item2.image = NamedImage(data2, 'image/jpeg', u'image.jpg')  
               
        self.portal = portal     

        
    def test_draft_view(self):

        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        # login in from login page
#        browser.open(portal.absolute_url() + '/login_form')
#        browser.getControl(name='__ac_name').value = SITE_OWNER_NAME
#        browser.getControl(name='__ac_password').value = SITE_OWNER_PASSWORD
#        browser.getControl(name='submit').click()
                
#        import pdb
#        pdb.set_trace()
        obj = portal['orgnizationfolder1']['orgnization1']['survey1']
        page = obj.absolute_url() + '/draftview'
        browser.open(page)

        outstr = '<span class="label">经办人：</span>' % obj
        import pdb
        pdb.set_trace()
        
        self.assertTrue(outstr in browser.contents)
        
