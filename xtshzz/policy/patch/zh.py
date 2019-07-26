# -*- coding: UTF-8 -*-

from plone.i18n.normalizer.base import mapUnicode
from plone.i18n.normalizer.interfaces import INormalizer
# Chinese character to pinyin mapping
from xtshzz.policy.patch.pinyin import PinYinDict as mapping
from zope.interface import implements


class Normalizer(object):
    """
    This normalizer can normalize any unicode string and returns a version
    that only contains of ASCII characters.

    Let's make sure that this implementation actually fulfills the API.

      >>> from zope.interface.verify import verifyClass
      >>> verifyClass(INormalizer, Normalizer)
      True

      >>> norm = Normalizer()
      >>> norm.normalize(u'\u0429')
      'SCH'
    """
    implements(INormalizer)

    def normalize(self, text, locale=None, max_length=None):
        """
        Returns a normalized text. text has to be a unicode string.
        """

        return mapUnicode(text, mapping=mapping)


normalizer = Normalizer()
