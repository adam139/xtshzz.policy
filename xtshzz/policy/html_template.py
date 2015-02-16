# -*- coding: utf-8 -*-

message = """<html>
<body>
<p>%(from)s</p>

%(message)s

<hr/>
<p><a href="%(url)s">%(url_text)s</a></p>
</body>
</html>
"""
# dummy i18n helper for workflow states
#from zope.i18nmessageid import MessageFactory
from Products.CMFPlone import PloneMessageFactory as _p
#_p = MessageFactory('plone')
dummy = _p("published")
dummy = _p("draft")
dummy = _p("pendingsponsor")
dummy = _p("pendingagent")

#_p = MessageFactory('plone')
dummy = _p("published")
dummy = _p("draft")
dummy = _p("pendingsponsor")
dummy = _p("Agree")
dummy = _p("Veto")

# translate customize roles name. them are come form rolemap.xml
#dummy = _p("Social Organization")
#dummy = _p("Sponsor")
#dummy = _p("Civil Agent")