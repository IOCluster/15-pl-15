# ./Error.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:2822c36b4c9082ba7843008891500b6fadea2c31
# Generated 2015-03-25 17:28:35.835754 by PyXB version 1.2.4 using Python 3.4.2.final.0
# Namespace http://www.mini.pw.edu.pl/ucc/

from __future__ import unicode_literals
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:fc3277f8-d30b-11e4-bfa1-c860008b05f1')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.4'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.mini.pw.edu.pl/ucc/', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword default_namespace The L{pyxb.Namespace} instance to use as the
    default namespace where there is no default namespace in scope.
    If unspecified or C{None}, the namespace of the module containing
    this function will be used.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement, default_namespace=default_namespace)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Atomic simple type: [anonymous]
class STD_ANON (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/samba/wisniewskip2/SEMESTR 6/IO2/SP1/Error.xsd', 12, 10)
    _Documentation = None
STD_ANON._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=STD_ANON)
STD_ANON.UnknownSender = STD_ANON._CF_enumeration.addEnumeration(unicode_value='UnknownSender', tag='UnknownSender')
STD_ANON.InvalidOperation = STD_ANON._CF_enumeration.addEnumeration(unicode_value='InvalidOperation', tag='InvalidOperation')
STD_ANON.ExceptionOccured = STD_ANON._CF_enumeration.addEnumeration(unicode_value='ExceptionOccured', tag='ExceptionOccured')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)

# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/samba/wisniewskip2/SEMESTR 6/IO2/SP1/Error.xsd', 9, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.mini.pw.edu.pl/ucc/}ErrorType uses Python identifier ErrorType
    __ErrorType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ErrorType'), 'ErrorType', '__httpwww_mini_pw_edu_plucc_CTD_ANON_httpwww_mini_pw_edu_pluccErrorType', False, pyxb.utils.utility.Location('/home/samba/wisniewskip2/SEMESTR 6/IO2/SP1/Error.xsd', 11, 8), )

    
    ErrorType = property(__ErrorType.value, __ErrorType.set, None, None)

    
    # Element {http://www.mini.pw.edu.pl/ucc/}ErrorMessage uses Python identifier ErrorMessage
    __ErrorMessage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ErrorMessage'), 'ErrorMessage', '__httpwww_mini_pw_edu_plucc_CTD_ANON_httpwww_mini_pw_edu_pluccErrorMessage', False, pyxb.utils.utility.Location('/home/samba/wisniewskip2/SEMESTR 6/IO2/SP1/Error.xsd', 25, 8), )

    
    ErrorMessage = property(__ErrorMessage.value, __ErrorMessage.set, None, None)

    _ElementMap.update({
        __ErrorType.name() : __ErrorType,
        __ErrorMessage.name() : __ErrorMessage
    })
    _AttributeMap.update({
        
    })



Error = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Error'), CTD_ANON, location=pyxb.utils.utility.Location('/home/samba/wisniewskip2/SEMESTR 6/IO2/SP1/Error.xsd', 8, 2))
Namespace.addCategoryObject('elementBinding', Error.name().localName(), Error)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ErrorType'), STD_ANON, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/samba/wisniewskip2/SEMESTR 6/IO2/SP1/Error.xsd', 11, 8)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ErrorMessage'), pyxb.binding.datatypes.string, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/samba/wisniewskip2/SEMESTR 6/IO2/SP1/Error.xsd', 25, 8)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/samba/wisniewskip2/SEMESTR 6/IO2/SP1/Error.xsd', 25, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ErrorType')), pyxb.utils.utility.Location('/home/samba/wisniewskip2/SEMESTR 6/IO2/SP1/Error.xsd', 11, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ErrorMessage')), pyxb.utils.utility.Location('/home/samba/wisniewskip2/SEMESTR 6/IO2/SP1/Error.xsd', 25, 8))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton()

