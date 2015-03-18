# ./NoOperation.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:2822c36b4c9082ba7843008891500b6fadea2c31
# Generated 2015-03-14 19:33:48.601359 by PyXB version 1.2.4 using Python 2.7.9.final.0
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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:a7a83182-ca78-11e4-bab4-080027c51aaa')

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


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/NoOperation.xsd', 4, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.mini.pw.edu.pl/ucc/}BackupCommunicationServers uses Python identifier BackupCommunicationServers
    __BackupCommunicationServers = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BackupCommunicationServers'), 'BackupCommunicationServers', '__httpwww_mini_pw_edu_plucc_CTD_ANON_httpwww_mini_pw_edu_pluccBackupCommunicationServers', False, pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/NoOperation.xsd', 7, 8), )

    
    BackupCommunicationServers = property(__BackupCommunicationServers.value, __BackupCommunicationServers.set, None, None)

    _ElementMap.update({
        __BackupCommunicationServers.name() : __BackupCommunicationServers
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/NoOperation.xsd', 8, 10)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.mini.pw.edu.pl/ucc/}BackupCommunicationServer uses Python identifier BackupCommunicationServer
    __BackupCommunicationServer = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BackupCommunicationServer'), 'BackupCommunicationServer', '__httpwww_mini_pw_edu_plucc_CTD_ANON__httpwww_mini_pw_edu_pluccBackupCommunicationServer', False, pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/NoOperation.xsd', 10, 14), )

    
    BackupCommunicationServer = property(__BackupCommunicationServer.value, __BackupCommunicationServer.set, None, None)

    _ElementMap.update({
        __BackupCommunicationServer.name() : __BackupCommunicationServer
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type EMPTY
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/NoOperation.xsd', 11, 16)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute address uses Python identifier address
    __address = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'address'), 'address', '__httpwww_mini_pw_edu_plucc_CTD_ANON_2_address', pyxb.binding.datatypes.anyURI)
    __address._DeclarationLocation = pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/NoOperation.xsd', 13, 18)
    __address._UseLocation = pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/NoOperation.xsd', 13, 18)
    
    address = property(__address.value, __address.set, None, None)

    
    # Attribute port uses Python identifier port
    __port = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'port'), 'port', '__httpwww_mini_pw_edu_plucc_CTD_ANON_2_port', pyxb.binding.datatypes.unsignedShort)
    __port._DeclarationLocation = pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/NoOperation.xsd', 15, 18)
    __port._UseLocation = pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/NoOperation.xsd', 15, 18)
    
    port = property(__port.value, __port.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __address.name() : __address,
        __port.name() : __port
    })



NoOperation = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NoOperation'), CTD_ANON, location=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/NoOperation.xsd', 3, 2))
Namespace.addCategoryObject('elementBinding', NoOperation.name().localName(), NoOperation)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BackupCommunicationServers'), CTD_ANON_, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/NoOperation.xsd', 7, 8)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BackupCommunicationServers')), pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/NoOperation.xsd', 7, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton()




CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BackupCommunicationServer'), CTD_ANON_2, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/NoOperation.xsd', 10, 14)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/NoOperation.xsd', 10, 14))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BackupCommunicationServer')), pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/NoOperation.xsd', 10, 14))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_._Automaton = _BuildAutomaton_()

