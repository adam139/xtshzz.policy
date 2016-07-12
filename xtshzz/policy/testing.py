#-*- coding: UTF-8 -*-
import datetime
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting,FunctionalTesting

from plone.app.testing import (
IntegrationTesting,
FunctionalTesting,
login, logout, setRoles,
PLONE_FIXTURE,
TEST_USER_NAME,
SITE_OWNER_NAME,
)

from plone.testing import z2
from plone.namedfile.file import NamedImage
from plone import namedfile
from zope.configuration import xmlconfig

def getFile(filename):
    """ return contents of the file with the given name """
    import os
    filename = os.path.join(os.path.dirname(__file__) + "/tests/", filename)
    return open(filename, 'r')

class SitePolicy(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)
    
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import xtshzz.policy
        import plone.app.contenttypes
        import collective.diazotheme.bootstrap
        import my315ok.socialorgnization
        import my315ok.products
        import dexterity.membrane
        xmlconfig.file('configure.zcml', collective.diazotheme.bootstrap, context=configurationContext)
        xmlconfig.file('configure.zcml', xtshzz.policy, context=configurationContext)
        xmlconfig.file('configure.zcml', plone.app.contenttypes, context=configurationContext)
        xmlconfig.file('configure.zcml', my315ok.products, context=configurationContext)        
#         xmlconfig.file('configure.zcml', dexterity.membrane, context=configurationContext)
#         xmlconfig.file('configure.zcml', my315ok.socialorgnization, context=configurationContext)        
        # Install products that use an old-style initialize() function
#         z2.installProduct(app, 'Products.PythonField')
#         z2.installProduct(app, 'Products.TALESField')
#         z2.installProduct(app, 'Products.TemplateFields')
#         z2.installProduct(app, 'Products.PloneFormGen')
#         z2.installProduct(app, 'Products.membrane')        
    
    def tearDownZope(self, app):
        pass
        # Uninstall products installed above
#         z2.uninstallProduct(app, 'Products.PloneFormGen')
#         z2.uninstallProduct(app, 'Products.TemplateFields')
#         z2.uninstallProduct(app, 'Products.TALESField')
#         z2.uninstallProduct(app, 'Products.PythonField')
#         z2.uninstallProduct(app, 'Products.membrane')        
        
    def setUpPloneSite(self, portal):
        applyProfile(portal, 'xtshzz.policy:default')
        applyProfile(portal, 'plone.app.contenttypes:default')
        applyProfile(portal, 'my315ok.products:default')        
#         applyProfile(portal, 'dexterity.membrane:default')
#        applyProfile(portal, 'dexterity.membrane.content:example')

class IntegrationSitePolicy(SitePolicy):      
        
    def setUpPloneSite(self, portal):
        applyProfile(portal, 'xtshzz.policy:default')
#         applyProfile(portal, 'my315ok.socialorgnization:default')
#         applyProfile(portal, 'dexterity.membrane:default')
#        applyProfile(portal, 'dexterity.membrane.content:example')

#        portal = self.layer['portal']
        #make global request work
        from zope.globalrequest import setRequest
        setRequest(portal.REQUEST)
        # login doesn't work so we need to call z2.login directly
        z2.login(portal.__parent__.acl_users, SITE_OWNER_NAME)
#        setRoles(portal, TEST_USER_ID, ('Manager',))
#        login(portal, TEST_USER_NAME)
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

POLICY_FIXTURE = SitePolicy()
POLICY_INTEGRATION_FIXTURE = IntegrationSitePolicy()
POLICY_INTEGRATION_TESTING = IntegrationTesting(bases=(POLICY_INTEGRATION_FIXTURE,), name="Site:Integration")
FunctionalTesting = FunctionalTesting(bases=(POLICY_FIXTURE,), name="Site:FunctionalTesting")