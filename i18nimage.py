##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
Revision Information:
$Id: i18nimage.py,v 1.3 2003/05/01 19:35:10 faassen Exp $
"""

from zope.app.content.image import Image, getImageInfo
from zope.app.content.i18nfile import I18nFile
from zope.app.interfaces.content.i18nimage import II18nImage

class I18nImage(I18nFile):
    """An internationalized Image object.  Note that images of all
    languages share the same content type.
    """

    __implements__ = II18nImage


    def _create(self, data):
        return Image(data)


    def setData(self, data, language=None):
        '''See interface IFile'''
        super(I18nImage, self).setData(data, language)

        if language is None or language == self.getDefaultLanguage():
            # Uploading for the default language only overrides content
            # type.  Note: do not use the argument data here, it doesn't
            # work.
            contentType = getImageInfo(self.getData(language))[0]
            if contentType:
                self.setContentType(contentType)


    def getImageSize(self, language=None):
        '''See interface IImage'''
        return self._get(language).getImageSize()
