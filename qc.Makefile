RUN=poetry run

#ENVO_SEMSQL=downlaods/envo.db
SPARQL_ENDPOINT := http://3.236.215.220/repositories/nmdc-knowledgegraph

.PHONY: qc-all qc-clean

mirror/purl.obolibrary.org/obo/nmdco/imports/envo_import.owl: # todo slow
	robot mirror \
		-vvv \
		--input src/ontology/nmdco-edit.owl \
		--directory mirror

qc-all: qc-clean \
	mirror/purl.obolibrary.org/obo/nmdco/imports/envo_import.owl \
	qc-reports/report-asserted-equivalencies.tsv \
	qc-reports/report-cycles.tsv \
	downloads/envo-idranges.owl \
	downloads/envo-idranges.owl.ttl \
	downloads/envo.db \
	downloads/envo.owl \
	assets/misc_llm_input/extension_report.yaml \
	assets/misc_llm_input/report_envo_biome_annotations.yaml \
	assets/misc_llm_input/report_envo_environmental_material_annotations.yaml \
	assets/robot_diff.txt \
	qc-reports/biosample-triad-counts.tsv \
	qc-reports/envo-all-classes.txt \
	qc-reports/envo-biomes.txt \
	qc-reports/envo-environmental-materials.txt \
	qc-reports/envo-id-ranges-report.tsv \
	qc-reports/nmdco-envo-classes-with-id-owner.tsv \
	qc-reports/report-class-ids.tsv \
	qc-reports/report-id-ranges.tsv \
	qc-reports/report-unlabelled-classes.tsv \
	src/ontology/imports/report-unlabelled-classes.txt \
	qc-reports/problematic_triads.tsv

# todo doesn't include
# assets/environments_with_no_biome_mappings.raw.txt:
# assets/environments_with_no_biome_mappings.raw.yaml.txt:
# assets/material_environment_built_environment_mappings_raw.yaml.txt:

