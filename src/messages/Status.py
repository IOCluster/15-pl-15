# ./Status.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:2822c36b4c9082ba7843008891500b6fadea2c31
# Generated 2015-03-14 19:33:53.011224 by PyXB version 1.2.4 using Python 2.7.9.final.0
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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:aa46a14e-ca78-11e4-80c1-080027c51aaa')

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
    _XSDLocation = pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 17, 20)
    _Documentation = None
STD_ANON._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON, enum_prefix=None)
STD_ANON.Idle = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Idle', tag='Idle')
STD_ANON.Busy = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Busy', tag='Busy')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)

# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 4, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.mini.pw.edu.pl/ucc/}Id uses Python identifier Id
    __Id = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Id'), 'Id', '__httpwww_mini_pw_edu_plucc_CTD_ANON_httpwww_mini_pw_edu_pluccId', False, pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 7, 6), )

    
    Id = property(__Id.value, __Id.set, None, None)

    
    # Element {http://www.mini.pw.edu.pl/ucc/}Threads uses Python identifier Threads
    __Threads = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Threads'), 'Threads', '__httpwww_mini_pw_edu_plucc_CTD_ANON_httpwww_mini_pw_edu_pluccThreads', False, pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 9, 6), )

    
    Threads = property(__Threads.value, __Threads.set, None, None)

    _ElementMap.update({
        __Id.name() : __Id,
        __Threads.name() : __Threads
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
    _XSDLocation = pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 10, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.mini.pw.edu.pl/ucc/}Thread uses Python identifier Thread
    __Thread = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Thread'), 'Thread', '__httpwww_mini_pw_edu_plucc_CTD_ANON__httpwww_mini_pw_edu_pluccThread', True, pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 12, 12), )

    
    Thread = property(__Thread.value, __Thread.set, None, None)

    _ElementMap.update({
        __Thread.name() : __Thread
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 13, 14)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.mini.pw.edu.pl/ucc/}State uses Python identifier State
    __State = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'State'), 'State', '__httpwww_mini_pw_edu_plucc_CTD_ANON_2_httpwww_mini_pw_edu_pluccState', False, pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 16, 18), )

    
    State = property(__State.value, __State.set, None, None)

    
    # Element {http://www.mini.pw.edu.pl/ucc/}HowLong uses Python identifier HowLong
    __HowLong = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'HowLong'), 'HowLong', '__httpwww_mini_pw_edu_plucc_CTD_ANON_2_httpwww_mini_pw_edu_pluccHowLong', False, pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 25, 18), )

    
    HowLong = property(__HowLong.value, __HowLong.set, None, None)

    
    # Element {http://www.mini.pw.edu.pl/ucc/}ProblemInstanceId uses Python identifier ProblemInstanceId
    __ProblemInstanceId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ProblemInstanceId'), 'ProblemInstanceId', '__httpwww_mini_pw_edu_plucc_CTD_ANON_2_httpwww_mini_pw_edu_pluccProblemInstanceId', False, pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 27, 18), )

    
    ProblemInstanceId = property(__ProblemInstanceId.value, __ProblemInstanceId.set, None, None)

    
    # Element {http://www.mini.pw.edu.pl/ucc/}TaskId uses Python identifier TaskId
    __TaskId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TaskId'), 'TaskId', '__httpwww_mini_pw_edu_plucc_CTD_ANON_2_httpwww_mini_pw_edu_pluccTaskId', False, pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 29, 18), )

    
    TaskId = property(__TaskId.value, __TaskId.set, None, None)

    
    # Element {http://www.mini.pw.edu.pl/ucc/}ProblemType uses Python identifier ProblemType
    __ProblemType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ProblemType'), 'ProblemType', '__httpwww_mini_pw_edu_plucc_CTD_ANON_2_httpwww_mini_pw_edu_pluccProblemType', False, pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 31, 18), )

    
    ProblemType = property(__ProblemType.value, __ProblemType.set, None, None)

    _ElementMap.update({
        __State.name() : __State,
        __HowLong.name() : __HowLong,
        __ProblemInstanceId.name() : __ProblemInstanceId,
        __TaskId.name() : __TaskId,
        __ProblemType.name() : __ProblemType
    })
    _AttributeMap.update({
        
    })



Status = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Status'), CTD_ANON, location=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 3, 0))
Namespace.addCategoryObject('elementBinding', Status.name().localName(), Status)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Id'), pyxb.binding.datatypes.unsignedLong, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 7, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Threads'), CTD_ANON_, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 9, 6)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Id')), pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 7, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Threads')), pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 9, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton()




CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Thread'), CTD_ANON_2, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 12, 12)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Thread')), pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 12, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_._Automaton = _BuildAutomaton_()




CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'State'), STD_ANON, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 16, 18)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HowLong'), pyxb.binding.datatypes.unsignedLong, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 25, 18)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProblemInstanceId'), pyxb.binding.datatypes.unsignedLong, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 27, 18)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TaskId'), pyxb.binding.datatypes.unsignedLong, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 29, 18)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProblemType'), pyxb.binding.datatypes.string, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 31, 18)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 25, 18))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 27, 18))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 29, 18))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 31, 18))
    counters.add(cc_3)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'State')), pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 16, 18))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'HowLong')), pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 25, 18))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ProblemInstanceId')), pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 27, 18))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TaskId')), pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 29, 18))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ProblemType')), pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Status.xsd', 31, 18))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_2._Automaton = _BuildAutomaton_2()

