# ./SolveRequest.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:2822c36b4c9082ba7843008891500b6fadea2c31
# Generated 2015-03-20 11:15:45.319822 by PyXB version 1.2.4 using Python 2.7.9.final.0
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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:124f8a24-ceea-11e4-95dd-080027c51aaa')

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
    _XSDLocation = pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/SolveRequest.xsd', 4, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.mini.pw.edu.pl/ucc/}ProblemType uses Python identifier ProblemType
    __ProblemType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ProblemType'), 'ProblemType', '__httpwww_mini_pw_edu_plucc_CTD_ANON_httpwww_mini_pw_edu_pluccProblemType', False, pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/SolveRequest.xsd', 7, 6), )

    
    ProblemType = property(__ProblemType.value, __ProblemType.set, None, None)

    
    # Element {http://www.mini.pw.edu.pl/ucc/}SolvingTimeout uses Python identifier SolvingTimeout
    __SolvingTimeout = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SolvingTimeout'), 'SolvingTimeout', '__httpwww_mini_pw_edu_plucc_CTD_ANON_httpwww_mini_pw_edu_pluccSolvingTimeout', False, pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/SolveRequest.xsd', 9, 6), )

    
    SolvingTimeout = property(__SolvingTimeout.value, __SolvingTimeout.set, None, None)

    
    # Element {http://www.mini.pw.edu.pl/ucc/}Data uses Python identifier Data
    __Data = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Data'), 'Data', '__httpwww_mini_pw_edu_plucc_CTD_ANON_httpwww_mini_pw_edu_pluccData', False, pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/SolveRequest.xsd', 11, 6), )

    
    Data = property(__Data.value, __Data.set, None, None)

    
    # Element {http://www.mini.pw.edu.pl/ucc/}Id uses Python identifier Id
    __Id = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Id'), 'Id', '__httpwww_mini_pw_edu_plucc_CTD_ANON_httpwww_mini_pw_edu_pluccId', False, pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/SolveRequest.xsd', 13, 6), )

    
    Id = property(__Id.value, __Id.set, None, None)

    _ElementMap.update({
        __ProblemType.name() : __ProblemType,
        __SolvingTimeout.name() : __SolvingTimeout,
        __Data.name() : __Data,
        __Id.name() : __Id
    })
    _AttributeMap.update({
        
    })



SolveRequest = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SolveRequest'), CTD_ANON, location=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/SolveRequest.xsd', 3, 0))
Namespace.addCategoryObject('elementBinding', SolveRequest.name().localName(), SolveRequest)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProblemType'), pyxb.binding.datatypes.string, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/SolveRequest.xsd', 7, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SolvingTimeout'), pyxb.binding.datatypes.unsignedLong, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/SolveRequest.xsd', 9, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Data'), pyxb.binding.datatypes.base64Binary, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/SolveRequest.xsd', 11, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Id'), pyxb.binding.datatypes.unsignedLong, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/SolveRequest.xsd', 13, 6)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/SolveRequest.xsd', 9, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/SolveRequest.xsd', 13, 6))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ProblemType')), pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/SolveRequest.xsd', 7, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SolvingTimeout')), pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/SolveRequest.xsd', 9, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Data')), pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/SolveRequest.xsd', 11, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Id')), pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/SolveRequest.xsd', 13, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton()

