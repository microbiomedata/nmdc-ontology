## Customize Makefile settings for nmdco
## 
## If you need to customize your Makefile, make
## changes here rather than in the main Makefile

# except that ship has already sailed

# https://github.com/INCATools/ontology-development-kit/releases/tag/v1.5 vs ODK_VERSION_MAKEFILE = v1.2.27

# UBERON:0001153 caecum
# UBERON:0035118 material entity in digestive tract

#robot mirror --input test.owl \
#  --directory results/my-cache \
#  --output results/my-catalog.xml

imports/uberon_import.owl:
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

imports/%_extract.owl: imports/report-unlabelled-classes.txt
	# use base ? maybe pato is the only source that asserts relations between chebi role and bfo role
	robot extract \
		--method TOP \
		--input-iri $(subst _extract.owl,.owl,$(subst imports/,https://purl.obolibrary.org/obo/,$@)) \
		--term-file $< \
		annotate --remove-annotations --output $@

do-extracts: imports/bfo_extract.owl \
imports/chebi_extract.owl \
imports/cob_extract.owl \
imports/fao_extract.owl \
imports/foodon_extract.owl \
imports/go_extract.owl \
imports/iao_extract.owl \
imports/ogms_extract.owl \
imports/pato_extract.owl \
imports/pco_extract.owl \
imports/so_extract.owl \
imports/uberon_extract.owl \
imports/upheno_extract.owl

# skipping  ncbitaxon for now
# imports/upheno_extract.owl slow