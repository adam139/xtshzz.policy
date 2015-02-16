# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from plone.dexterity.utils import createContentInContainer
from my315ok.socialorgnization.content.orgnization import IOrgnization,IOrgnization_annual_survey

from my315ok.socialorgnization.content.orgnizationfolder import IOrgnizationFolder
from plone.i18n.normalizer.interfaces import INormalizer
from zope.component import getUtility

def publish_survey(context):
    "将旧的社会组织年检数据直接发布为published状态"
    pc = getToolByName(context, "portal_catalog")
    wf = getToolByName(context, 'portal_workflow')
    query = {"object_provides":IOrgnization_annual_survey.__identifier__}
    bns = pc(query)
    for bn in bns:
        if bn.review_state  == "draft":  # after modify workflow and add directly publish transition.
            ob = bn.getObject()

            wf.doActionFor(ob, 'publish', comment='迁移数据，将原始年检直接标记为发布状态。' )


def publish_organization(context):
    "将旧的社会组织数据直接发布为published状态"
    pc = getToolByName(context, "portal_catalog")
    wf = getToolByName(context, 'portal_workflow')
    query = {"object_provides":IOrgnization.__identifier__}
    bns = pc(query)
    for bn in bns:
        if bn.review_state  == "private":
            ob = bn.getObject()
           
            wf.doActionFor(ob, 'publish', comment='old org init as published status' )
        
    
    
def init_governmentdepartment(context):
    "将归属湘潭市的社会组织提取出来，为每个对象创建一个上级监管单位"
    
    pc = getToolByName(context, "portal_catalog")
    query = {"object_provides":IOrgnizationFolder.__identifier__}
    bns = pc(query)
    folder = bns[0].getObject()
    query = {"object_provides":IOrgnization.__identifier__,"orgnization_belondtoArea":"xiangtanshi"}
    bns = pc(query)
    # create government department data
    title2id = getUtility(INormalizer,'zh')
    ts = [i.orgnization_supervisor for i in bns]
    bsset = set(ts)
    for title in bsset:
        if title == "" or title == None:continue        
        if not isinstance(title, unicode):
            title = unicode(title, 'utf-8')                    
        # call title to id utility
        id = title2id.normalize(title)
        try:
            item =createContentInContainer(folder,
                                           "my315ok.socialorgnization.governmentorgnization",
                                           checkConstraints=False,
                                           id=id,
                                           title=title)
            item.reindex()
#            setattr(item,'title',title)
        except:
            pass

        
        
    
    
    

