from five import grok
from Acquisition import aq_inner
from zope.component import getMultiAdapter

from plone.directives import form
from zope import schema
from z3c.form import form, field
from Products.CMFCore.utils import getToolByName
from dexterity.membrane.content.member import IOrganizationMember
from zope.interface import Interface
 
from plone.memoize.instance import memoize

from dexterity.membrane.behavior.membranepassword import IProvidePasswords 
from plone.app.layout.navigation.interfaces import INavigationRoot
from dexterity.membrane import _
from plone.directives import dexterity
from xtshzz.policy.browser.interfaces import IXtshzzThemeSpecific as IThemeSpecific
grok.templatedir('templates')

class MemberUrlView(grok.View):
    grok.name('member_url')
    grok.layer(IThemeSpecific)    
    grok.require('zope2.View')
    grok.context(Interface)

    @memoize    
    def render(self):
        pm =getToolByName(self.context,'portal_membership')
        userobj = pm.getAuthenticatedMember()
        catalog = getToolByName(self.context,'portal_catalog')
        email = userobj.getUserName()
        try:
            member = catalog({'object_provides': IOrganizationMember.__identifier__, "email":email})[0].getObject()
            return member.absolute_url()
        except:
            return ""      
            


class MembraneMemberView(grok.View):
    grok.context(IOrganizationMember)     
    grok.template('member_b3_view')
    grok.name('view')
    grok.layer(IThemeSpecific)    
    grok.require('zope2.View')

    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)

    @memoize    
    def catalog(self):
        context = aq_inner(self.context)
        pc = getToolByName(context, "portal_catalog")
        return pc
    
    @memoize    
    def pm(self):
        context = aq_inner(self.context)
        pm = getToolByName(context, "portal_membership")
        return pm 
       
    @memoize    
    def getHomeFolder(self):
        member = self.pm().getAuthenticatedMember()
        member_id = member.getId()
        member_folder = self.pm().getHomeFolder(member_id)
        return member_folder
    
    @memoize    
    def createSurveyUrl(self):
        from xtshzz.policy.behaviors.org import IOrg

        member_data = self.pm().getAuthenticatedMember()
        id = member_data.getUserName()
        query = {"object_provides":IOrganizationMember.__identifier__,'email':id}
        bns = self.catalog()(query)
        if bns:
            member = bns[0].getObject()
#            import pdb
#            pdb.set_trace()
            path = IOrg(member).getOrgPath()
            if not path:return ""
            return "%s/++add++my315ok.socialorgnization.orgnizationsurvey"  % path
        else:
            return ""     
    
    def fullname(self):
        context = self.context
        return context.title
    
    def tranVoc(self,value):
        """ translate vocabulary value to title"""
        translation_service = getToolByName(self.context,'translation_service')
        title = translation_service.translate(
                                                  value,
                                                  domain='dexterity.membrane',
                                                  mapping={},
                                                  target_language='zh_CN',
                                                  context=self.context,
                                                  default="translate")
        return title
    


      
    
class EditProfile(dexterity.EditForm):
    grok.name('edit-baseinfo')
    grok.context(IOrganizationMember)
    grok.layer(IThemeSpecific)        
    label = _(u'Base information')
# avoid autoform functionality
    def updateFields(self):
        pass
    @property
    def fields(self):
        return field.Fields(IOrganizationMember).select('title','description','email')

class EditProfilePassword(dexterity.EditForm):
    grok.name('edit-password')
    grok.context(IOrganizationMember)
    grok.layer(IThemeSpecific)        
    label = _(u'Update password')
# avoid autoform functionality
    def updateFields(self):
        pass
    @property
    def fields(self):
        return field.Fields(IProvidePasswords).select('password','confirm_password')

class EditProfileNetworking(dexterity.EditForm):
    grok.name('edit-networking')
    grok.context(IOrganizationMember)
    grok.layer(IThemeSpecific)        
    label = _(u'Network information')
# avoid autoform functionality
    def updateFields(self):
        pass
    @property
    def fields(self):
        return field.Fields(IOrganizationMember).select('homepage',)
        
