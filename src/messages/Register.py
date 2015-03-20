# ./Register.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:2822c36b4c9082ba7843008891500b6fadea2c31
# Generated 2015-03-20 11:15:42.261348 by PyXB version 1.2.4 using Python 2.7.9.final.0
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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:10743326-ceea-11e4-a7c3-080027c51aaa')

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
    _XSDLocation = pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Register.xsd', 8, 10)
    _Documentation = None
STD_ANON._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON, enum_prefix=None)
STD_ANON.TaskManager = STD_ANON._CF_enumeration.addEnumeration(unicode_value='TaskManager', tag='TaskManager')
STD_ANON.ComputationalNode = STD_ANON._CF_enumeration.addEnumeration(unicode_value='ComputationalNode', tag='ComputationalNode')
STD_ANON.CommunicationServer = STD_ANON._CF_enumeration.addEnumeration(unicode_value='CommunicationServer', tag='CommunicationServer')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)

# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Register.xsd', 4, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.mini.pw.edu.pl/ucc/}Type uses Python identifier Type
    __Type = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Type'), 'Type', '__httpwww_mini_pw_edu_plucc_CTD_ANON_httpwww_mini_pw_edu_pluccType', False, pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Register.xsd', 7, 8), )

    
    Type = property(__Type.value, __Type.set, None, None)

    
    # Element {http://www.mini.pw.edu.pl/ucc/}SolvableProblems uses Python identifier SolvableProblems
    __SolvableProblems = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SolvableProblems'), 'SolvableProblems', '__httpwww_mini_pw_edu_plucc_CTD_ANON_httpwww_mini_pw_edu_pluccSolvableProblems', False, pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Register.xsd', 17, 8), )

    
    SolvableProblems = property(__SolvableProblems.value, __SolvableProblems.set, None, None)

    
    # Element {http://www.mini.pw.edu.pl/ucc/}ParallelThreads uses Python identifier ParallelThreads
    __ParallelThreads = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ParallelThreads'), 'ParallelThreads', '__httpwww_mini_pw_edu_plucc_CTD_ANON_httpwww_mini_pw_edu_pluccParallelThreads', False, pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Register.xsd', 25, 8), )

    
    ParallelThreads = property(__ParallelThreads.value, __ParallelThreads.set, None, None)

    
    # Element {http://www.mini.pw.edu.pl/ucc/}Deregister uses Python identifier Deregister
    __Deregister = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Deregister'), 'Deregister', '__httpwww_mini_pw_edu_plucc_CTD_ANON_httpwww_mini_pw_edu_pluccDeregister', False, pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Register.xsd', 27, 8), )

    
    Deregister = property(__Deregister.value, __Deregister.set, None, None)

    
    # Element {http://www.mini.pw.edu.pl/ucc/}Id uses Python identifier Id
    __Id = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Id'), 'Id', '__httpwww_mini_pw_edu_plucc_CTD_ANON_httpwww_mini_pw_edu_pluccId', False, pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Register.xsd', 30, 8), )

    
    Id = property(__Id.value, __Id.set, None, None)

    _ElementMap.update({
        __Type.name() : __Type,
        __SolvableProblems.name() : __SolvableProblems,
        __ParallelThreads.name() : __ParallelThreads,
        __Deregister.name() : __Deregister,
        __Id.name() : __Id
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
    _XSDLocation = pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Register.xsd', 18, 10)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.mini.pw.edu.pl/ucc/}ProblemName uses Python identifier ProblemName
    __ProblemName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ProblemName'), 'ProblemName', '__httpwww_mini_pw_edu_plucc_CTD_ANON__httpwww_mini_pw_edu_pluccProblemName', True, pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Register.xsd', 20, 14), )

    
    ProblemName = property(__ProblemName.value, __ProblemName.set, None, None)

    _ElementMap.update({
        __ProblemName.name() : __ProblemName
    })
    _AttributeMap.update({
        
    })



Register = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Register'), CTD_ANON, location=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Register.xsd', 3, 2))
Namespace.addCategoryObject('elementBinding', Register.name().localName(), Register)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Type'), STD_ANON, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Register.xsd', 7, 8)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SolvableProblems'), CTD_ANON_, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Register.xsd', 17, 8)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ParallelThreads'), pyxb.binding.datatypes.unsignedByte, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Register.xsd', 25, 8)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Deregister'), pyxb.binding.datatypes.boolean, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Register.xsd', 27, 8)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Id'), pyxb.binding.datatypes.unsignedLong, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Register.xsd', 30, 8)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Register.xsd', 27, 8))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Register.xsd', 30, 8))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Type')), pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Register.xsd', 7, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SolvableProblems')), pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Register.xsd', 17, 8))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ParallelThreads')), pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Register.xsd', 25, 8))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Deregister')), pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Register.xsd', 27, 8))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Id')), pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Register.xsd', 30, 8))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton()




CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProblemName'), pyxb.binding.datatypes.string, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Register.xsd', 20, 14)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Register.xsd', 20, 14))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ProblemName')), pyxb.utils.utility.Location('/home/pio/IO2/Project/xml/Register.xsd', 20, 14))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_._Automaton = _BuildAutomaton_()

