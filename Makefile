# This makefile is mainly used to run sparql query on the nmdco onotology
# To create ontology files, use the Makefile in src/ontology
ONT=	nmdco
ROBOT=	robot

.PHONY: .FORCE test-query

test-query:
	$(ROBOT) query \
	  --input $(ONT)-rg.ttl \
	  --query src/sparql/nmdco-test.sparql subset-files/temp.tsv

subset-files/astronomical-body-parts.tsv: .FORCE
	$(ROBOT) query \
	  --input $(ONT)-rg.ttl \
	  --query src/sparql/astronomical-body-parts.sparql $@