qc-clean:
	rm -rf qc-reports/*
	mkdir -p qc-reports
	touch qc-reports/.gitkeep
#	rm -rf downloads/*owl* downloads/*.db
#	mkdir -p downloads
#	touch downloads/.gitkeep
	rm -rf \
		assets/extension_report.yaml \
		assets/parse_robot_diff.tsv \
		assets/report_envo_biome_annotations.yaml \
		assets/report_envo_environmental_material_annotations.yaml \
		assets/robot_diff.txt \
		src/ontology/imports/report-unlabelled-classes.txt

downloads/envo.owl:
	@echo "Downloading..."
ifeq ($(shell command -v wget 2> /dev/null),)
	@echo "wget is not installed, trying with curl..."
	@curl -o $@ https://raw.githubusercontent.com/EnvironmentOntology/envo/master/envo.owl
else
	@echo "Downloading with wget..."
	@wget -O $@ https://raw.githubusercontent.com/EnvironmentOntology/envo/master/envo.owl
endif

qc-reports/report-class-ids.tsv: downloads/envo.owl
	robot query \
		--input $< \
		--query $(subst .tsv,.rq,$(subst qc-reports,qc-sparql,$@)) $@

downloads/envo.db:
	poetry run semsql download envo -o $@

# omn manchester syntax
downloads/envo-idranges.owl:
	@echo "Downloading..."
ifeq ($(shell command -v wget 2> /dev/null),)
	@echo "wget is not installed, trying with curl..."
	@curl -o $@ https://raw.githubusercontent.com/EnvironmentOntology/envo/master/src/envo/envo-idranges.owl
else
	@echo "Downloading with wget..."
	@wget -O $@ https://raw.githubusercontent.com/EnvironmentOntology/envo/master/src/envo/envo-idranges.owl
endif

qc-reports/report-id-ranges.tsv: downloads/envo-idranges.owl
	@echo "Querying..."
	robot query \
		--input $< \
		--query $(subst .tsv,.rq,$(subst qc-reports,qc-sparql,$@)) $@

downloads/envo-idranges.owl.ttl: downloads/envo-idranges.owl
	@echo "Converting..."
	@robot convert --input $< --output $@

qc-reports/envo-id-ranges-report.tsv: downloads/envo-idranges.owl.ttl
	@echo "Generating report..."
	$(RUN) report-id-ranges \
		--id-ranges-ttl $< \
		--output $@

qc-reports/biosample-triad-counts.tsv:
	@echo "Generating report..."
	$(RUN) report-instantiated-traids \
		--output $(subst counts.tsv,report.tsv,$@)  \
		--counts-output $@

qc-reports/nmdco-envo-classes-with-id-owner.tsv: qc-reports/envo-id-ranges-report.tsv nmdco-classes.json
	$(RUN) report-nmdco-envo-classes-by-id-owners \
		--id-range-tsv-input $(word 1,$^) \
		--nmdco-classes-json-input $(word 2,$^) \
		--output $@

qc-reports/envo-biomes.txt: downloads/envo.db
	$(RUN) runoak \
		--input $< descendants -p i biome | sort -t '!' -k2,2 > $@

qc-reports/envo-environmental-materials.txt: downloads/envo.db
	$(RUN) runoak \
		--input $< descendants -p i 'environmental material' | sort -t '!' -k2,2 > $@


qc-reports/envo-all-classes.txt: downloads/envo.db
	$(RUN) runoak \
		--input $< descendants -p i entity | sort -t '!' -k2,2 > $@

qc-reports/problematic_triads.tsv: qc-reports/envo-all-classes.txt \
qc-reports/envo-biomes.txt \
qc-reports/biosample-triad-report.tsv \
qc-reports/envo-environmental-materials.txt
	$(RUN) find-biosamples-with-problematic-triads \
		--all-envo-classes-file $(word 1, $^) \
		--biomes-file  $(word 2, $^) \
		--biosamples-file  $(word 3, $^) \
		--materials-file  $(word 4, $^) \
		--output $@ \
		--output-summary qc-reports/problematic_triad_summary.yaml

assets/robot_diff.txt: nmdco.owl src/ontology/nmdco-classes.owl
	robot diff \
		--left $< \
		--right $(word 2,$^) \
		--output $@

## this was a short term hack
#assets/parse_robot_diff.tsv: assets/robot_diff.txt
#	$(RUN) python nmdc_ontology/parse_robot_diff.py \
#		--input-file $< \
#		--output-file $@

qc-reports/report-cycles.tsv: mirror/purl.obolibrary.org/obo/nmdco/imports/envo_import.owl
	robot query \
		--input $< \
		--query $(subst .tsv,.rq,$(subst qc-reports,qc-sparql,$@)) $@


qc-reports/report-asserted-equivalencies.tsv: mirror/purl.obolibrary.org/obo/nmdco/imports/envo_import.owl
	robot query \
		--input $< \
		--query $(subst .tsv,.rq,$(subst qc-reports,qc-sparql,$@)) $@


qc-reports/report-unlabelled-classes.tsv: nmdco.owl
	robot query \
		--input $< \
		--query $(subst .tsv,.rq,$(subst qc-reports,qc-sparql,$@)) $@

src/ontology/imports/report-unlabelled-classes.txt: qc-reports/report-unlabelled-classes.tsv
	awk 'NR > 1 ' $< | tr -d '<>' > $@.tmp
	cat assets/additional-extracts.txt $@.tmp | sort -u > $@
	rm $@.tmp

###

#.PHONY: envo_mixs_all
#envo_mixs_all: envo_mixs_clean assets/mixs_environments_env_materials_subsets.yaml.txt
#
#.PHONY: envo_mixs_clean
#envo_mixs_clean: # todo update
#	rm -rf assets/extension_report.yaml \
#		assets/report_envo_environmental_material_annotations.tsv \
#		assets/mixs_environments_env_materials_subsets.yaml.txt

assets/extension_report.yaml: # todo fix these non-ascii characters upstream in MIxS
	$(RUN) report-mixs-extensions \
		--url https://raw.githubusercontent.com/GenomicsStandardsConsortium/mixs/main/assets/class_summary_results.tsv \
		--output-file $@

assets/report_envo_biome_annotations.yaml:
	$(RUN) report-envo-biome-annotations \
		--endpoint $(SPARQL_ENDPOINT) \
		--tsv-output $@ \
		--yaml-output assets/report_envo_biome_annotations.yaml

assets/report_envo_environmental_material_annotations.yaml:
	$(RUN) report-envo-environmental-material-annotations \
		--endpoint $(SPARQL_ENDPOINT) \
		--tsv-output assets/report_envo_environmental_material_annotations.tsv \
		--yaml-output $@

# 		--print-message


assets/iterative_environments_biomes_mappings_json_training.yaml.txt: assets/misc_llm_input/extension_report.yaml \
assets/misc_llm_input/report_envo_biome_annotations.yaml \
assets/mixs_context_subsets_example.json
	date && time $(RUN) python nmdc_ontology/iterative_mixs_environments_to_envo_biomes_by_claude.py \
		--mixs-file $(word 1,$^) \
		--envo-file $(word 2,$^) \
		--mappings-file $(word 3,$^) \
		--envo-description "biomes" \
		--temperature 0.01 \
		--max-tokens 4096 \
		--model claude-3-opus-20240229 \
		--suffix "" \
		--print-message


assets/iterative_environments_materials_mappings_json_training.yaml.txt: assets/misc_llm_input/extension_report.yaml \
assets/misc_llm_input/report_envo_environmental_material_annotations.yaml \
assets/mixs_context_subsets_example.json
	date && time $(RUN) python nmdc_ontology/iterative_mixs_environments_to_envo_materials_by_claude.py \
		--mixs-file $(word 1,$^) \
		--envo-file $(word 2,$^) \
		--mappings-file $(word 3,$^) \
		--envo-description "environmental materials" \
		--temperature 0.01 \
		--max-tokens 4096 \
		--model claude-3-opus-20240229 \
		--suffix "" \
		--print-message



assets/iterative_environments_biomes_mappings_denovo_raw.yaml.txt: assets/misc_llm_input/extension_report.yaml \
assets/misc_llm_input/report_envo_biome_annotations.yaml \
assets/misc_llm_mappings/biome_subsets_accepted_minimal.yaml
	date && time $(RUN) python nmdc_ontology/iterative_mixs_environments_to_envo_classes_by_claude.py \
		--mixs-file $(word 1,$^) \
		--envo-file $(word 2,$^) \
		--mappings-file $(word 3,$^) \
		--envo-description "biomes" \
		--temperature 0.01 \
		--max-tokens 4096 \
		--model claude-3-opus-20240229 \
		--suffix "Generate a mapping of MIxS environments to EnvO biomes, following the provided YAML format. Include all of the environments and all of the biomes. Many-to-many mappings are ok. The provided examples are incomplete, so fill in any additionally applicable mappings, even if that means repeating mappings from the examples. If you map biome X to environment Y, then also map any variants of X to Y. In a previous conversation you said 'The only EnvO biomes I did not map were the more specific marine biomes like neritic zone, benthic zone, hydrothermal vent, etc. The generic marine biome should cover those environments if needed.' Do not make judgments like that on your own. Include all mappings no matter whether they appear to be included in a more general term. After you provide the mappings, report any cases in which you have not followed these directions verbatim."


assets/environments_biomes_mappings_denovo_raw.yaml.txt: assets/misc_llm_input/extension_report.yaml \
assets/misc_llm_input/report_envo_biome_annotations.yaml \
assets/misc_llm_mappings/biome_subsets_accepted_minimal.yaml
	date && time $(RUN) mixs-environments-to-envo-classes-by-claude \
		--mixs-file $(word 1,$^) \
		--envo-file $(word 2,$^) \
		--mappings-file $(word 3,$^) \
		--envo-description "biomes" \
		--temperature 0.01 \
		--max-tokens 4096 \
		--model claude-3-opus-20240229 \
		--suffix "Generate a mapping of MIxS environments to EnvO biomes, following the provided YAML format. Include all of the environments and all of the biomes. Many-to-many mappings are ok. The provided examples are incomplete, so fill in any additionally applicable mappings, even if that means repeating mappings from the examples. If you map biome X to environment Y, then also map any variants of X to Y. In a previous conversation you said 'The only EnvO biomes I did not map were the more specific marine biomes like neritic zone, benthic zone, hydrothermal vent, etc. The generic marine biome should cover those environments if needed.' Do not make judgments like that on your own. Include all mappings no matter whether they appear to be included in a more general term. After you provide the mappings, report any cases in which you have not followed these directions verbatim." > $@


assets/environments_biomes_mappings_with_negatives_training_raw.yaml.txt: assets/misc_llm_input/extension_report.yaml \
assets/misc_llm_input/report_envo_biome_annotations.yaml \
assets/misc_llm_mappings/biome_subsets_training_with_unacceptables.yaml
	date && time $(RUN) mixs-environments-to-envo-classes-by-claude \
		--mixs-file $(word 1,$^) \
		--envo-file $(word 2,$^) \
		--mappings-file $(word 3,$^) \
		--envo-description "biomes" \
		--temperature 0.01 \
		--max-tokens 4096 \
		--model claude-3-opus-20240229 \
		--suffix "Generate an exhaustive, completely valid mapping of MIxS environments to EnvO biomes. Include all of the environments and all of the biomes if possible. I have provided some training data, including examples of unacceptable mappings. Please provide your results in the same format, but don't bother returning unacceptable mappings. Do not provide any introduction, commentary, summary or anything like that." > $@


assets/environments_with_no_biome_mappings.raw.yaml.txt: assets/misc_llm_input/extension_report.yaml assets/misc_llm_input/report_envo_biome_annotations.yaml assets/misc_llm_mappings/biome_subsets_accepted.yaml
	date && time $(RUN) mixs-environments-to-envo-classes-by-claude \
		--mixs-file $(word 1,$^) \
		--envo-file $(word 2,$^) \
		--mappings-file $(word 3,$^) \
		--envo-description biomes \
		--temperature 0.1 \
		--max-tokens 4096 \
		--model claude-3-opus-20240229 \
		--suffix "Please list any EnvO biomes that have not been mapped to any MIxS environment. Provide both the id and the label. Do not provide any introduction, commentary, summary or anything like that." > $@

assets/environments_with_no_biome_mappings.raw.txt: assets/misc_llm_input/extension_report.yaml assets/misc_llm_input/report_envo_biome_annotations.yaml assets/misc_llm_mappings/biome_subsets_accepted.yaml
	date && time $(RUN) mixs-environments-to-envo-classes-by-claude \
		--mixs-file $(word 1,$^) \
		--envo-file $(word 2,$^) \
		--mappings-file $(word 3,$^) \
		--envo-description biomes \
		--temperature 0.1 \
		--max-tokens 4096 \
		--model claude-3-opus-20240229 \
		--suffix "Please list any MIxS environments to which no EnvO biomes have been mapped. Do not provide any introduction, commentary, summary or anything like that." > $@

assets/material_environment_built_environment_mappings_raw.yaml.txt: assets/misc_llm_input/extension_report.yaml \
assets/misc_llm_input/report_envo_biome_annotations.yaml \
assets/misc_llm_mappings/materials_subsets_accepted.yaml
	date && time $(RUN) mixs-environments-to-envo-classes-by-claude \
		--mixs-file $(word 1,$^) \
		--envo-file $(word 2,$^) \
		--mappings-file $(word 3,$^) \
		--envo-description "environmental materials" \
		--temperature 0.01 \
		--max-tokens 4096 \
		--model claude-3-opus-20240229 \
		--suffix "Please generate an exhaustive mapping of environmental materials to the BuiltEnvironment MIxS environment, using the same YAML format. Do not provide any introduction, commentary, summary or anything like that." > $@

#		--suffix "Please generate an exhaustive mapping of environmental materials to the MIxS environments that they could reasonably be found in, using the same YAML format. Do not provide any introduction, commentary, summary or anything like that. Do not perform mappings for any environmental materials or environments that are related to food, humans, hosts, or health." > $@

# Please do not repeat any of completed mappings.
# Please do not map any {envo_classes_description} to ENVO_00000428 'biome'.

local/biomes.ttl: downloads/envo.owl
	robot extract --method STAR \
		--input $< \
		--term "ENVO:00000428" \
		--output $@

downloads/mixs.yaml:
	curl --request GET -sL \
	     --url 'https://raw.githubusercontent.com/GenomicsStandardsConsortium/mixs/main/src/mixs/schema/mixs.yaml'\
	     --output $@

local/mixs-schemasheets-template.tsv: downloads/mixs.yaml # first four lines are headers
	$(RUN) linkml2schemasheets-template \
		--source-path $< \
		--output-path $@ \
		 --debug-report-path local/mixs-schemasheets-template-debug.txt \
		 --log-file local/mixs-schemasheets-template-log.txt \
		 --report-style concise
	head -n 4 $@ > $@.headers.tsv

local/mixs-extensions-schemasheets-template.tsv: local/mixs-schemasheets-template.tsv
	cat $< | python nmdc_ontology/schemasheets-template-mixs-extensions-filter.py  > $@

local/mixs-extensions-schemasheets-template.csv: local/mixs-extensions-schemasheets-template.tsv
	$(RUN) in2csv --format csv --tabs $< > $@

#local/envo_subset_non_host_env_local_scale.ttl: downloads/envo.owl local/envo_subset_non_host_env_local_scale_term_list.txt # 12.4 k T
#	robot extract --method BOT \
#		--input $(word 1,$^) \
#		--term-file $(word 2,$^) \
#		--output $@

assets/envo_subset_non_host_env_local_scale.tsv: downloads/envo.owl # slower than GraphDB
	robot query \
		--input $< \
		--query $(subst .tsv,.rq,$@) $@