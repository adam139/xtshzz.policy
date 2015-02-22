# -*- coding: utf-8 -*-
from zope.interface import alsoProvides, implements
from zope.interface import Interface
from zope.interface import implementer
from zope.component import adapter
import datetime
from plone.app.content.interfaces import INameFromTitle

class INameFromYear(Interface):
    """ Interface to adapt to INameFromTitle """

@implementer(INameFromTitle)
@adapter(INameFromYear)
class NameFromYear(object):
    """ Adapter to INameFromTitle """
#    implements(INameFromTitle)
#    adapts(INameFromYear)

    def __init__(self, context):
        pass

    def __new__(cls, context):
#        org = context.brand
        year = (datetime.datetime.today() + datetime.timedelta(-365)).strftime("%Y")    
        title = u'%s' % (year)
        inst = super(NameFromYear, cls).__new__(cls)

        inst.title = title
#        context.setTitle(title)

        return inst


