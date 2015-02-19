#-*- coding: UTF-8 -*-
from five import grok
from zope import event
from zope.lifecycleevent import ObjectAddedEvent
import json
from Acquisition import aq_inner
from zope.component import getMultiAdapter

from plone.directives import form
from zope import schema
from z3c.form import form, field
from Products.CMFCore.utils import getToolByName
from dexterity.membrane.content.memberfolder import IMemberfolder 
from dexterity.membrane.content.member import IOrganizationMember
from dexterity.membrane.content.member import IMember
from dexterity.membrane.content.member import ISponsorMember

from Products.CMFCore import permissions 

from plone.app.layout.navigation.interfaces import INavigationRoot
from dexterity.membrane import _
from plone.directives import dexterity
from xtshzz.policy.browser.interfaces import IXtshzzThemeSpecific as IThemeSpecific

grok.templatedir('templates')

class MemberFolderView(grok.View):
    grok.context(IMemberfolder)     
    grok.template('member_listing')
    grok.name('admin_view')
    grok.layer(IThemeSpecific)
    grok.require('cmf.ManagePortal')

    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
        context = aq_inner(self.context)
        self.pm = getToolByName(context, 'portal_membership')
        
    
    def fullname(self):
        context = self.context
        return context.title
    
    def tranVoc(self,value,domain="dexterity.membrane",target_language="zh_CN"):
        """ translate vocabulary value to title"""
        translation_service = getToolByName(self.context,'translation_service')
        title = translation_service.translate(
                                                  value,
                                                  domain= domain,
                                                  mapping={},
                                                  target_language=target_language,
                                                  context=self.context,
                                                  default="translate")
        return title
    
    @property
    def isEditable(self):
        return self.pm.checkPermission(permissions.ManagePortal,context) 

    def _getUserData(self,userId):


        member = self.pm.getMemberById(userId)
        try:
            groups = member.getGroups()
        except:
            return ""
        roles = [self.tranVoc(role, domain="plone")  for role in member.getRoles() if role != 'Authenticated']
        roles = ','.join(roles)
        return roles
        
    def getMemberBrains(self):

        catalog = getToolByName(self.context, "portal_catalog")
        memberbrains = catalog(object_provides=IMember.__identifier__, 
                                path="/".join(self.context.getPhysicalPath()),
                                              sort_order="reverse",
                                              sort_on="created")
        return memberbrains        
        
    def getMemberList(self):
        """获取会员列表"""
        mlist = []
        memberbrains = self.getMemberBrains()        
                   

        for brain in memberbrains:
           
            row = {'id':'', 'name':'', 'type':'', 'url':'','roles':'',
                    'email':'', 'register_date':'', 'status':'', 'editurl':'',
                    'delurl':''}
            row['id'] = brain.id
            row['name'] = brain.Title
            if brain.portal_type == 'dexterity.membrane.organizationmember':

                row['type'] = u"社会组织关联账号"
            else:
                row['type'] = u"监管单位关联账号"
               
            row['url'] = brain.getURL()


            email = brain.email
            row['roles'] = self._getUserData(email)
            row['email'] = email
            row['register_date'] = brain.created.strftime('%Y-%m-%d')
            row['status'] = brain.review_state
            row['editurl'] = row['url'] + '/@@edit-baseinfo'
            row['delurl'] = row['url'] + '/delete_confirmation'            
            mlist.append(row)
        return mlist

class MemberFolderB3View(MemberFolderView):
    grok.context(IMemberfolder)     
    grok.template('member_b3_listing')
    grok.name('adminb3_view')
    grok.layer(IThemeSpecific)
    grok.require('cmf.ManagePortal')             

class memberstate(grok.View):
    grok.context(IMemberfolder)
    grok.name('ajaxmemberstate')
    grok.layer(IThemeSpecific)
    grok.require('zope2.View')
    
    def render(self):
        data = self.request.form
        id = data['id']
        state = data['state']
#        import pdb
#        pdb.set_trace()
        
        catalog = getToolByName(self.context, 'portal_catalog')
        obj = catalog({'object_provides': IMember.__identifier__,
                       'path':"/".join(self.context.getPhysicalPath()), 
                       "id":id})[0].getObject()        
        portal_workflow = getToolByName(self.context, 'portal_workflow')
# obj current status        
        if state == "pending" : # this is a new account
            try:
                portal_workflow.doActionFor(obj, 'approve')
                # is sponsor member?  send event update relative government department update operator
                if ISponsorMember.providedBy(obj):event.notify(ObjectAddedEvent(obj,self.context,obj.id))
                    
                result = True              

            except:
                result = False
        elif state == "disabled":
            try:
                portal_workflow.doActionFor(obj, 'enable')
                result = True
            except:
                result = False
        else:
            try:
                portal_workflow.doActionFor(obj, 'disable')
                # to do remove the account form government department's operators list 
                result = True
            except:
                result = False            
        obj.reindexObject()

        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(result)     
