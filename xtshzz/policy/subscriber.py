#-*- coding: UTF-8 -*-
import json
from five import grok
from time import strftime, localtime 
from zope.component import getMultiAdapter

from my315ok.socialorgnization.content.governmentdepartment import IOrgnization
from dexterity.membrane.interfaces import ICreateMembraneEvent,ICreateBonusRecorderEvent
from dexterity.membrane.content.memberfolder import IMemberfolder
from dexterity.membrane.content.member import IMember
from Products.DCWorkflow.interfaces import IAfterTransitionEvent
from Products.DCWorkflow.events import AfterTransitionEvent 

from Products.CMFCore.utils import getToolByName

from plone.dexterity.utils import createContentInContainer

from zope.site.hooks import getSite
from zope.component import getUtility
  

#from Products.CMFCore.Expression import Expression
#from Products.CMFPlone.PloneBaseTool import getExprContext
from Products.PlonePAS.interfaces.events import IUserInitialLoginInEvent

from zope.interface import Interface
from ZODB.POSException import ConflictError
from zExceptions import Forbidden

from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFPlone import PloneMessageFactory as _p
#from collective.singing import mail

##@grok.subscribe(IMember, IObjectModifiedEvent)
#def trigger_member_workflow(member, event):
#    wtool = getToolByName(member, 'portal_workflow')
#    wtool.doActionFor(member, 'autotrigger')

def getMember(context,email):
    "get member object from email"
    catalog = getToolByName(context, "portal_catalog")
    memberbrains = catalog(object_provides=IMember.__identifier__,
                               email=email)

    if len(memberbrains) == 0:return None
    return memberbrains[0].getObject()

def updateSponsorOperator(obj,event):
    "创建sponsormember对象时，触发，更新该sponsormember关联的governmentorganization的operator记录"
    
    catalog = getToolByName(obj,'portal_catalog')

    bns = catalog.unrestrictedSearchResults({'object_provides': IOrgnization.__identifier__,
                                             'orgnization_supervisor':obj.orgname})
    if bns:
        org = bns[0].getObject()
        org.operator = obj.mail
        org.reindexObject()
    else:
        pass
        



# be call by membrane.usersinout
#@grok.subscribe(ICreateMembraneEvent)
def CreateMembraneEvent(event):
    """this event be fired by member join event, username,address password parameters to create a membrane object"""
    site = getSite()
#    mp = getToolByName(site,'portal_membership')
#    members = mp.getMembersFolder()
#    if members is None: return      
    catalog = getToolByName(site,'portal_catalog')
    try:
        newest = catalog.unrestrictedSearchResults({'object_provides': IMemberfolder.__identifier__})
    except:
        return      

    memberfolder = newest[0].getObject()
#    import pdb
#    pdb.set_trace()
#    oldid = getattr(memberfolder,'registrant_increment','999999')
#    memberid = str(int(oldid) + 1)
    memberid = event.id        
    try:
        item =createContentInContainer(memberfolder,"dexterity.membrane.member",checkConstraints=False,id=memberid)
        setattr(memberfolder,'registrant_increment',memberid)
        item.email = event.email
        item.password = event.password
        item.title = event.title 
        item.description = event.description
        item.homepage = event.homepage
        item.phone = event.phone
        item.organization = event.organization 
        item.sector = event.sector
        item.position = event.position
        item.province = event.province 
        item.address = event.address         

        membrane = getToolByName(item, 'membrane_tool')
        membrane.reindexObject(item)        
    except:
        return
    
#@grok.subscribe(Interface, IUserInitialLoginInEvent)
def userInitialLogin(obj, event):
    """Redirects initially logged in users to getting started wizard"""  
    # get portal object
    portal = getSite()  
    # check if we have an access to request object
    request = getattr(portal, 'REQUEST', None)
    if not request:
        return  
    # now complile and render our expression to url

    try:
        member_url_view = getMultiAdapter((portal, request),name=u"member_url") 
        url = member_url_view()
    except Exception, e:
        logException(u'Error during user initial login redirect')
        return
    else:
        # check if came_from is not empty, then clear it up, otherwise further
        # Plone scripts will override our redirect
        if request.get('came_from'):
            request['came_from'] = ''
            request.form['came_from'] = ''
        request.RESPONSE.redirect(url)    

# be call by bonus operation
#@grok.subscribe(ICreateBonusRecorderEvent)
def CreateBonusRecorderEvent(event):

    who = event.who  #this should be a email address 

    site = getSite()
    pm = getToolByName(site,'portal_membership')
    userobject = pm.getMemberById(who)
#    userobject = mp.getAuthenticatedMember()
#    username = userobject.getUserName()
#    username = "12@qq.com"    
    recorders = list(userobject.getProperty('bonusrecorder'))
    member = getMember(site,who)
    if not(member  is None):
        who = member.title
        member.bonus = member.bonus + 2
        member.reindexObject()
    recorder = u"%s于%s日，因为%s<a href='%s'>%s<a>而%s%s积分。" %(who,
                                        event.when,
                                        event.what,
                                        event.obj_url,                                        
                                        event.obj_title,
                                        event.result,
                                        event.bonus)        
#    start = datetime.today().strftime('%Y-%m-%d')
#    recorder = "%s 于%s因参加活动<a href='%s'>%s</a>而获取%s积分。" %(username,start,obj.absolute_url(),obj.title,2)
#    
    recorders.append(recorder)
    userobject.setProperties(bonusrecorder=recorders)                        
                            
    
        
