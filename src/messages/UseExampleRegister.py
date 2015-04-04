import Register

mes = Register.CreateFromDocument("\
﻿<?xml version=\"1.0\" encoding=\"utf-8\" ?>\
<Register  xmlns=\"http://www.mini.pw.edu.pl/ucc/\"\
               xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\
               xsi:noNamespaceSchemaLocation=\"Register.xsd\">\
  <Type>TaskManager</Type>\
  <SolvableProblems>\
    <ProblemName>TSP</ProblemName>\
    <ProblemName>3-SAT</ProblemName>\
    <ProblemName>DVRP</ProblemName>\
    <ProblemName>GraphColoring</ProblemName>\
  </SolvableProblems>\
  <ParallelThreads>8</ParallelThreads>\
  <Deregister>false</Deregister>\
  <Id>12</Id>\
</Register>")
