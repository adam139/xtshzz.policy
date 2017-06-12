#-*- coding: UTF-8 -*-
from zope.interface import implements
from Acquisition import aq_inner
from zope.dottedname.resolve import resolve
from Products.Five.utilities.marker import mark
from zope.publisher.interfaces import IPublishTraverse
from Products.Five.browser import BrowserView
from zope.interface import Interface

from zExceptions import NotFound



class setLayout(BrowserView):
    """
    设置指定内容对象的视图名称，通过:contentobj@@set_layout?new_view_name形式来设置。
    """    
    implements(IPublishTraverse)        
    layout = None
    #receive url parameters
    def publishTraverse(self, request, name):

#         import pdb
#         pdb.set_trace()
        if self.layout is None:
            self.layout = name
            return self
        else:
            raise NotFound()
        
    def __call__(self):        
        obj = self.context
        datev = self.request.form.keys()[0]
        try:
            obj.setLayout(datev)
            return "success"
        except:
            return "error"   
    
class setDate(setLayout):
    """set content object create date for dexterity content types.
    通过:contentobj@@set_date?2016-08-08形式来设置。
    """

   
    def __call__(self):
#         datev = self.layout
        datev = self.request.form.keys()[0]
        from datetime import datetime
        context = self.context

        try:
            d= datetime.strptime(datev,'%Y-%m-%d')
        except:
             return "problem with parameter '%s'. usage: @@setdate?YYYY-MM-DD" % datev
        context.setModificationDate(datev)
        context.creation_date = datev
        context.setEffectiveDate(datev)
        context.reindexObject(idxs=['created', 'modified'])

        return "date on '%s' successfully set to %s." % (context.Title(), datev)    

class addMarkInterface(setLayout):
    """
    self.layout will be input a name of the mark interface ,this parameter come from browser request url
    # id is yourpackage.interfaces.IFoo.
    usage:http://host/yourobject/@@add_mark?yourpackage.interfaces.Imark
    """
    
    def __call__(self):

        ifid = self.request.form.keys()[0]
        try:
            ifobj = resolve(ifid)
        except:
            return "interface %s can not be resolved" % (ifid)
        context = aq_inner(self.context)
        mark(context,ifobj)        
        return "I has marked %s to provide %s" % (context.id,ifid)        