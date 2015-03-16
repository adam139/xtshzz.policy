#-*- coding: UTF-8 -*-
from five import grok
from Acquisition import aq_inner
from zope import schema
from zope.interface import Interface
from zope.component import getMultiAdapter
from z3c.form import form, field
from Products.CMFCore.utils import getToolByName
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.directives import dexterity
from plone.directives import form
from plone.memoize.instance import memoize
import json
from dexterity.membrane.content.member import IOrganizationMember
from dexterity.membrane.content.member import IMember
from dexterity.membrane.content.member import ISponsorMember
from dexterity.membrane.behavior.membranepassword import IProvidePasswords 
from dexterity.membrane import _
from my315ok.socialorgnization.content.orgnization import IOrgnization
from my315ok.socialorgnization.content.orgnization import IOrgnization_annual_survey
from xtshzz.policy.browser.interfaces import IXtshzzThemeSpecific as IThemeSpecific
import datetime

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
            member = catalog({'object_provides': IMember.__identifier__, "email":email})[0].getObject()
            return member.absolute_url()
        except:
            return ""      
            


class MembraneMemberView(grok.View):
    grok.context(IMember)     
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
    def currentUserEmail(self):
        "return current user's login name:email"
        member_data = self.pm().getAuthenticatedMember()
        try:
            id = member_data.getUserName()
            if "@" in id:return id
            return ""
        except:
            return ""

    def isOrgAccount(self):
        "see current user if is a organization account"
        id = self.currentUserEmail()
        if id =="":return False
        query = {"object_provides":IOrganizationMember.__identifier__,'email':id}
        bns = self.catalog()(query)
        return len(bns)
            
    @memoize 
    def getSponsorOrgName(self):
        "return current sponsormember's sponsor name"
        from xtshzz.policy.behaviors.org import ISponsor
        id = self.currentUserEmail()
        if id =="":return False
        query = {"object_provides":ISponsorMember.__identifier__,'email':id}
        bns = self.catalog()(query)
        try:
            bn = bns[0]
        except:
            return ""                

        member = bn.getObject()
        orgbn = ISponsor(member).getSponsorBn()
        if not orgbn:return ""
        return orgbn.Title
    
    def isSponsor(self):
        "see current user if is a sponsor account"
        id = self.currentUserEmail()
        if id =="":return False
        query = {"object_provides":ISponsorMember.__identifier__,'email':id}
        bns = self.catalog()(query)
        try:
            bn = bns[0]
            return True
        except:
            return False
        
    def isAgentOperator(self):
        "see current user if is a civil agent operator account"
        id = self.currentUserEmail()
        if id =="":return False
        # search civil agent object
        from my315ok.socialorgnization.content.governmentdepartment import IOrgnization
        query = {"object_provides":IOrgnization.__identifier__,'id':"minzhengju"}
        bns = self.catalog()(query)
        return (bns[0].getObject().operator == id) and self.isSponsor()    
    
    @memoize
    def canRead(self):
        "see if current user can read this page"
        from AccessControl import getSecurityManager
        from Products.CMFCore.permissions import ModifyPortalContent
        context = self.context
        sm = getSecurityManager()
        id = self.currentUserEmail()
        if id == context.email:return True
        elif not sm.checkPermission(ModifyPortalContent, context):return False
        else:
            return True
        
        
    @memoize
    def pendingsurvey(self):
        "return all annual survey that pending current user review,return value should be list that item is dic"
# is normal organization
        if self.isOrgAccount():
            return []
# is civil agent         
        elif self.isAgentOperator():
            query = {"object_provides":IOrgnization_annual_survey.__identifier__,'review_state':"pendingagent"}
            bns = self.catalog()(query)           
            return bns
# is sponsor :government department        
        else:
            query = {"object_provides":IOrgnization_annual_survey.__identifier__,'review_state':"pendingsponsor"}
            bns = self.catalog()(query)
            email = self.currentUserEmail()
            pending = []
            for bn in bns:
                ob = bn.getObject()
                dview = getMultiAdapter((ob, self.request),name=u"sponsorview")
                op = dview.getSponsorOperatorEmail()
                if op == email:
                    pending.append(bn)
                    continue
                else:
                    continue      
            return pending
        
    @memoize    
    def SurveyUrl(self):
        "return current annual survey url"
        from xtshzz.policy.behaviors.org import IOrg

        member_data = self.pm().getAuthenticatedMember()
        try:
            id = member_data.getUserName()
        except:
            return ""
        query = {"object_provides":IMember.__identifier__,'email':id}
        bns = self.catalog()(query)
        try:
            bn = bns[0]
        except:
            return ""                

        member = bn.getObject()
        orgbn = IOrg(member).getOrgBn()
        if not orgbn:return ""
        org = orgbn.getObject()
        # last year's number as annual survey id 
        id = (datetime.datetime.today() + datetime.timedelta(-365)).strftime("%Y")
            # see if org container contain id object
        try:
            survey = getattr(org, id, None)
            if survey ==None:return ""
        except:
            return ""

        path = IOrg(member).getOrgPath()
        if not path:return ""
        return "%s/%s"  % (path,id)
        
    
    @memoize    
    def createSurveyUrl(self):
        from xtshzz.policy.behaviors.org import IOrg
        member_data = self.pm().getAuthenticatedMember()
        try:
            id = member_data.getUserName()
        except:
            return ""
        query = {"object_provides":IMember.__identifier__,'email':id}
        bns = self.catalog()(query)
        try:
            bn = bns[0]
        except:
            return ""
                
        if bn.review_state =="enabled":
            member = bn.getObject()
            orgbn = IOrg(member).getOrgBn()
            if not orgbn:return ""
            org = orgbn.getObject()
            id = (datetime.datetime.today() + datetime.timedelta(-365)).strftime("%Y")
            # see if org container contain id object
            try:
                survey = getattr(org, id, None)
                if survey !=None:return ""
            except:
                return ""

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
    
