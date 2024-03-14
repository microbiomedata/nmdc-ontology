## Customize Makefile settings for nmdco
## 
## If you need to customize your Makefile, make
## changes here rather than in the main Makefile

# except that ship has already sailed

# https://github.com/INCATools/ontology-development-kit/releases/tag/v1.5 vs ODK_VERSION_MAKEFILE = v1.2.27

# UBERON:0001153 caecum
# UBERON:0035118 material entity in digestive tract

#robot extract --method STAR \
#    --input filtered.owl \
#    --term-file uberon_module.txt \
#    --output results/uberon_module.owl

# -a,--annotate-with-source <arg>        if true, annotate terms with
#                                        rdfs:isDefinedBy
#    --add-prefix <arg>                  add prefix 'foo: http://bar' to
#                                        the output
#    --add-prefixes <arg>                add JSON-LD prefixes to the output
# -b,--branch-from-term <arg>            root term of branch to extract
# -B,--branch-from-terms <arg>           root terms of branches to extract
# -c,--copy-ontology-annotations <arg>   if true, include ontology
#                                        annotations
#    --catalog <arg>                     use catalog from provided file
# -f,--force <arg>                       if true, warn on empty input terms
#                                        instead of fail
# -h,--help                              print usage information
# -i,--input <arg>                       load ontology from a file
# -I,--input-iri <arg>                   load ontology from an IRI
# -l,--lower-term <arg>                  lower level term to extract
# -L,--lower-terms <arg>                 lower level terms to extract
# -m,--method <arg>                      extract method to use: star, top,
#                                        bot, mireot, subset
# -M,--imports <arg>                     handle imports (default: include)
# -n,--individuals <arg>                 handle individuals (default:
#                                        include)
# -N,--intermediates <arg>               specify how to handle intermediate
#                                        entities
#    --noprefixes                        do not use default prefixes
# -o,--output <arg>                      save ontology to a file
# -O,--output-iri <arg>                  set OntologyIRI for output
# -p,--prefix <arg>                      add a prefix 'foo: http://bar'
# -P,--prefixes <arg>                    use prefixes from JSON-LD file
# -s,--sources <arg>                     specify a mapping file of term to
#                                        source ontology
#    --strict                            use strict parsing when loading an
#                                        ontology
# -t,--term <arg>                        term to extract
# -T,--term-file <arg>                   load terms from a file
# -u,--upper-term <arg>                  upper level term to extract
# -U,--upper-terms <arg>                 upper level terms to extract
# -V,--version                           print version information
# -v,--verbose                           increased logging
# -vv,--very-verbose                     high logging
# -vvv,--very-very-verbose               maximum logging, including stack
#                                        traces
# -x,--xml-entities                      use entity substitution with
#                                        ontology XML output


#robot mirror --input test.owl \
#  --directory results/my-cache \
#  --output results/my-catalog.xml

imports/uberon_import.ttl:
#	rm -f \
#		nmdco-classes.json \
#		nmdco.json \
#		nmdco.owl
#	rm -f \
#		subsets/astronomical-body-parts-and-manufactured-products.tsv \
#		subsets/astronomical-body-parts.tsv \
#		subsets/manufactured-products.tsv \
#		subsets/non-terrestrial-biomes.tsv \
#		subsets/soil-environmental-materials.tsv \
#		subsets/terrestrial-biomes.tsv
#	rm -f \
#		imports/envo_import.owl \
#		imports/po_import.owl \
#		imports/ro_import.owl
	echo "\n** trying an extract import **"
#	robot --catalog catalog-v001.xml merge -I http://purl.obolibrary.org/obo/po.owl \
#	  annotate --remove-annotations \
#			   --annotation owl:versionInfo 2024-03-14 \
#			   --ontology-iri http://purl.obolibrary.org/obo/nmdco/imports/po_import.owl  \
#			   --version-iri http://purl.obolibrary.org/obo/nmdco/releases/2024-03-14/imports/po_import.owl \
#			   --output imports/po_import.owl.tmp.owl && mv imports/po_import.owl.tmp.owl imports/po_import.owl
	robot --catalog catalog-v001.xml extract \
			--method BOT \
			--input-iri http://purl.obolibrary.org/obo/uberon.owl \
			--term UBERON:0035118 \
			--term UBERON:0001153 \
		annotate --remove-annotations \
		   --annotation owl:versionInfo 2024-03-14 \
		   --ontology-iri http://purl.obolibrary.org/obo/nmdco/imports/uberon_import.owl  \
		   --version-iri http://purl.obolibrary.org/obo/nmdco/releases/2024-03-14/imports/uberon_import.owl \
		--output $@