#!/bin/bash

DIR=/home/pio/IO2/Project/xml/
NAME=DivideProblem
pyxbgen -u $DIR/$NAME.xsd -m $NAME --schema-root . --allow-builtin-generation
NAME=NoOperation
pyxbgen -u $DIR/$NAME.xsd -m $NAME --schema-root . --allow-builtin-generation
NAME=PartialProblems
pyxbgen -u $DIR/$NAME.xsd -m $NAME --schema-root . --allow-builtin-generation
NAME=Register
pyxbgen -u $DIR/$NAME.xsd -m $NAME --schema-root . --allow-builtin-generation
NAME=RegisterResponse
pyxbgen -u $DIR/$NAME.xsd -m $NAME --schema-root . --allow-builtin-generation
NAME=Solution
pyxbgen -u $DIR/$NAME.xsd -m $NAME --schema-root . --allow-builtin-generation
NAME=SolutionRequest
pyxbgen -u $DIR/$NAME.xsd -m $NAME --schema-root . --allow-builtin-generation
NAME=SolveRequest
pyxbgen -u $DIR/$NAME.xsd -m $NAME --schema-root . --allow-builtin-generation 
NAME=SolveRequestResponse
pyxbgen -u $DIR/$NAME.xsd -m $NAME --schema-root . --allow-builtin-generation
NAME=Status
pyxbgen -u $DIR/$NAME.xsd -m $NAME --schema-root . --allow-builtin-generation




 
