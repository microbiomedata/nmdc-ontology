# ----------------------------------------
# Makefile for nmdco
# Generated using ontology-development-kit
# ODK Version: v1.2.27
# ----------------------------------------
# IMPORTANT: DO NOT EDIT THIS FILE. To override default make goals, use nmdco.Makefile instead


# ----------------------------------------
# More information: https://github.com/INCATools/ontology-development-kit/


# ----------------------------------------
# Standard Constants
# ----------------------------------------
# these can be overwritten on the command line

URIBASE=                    http://purl.obolibrary.org/obo
ONT=                        nmdco
ONTBASE=                    $(URIBASE)/$(ONT)
EDIT_FORMAT=                owl
SRC =                       $(ONT)-edit.$(EDIT_FORMAT)
CATALOG=                    catalog-v001.xml
ROBOT=                      robot --catalog $(CATALOG)
RELEASEDIR=                 ../..
REPORTDIR=                  reports
TEMPLATEDIR=                ../templates
TMPDIR=                     tmp
SCRIPTSDIR=                 ../scripts
SPARQLDIR =                 ../sparql
IMPORTS_DIR =             	imports
REPORT_FAIL_ON =            None
REPORT_LABEL =              -l true
REPORT_PROFILE_OPTS =       
OBO_FORMAT_OPTIONS =        
SPARQL_VALIDATION_CHECKS =   equivalent-classes owldef-self-reference
SPARQL_EXPORTS =             basic-report class-count-by-prefix edges xrefs obsoletes synonyms
ODK_VERSION_MAKEFILE =      v1.2.27

TODAY ?=                    $(shell date +%Y-%m-%d)
OBODATE ?=                  $(shell date +'%d:%m:%Y %H:%M')
VERSION=                    $(TODAY)
ANNOTATION_PROPERTIES=rdfs:label IAO:0000115 
ANNOTATE_ONTOLOGY_VERSION = annotate -V $(ONTBASE)/releases/$(VERSION)/$@ --annotation owl:versionInfo $(VERSION)
OTHER_SRC =                 $(IMPORTS_DIR)/po_import.owl $(IMPORTS_DIR)/envo_import.owl $(IMPORTS_DIR)/ro_import.owl
IMPORTS =  					ro envo po
IMPORT_FILES =              $(IMPORTS_DIR)/po_import.owl $(IMPORTS_DIR)/envo_import.owl $(IMPORTS_DIR)/ro_import.owl

SUBSETS := \
	subsets/astronomical-body-parts.tsv \
	subsets/astronomical-body-parts-and-manufactured-products.tsv \
	subsets/non-terrestrial-biomes.tsv \
	subsets/terrestrial-biomes.tsv \
	subsets/soil-environmental-materials.tsv \
	subsets/manufactured-products.tsv

RELEASE_ARTEFACTS = $(ONT)-relation-graph.owl $(ONT).json $(ONT)-classes.json $(ONT).owl

# ----------------------------------------
# Top-level targets
# ----------------------------------------

.PHONY: .FORCE all all_imports all_main all_subsets clean test test-query test-subsets release release-subsets release-artefacts
.PHONY: refresh-imports refresh-% imports/%_import.owl refresh-all refresh-all-%

all: all_imports all_main all_subsets

all_main: $(RELEASE_ARTEFACTS)

refresh-all:
	make -B all_imports
	make -B all_main
	make -B all_subsets

refresh-all-%:
	make -B all_$*

# ----------------------------------------
# Release Management
# ----------------------------------------

release: release-artefacts release-subsets

release-artefacts: $(RELEASE_ARTEFACTS)
# copy artefacts to release directory
	@echo "\n** releasing $@ **"
	cp $^ $(RELEASEDIR)

release-subsets: $(SUBSETS)
# copy subsets to the release directory
	@echo "\n** releasing $@ **"
	cp $^ $(RELEASEDIR)/subsets

clean:
	rm -f $(RELEASE_ARTEFACTS)
	rm -f $(SUBSETS)
	rm -f $(IMPORT_FILES)