class SponsorMemberView(MembraneMemberView):
    grok.context(ISponsorMember)     
    grok.template('sponsor_member_b3_view')
   
class ManagedOrgsView(MembraneMemberView):
    grok.context(ISponsorMember)
    grok.name("managed_orgs_b3_view")     
    grok.template('i_managed_orgs_b3_view')
    
    def pendingDefault(self):
        "计算缺省情况下，还剩多少条"
        total = len(self.allitems())
        if total > 10:
            return total -10
        else:
            return 0      
    
    @memoize    
    def allitems(self):        

        "return I managed all organizations"
        sponsor = self.getSponsorOrgName()
        query = {"object_provides":IOrgnization.__identifier__,'orgnization_supervisor':sponsor}
        bns = self.catalog()(query)
        return bns  
    
    @memoize
    def getManaged_orgs_list(self,start=0,size=0):
        "return I managed all organizations"
#        sponsor = self.getSponsorOrgName()
#        query = {"object_provides":IOrgnization.__identifier__,'orgnization_supervisor':sponsor}
#        bns = self.catalog()(query)
#        return bns
    
        if size == 0:
            braindata = self.allitems()
#            return self.outputList(braindata)      

        else:
            sponsor = self.getSponsorOrgName()
            braindata = self.catalog()({"object_provides":IOrgnization.__identifier__, 
                                'orgnization_supervisor':sponsor,
                             'sort_order': 'reverse',
                             'sort_on': 'created',
                             'b_start':start,
                             'b_size':size})
            
        return self.outputList(braindata)     
    
    def isSurveyed(self,bn):
        "bn is organization brain,return this bn if has been surveyed"
        org = bn.getObject()
        id = (datetime.datetime.today() + datetime.timedelta(-365)).strftime("%Y")
            # see if org container contain last year survey report
        try:
            survey = getattr(org, id, None)
            if survey ==None:return u"未提交年检报告"
            else:
                return u"已提交年检报告"
        except:
            return u"未指定"        

    def outputList(self,braindata):
        outhtml = ""
        brainnum = len(braindata)        
        for i in braindata:
            objurl =  i.getURL()
            objtitle = i.Title
            status = self.isSurveyed(i)                        
            out = """ <tr class="row">
                  <td class="col-md-9 text-left">
                      <a href="%(url)s">
                         <span>%(Title)s</span>
                      </a>
                  </td>
                  <td class="col-md-3" >
                      <span>%(survey_status)s</span>
                  </td>                   
             </tr>""" % dict(url=objurl,Title=objtitle,survey_status=status)
          
            outhtml = outhtml + out
        return outhtml      
    
class ManagedOrgMore(grok.View):
    """I managed all organizations list view AJAX action for click more.
    """
    
    grok.context(ISponsorMember)
    grok.name('managed_org_more')
    grok.require('zope2.View')            
    
    def render(self):
#        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")        
        form = self.request.form
        formst = form['formstart']
        formstart = int(formst)*10 
        nextstart = formstart + 10                
        favorite_view = getMultiAdapter((self.context, self.request),name=u"managed_orgs_b3_view")
        favoritenum = len(favorite_view.allitems())
        
        if nextstart >= favoritenum :
            ifmore =  1
            pending = 0
        else :
            ifmore = 0  
            pending = favoritenum - nextstart          

        pending = "%s" % (pending)          
        outhtml = favorite_view.getManaged_orgs_list(formstart,10)            
        data = {'outhtml': outhtml,'pending':pending,'ifmore':ifmore}
    
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)

class EditProfile(dexterity.EditForm):
    grok.name('edit-baseinfo')
    grok.context(IMember)
    grok.layer(IThemeSpecific)        
    label = _(u'Base information')
# avoid autoform functionality
    def updateFields(self):
        pass
    @property
    def fields(self):
        return field.Fields(IMember).select('title','description')

class EditProfilePassword(dexterity.EditForm):
    grok.name('edit-password')
    grok.context(IMember)
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
    grok.context(IMember)
    grok.layer(IThemeSpecific)        
    label = _(u'Network information')
# avoid autoform functionality
    def updateFields(self):
        pass
    @property
    def fields(self):
        return field.Fields(IMember).select('homepage',)

class EditProfileOrgName(dexterity.EditForm):
    grok.name('edit-orgname')
    grok.context(IOrganizationMember)
    grok.layer(IThemeSpecific)        
    label = u'更新所属社会组织'
# avoid autoform functionality
    def updateFields(self):
        pass
    @property
    def fields(self):
        return field.Fields(IOrganizationMember).select('orgname',)        
