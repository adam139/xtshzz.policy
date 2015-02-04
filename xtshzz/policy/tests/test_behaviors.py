# -*- coding: utf-8 -*-

import unittest


class TestBasic(unittest.TestCase):

    def _makeTwo(self):
        from dexterity.membrane.content.member import member
        dummy = member()

        from xtshzz.policy.behaviors.org import Org
        return Org(dummy)        


    def test_setter(self):
        b = self._makeTwo()

        b.orgname = u'foo'
        self.assertEqual(u'foo', b.context.orgname)



    def test_getter(self):
        b = self._makeTwo()
        b.context.orgname = u'foo'
        self.assertEqual(u'foo', b.orgname)