# ----------------------------------------
# Import modules
# ----------------------------------------

# Most ontologies are modularly constructed using portions of other ontologies
# These live in the imports/ folder
all_imports: $(IMPORT_FILES)

# -- Generate Import Modules --
imports/%_import.owl:
	@echo "\n** building $@ **"
	$(ROBOT) merge -I $(URIBASE)/$*.owl \
	  annotate --remove-annotations \
	           --ontology-iri $(ONTBASE)/$@  \
	           --version-iri $(ONTBASE)/releases/$(VERSION)/$@ \
	           --annotation owl:versionInfo $(VERSION) \
	  --output $@.tmp.owl && mv $@.tmp.owl $@

refresh-imports:
# force rebuild of all imports
	make -B $(IMPORT_FILES)

refresh-%:
# force rebuild a single import
	make -B imports/$*_import.owl

# -------------------------------------------
# Main release artefacts
# -------------------------------------------

##$(ONT).owl: $(ONT)-full.owl # reasoning is currently broken will need to fix!!!
$(ONT).owl: $(ONT)-merged.owl
	@echo "\n** building $@ **"
	$(ROBOT) annotate --input $< --ontology-iri $(URIBASE)/$@ $(ANNOTATE_ONTOLOGY_VERSION) \
		convert -o $@.tmp.owl && mv $@.tmp.owl $@

$(ONT)-relation-graph.owl: $(ONT).owl $(ONT)-merged-labels.ttl
# build relation-graph from nmdc-merged.ttl file
# for relation-graph see https://github.com/balhoff/relation-graph	
# note, you may need to increase Java memory: export JAVA_OPTS=-Xmx16G
	@echo "\n** building $@ **"
	relation-graph --ontology-file $< \
	    --reflexive-subclasses false \
	    --equivalence-as-subclass false \
	    --non-redundant-output-file $(ONT)-nonredundant.ttl \
	    --redundant-output-file $(ONT)-redundant.ttl \
	    --mode rdf
# merge in nmdco-merged for annotations
	$(ROBOT) merge \
	    --input $(word 2, $^) \
	    --input $(ONT)-nonredundant.ttl \
	    annotate --ontology-iri $(ONTBASE)/$@ \
	    $(ANNOTATE_ONTOLOGY_VERSION) \
	    --output $@

$(ONT).json: $(ONT)-relation-graph.owl
# convert ontology to json
	@echo "\n** building $@ **"
	$(ROBOT) annotate --ontology-iri $(ONTBASE)/$@ --input $< \
	    $(ANNOTATE_ONTOLOGY_VERSION) \
	    convert --output $@

$(ONT)-classes.owl: $(ONT)-relation-graph.owl $(ONT)-merged-labels.ttl
# select classes and merge with the labels
	@echo "\n** building $@ **"
	$(ROBOT) filter --input $< \
	    --select classes \
	    merge --input $(word 2, $^) \
	    annotate --ontology-iri $(ONTBASE)/$@ \
	    $(ANNOTATE_ONTOLOGY_VERSION) \
	    --output $@

$(ONT)-classes.json: $(ONT)-classes.owl
# convert ontology to json
	@echo "\n** building $@ **"
	$(ROBOT) annotate --input $< --ontology-iri $(URIBASE)/$@ $(ANNOTATE_ONTOLOGY_VERSION) \
		convert -o $@.tmp.json && mv $@.tmp.json $@

# -----------------------------------------------------
# Variant artefacts
# -----------------------------------------------------

# Full: The full artefacts with imports merged, reasoned
$(ONT)-full.owl: $(ONT)-merged.owl
# reason over the merged file
	@echo "\n** building $@ **"
	$(ROBOT) reason --input $< --reasoner ELK --equivalent-classes-allowed all --exclude-tautologies structural \
		relax \
		reduce -r ELK \
		annotate --ontology-iri $(ONTBASE)/$@ $(ANNOTATE_ONTOLOGY_VERSION) --output $@.tmp.owl && mv $@.tmp.owl $@
