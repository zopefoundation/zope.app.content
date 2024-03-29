##############################################################################
#
# Copyright (c) 2002 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Content Type convenience lookup functions."""

from zope.componentvocabulary.vocabulary import UtilityVocabulary
from zope.interface import providedBy
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.security.proxy import removeSecurityProxy

from zope.app.content.interfaces import IContentType


def queryType(object, interface):
    """Returns the object's interface which implements interface.

    >>> from zope.interface import Interface
    >>> class IContentType(Interface):
    ...    pass
    >>> from zope.interface import Interface, implementer, directlyProvides
    >>> class I(Interface):
    ...     pass
    >>> class J(Interface):
    ...     pass
    >>> directlyProvides(I, IContentType)

    >>> @implementer(I)
    ... class C(object):
    ...     pass

    >>> @implementer(J, I)
    ... class D(object):
    ...     pass

    >>> obj = C()
    >>> c1_ctype = queryType(obj, IContentType)
    >>> c1_ctype.__name__
    'I'
    >>> class I1(I):
    ...     pass
    >>> class I2(I1):
    ...     pass
    >>> class I3(Interface):
    ...     pass

    >>> @implementer(I1)
    ... class C1(object):
    ...     pass

    >>> obj1 = C1()
    >>> c1_ctype = queryType(obj1, IContentType)
    >>> c1_ctype.__name__
    'I'

    >>> @implementer(I2)
    ... class C2(object):
    ...     pass
    >>> obj2 = C2()
    >>> c2_ctype = queryType(obj2, IContentType)
    >>> c2_ctype.__name__
    'I'

    >>> @implementer(I3)
    ... class C3(object):
    ...     pass
    >>> obj3 = C3()

    If Interface doesn't provide `IContentType`, `queryType` returns ``None``.

    >>> c3_ctype = queryType(obj3, IContentType)
    >>> c3_ctype
    >>> c3_ctype is None
    True
    >>> class I4(I):
    ...     pass
    >>> directlyProvides(I4, IContentType)

    >>> @implementer(I4)
    ... class C4(object):
    ...     pass
    >>> obj4 = C4()
    >>> c4_ctype = queryType(obj4, IContentType)
    >>> c4_ctype.__name__
    'I4'

    """
    # Remove the security proxy, so that we can introspect the type of the
    # object's interfaces.
    naked = removeSecurityProxy(object)
    object_iro = providedBy(naked).__iro__
    for iface in object_iro:
        if interface.providedBy(iface):
            return iface
    return None


def queryContentType(object):
    """Returns the interface implemented by object which implements
    :class:`zope.app.content.interfaces.IContentType`.

    >>> from zope.interface import Interface, implementer, directlyProvides
    >>> class I(Interface):
    ...     pass
    >>> directlyProvides(I, IContentType)

    >>> @implementer(I)
    ... class C(object):
    ...     pass

    >>> obj = C()
    >>> c1_ctype = queryContentType(obj)
    >>> c1_ctype.__name__
    'I'

    """
    return queryType(object, IContentType)


@provider(IVocabularyFactory)
class ContentTypesVocabulary(UtilityVocabulary):
    interface = IContentType