# remove obsolete classes
	robot remove --input $@.tmp.owl \
	  --select "owl:deprecated='true'^^xsd:boolean" \
	  --output $@
# clean up
	rm -f $@.tmp.owl

$(ONT)-merged.owl: $(SRC) $(IMPORT_FILES)
# merge imports into single owl file
	@echo "\n** building $@ **"
	$(ROBOT) merge --input $< $(patsubst %, --input %, $(IMPORT_FILES)) \
	    annotate --ontology-iri $(ONTBASE)/$@ \
	    $(ANNOTATE_ONTOLOGY_VERSION) \
	    --output $@.tmp.owl
# remove obsolete classes
	robot remove --input $@.tmp.owl \
	    --select "owl:deprecated='true'^^xsd:boolean" \
	    --output $@
# clean up
	rm -f $@.tmp.owl

refresh-merged:
# force rebuild of merged ontology
	make -B $(ONT)-merged.owl

$(ONT)-merged.ttl: $(ONT)-merged.owl
# convert merged owl file to ttl
	@echo "\n** building $@ **"
	$(ROBOT) annotate --ontology-iri $(ONTBASE)/$@ --input $< \
	         convert --output $@

$(ONT)-merged-labels.ttl: $(ONT)-merged.ttl
# create an ontology of just the labels in the merged ontology
# this is needed so that we can easily view the ontology in protege
	@echo "\n** building $@ **"
	$(ROBOT) query --format ttl -i $< --query ../sparql/all-labels.sparql $@

$(ONTOLOGYTERMS): $(SRC) $(OTHER_SRC)
	@echo "\n** building $@ **"
	touch $(ONTOLOGYTERMS) && \
	$(ROBOT) query --use-graphs true -f csv -i $< --query ../sparql/nmdco_terms.sparql $@

# ----------------------------------------
# Subsets
# ----------------------------------------

all_subsets: $(SUBSETS)

test-query: $(ONT)-relation-graph.owl .FORCE
# a simple query to very that I can run a query
	$(ROBOT) query \
	  --input $< \
	  --query ../sparql/nmdco-test.sparql temp.tsv

test-subsets: $(SUBSETS) .FORCE
# test creating all subsets

subsets/astronomical-body-parts.tsv: $(ONT)-relation-graph.owl $(SPARQLDIR)/astronomical-body-parts.sparql
	@echo "\n** building $@ **"
	$(ROBOT) query \
	  --input $< \
	  --query $(word 2, $^) $@

subsets/astronomical-body-parts-and-manufactured-products.tsv: $(ONT)-relation-graph.owl $(SPARQLDIR)/astronomical-body-parts-and-manufactured-products.sparql
	@echo "\n** building $@ **"
	$(ROBOT) query \
	  --input $< \
	  --query $(word 2, $^) $@

subsets/non-terrestrial-biomes.tsv: $(ONT)-relation-graph.owl $(SPARQLDIR)/non-terrestrial-biomes.sparql
	@echo "\n** building $@ **"
	$(ROBOT) query \
	  --input $< \
	  --query $(word 2, $^) $@

subsets/terrestrial-biomes.tsv: $(ONT)-relation-graph.owl $(SPARQLDIR)/terrestrial-biomes.sparql
	@echo "\n** building $@ **"
	$(ROBOT) query \
	  --input $< \
	  --query $(word 2, $^) $@

subsets/soil-environmental-materials.tsv: $(ONT)-relation-graph.owl $(SPARQLDIR)/soil-environmental-materials.sparql
	@echo "\n** building $@ **"
	$(ROBOT) query \
	  --input $< \
	  --query $(word 2, $^) $@

subsets/manufactured-products.tsv: $(ONT)-relation-graph.owl $(SPARQLDIR)/manufactured-products.sparql
	@echo "\n** building $@ **"
	$(ROBOT) query \
	  --input $< \
	  --query $(word 2, $^) $@



include nmdco.Makefile
