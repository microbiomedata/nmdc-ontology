RUN=poetry run

ENVO_SEMSQL=downlaods/envo.db

.PHONY: qc-all qc-clean


qc-all: qc-clean \
	qc-reports \
	downloads/envo.db \
	qc-reports \
	qc-reports \
	qc-reports \
	qc-reports \
	qc-reports

qc-clean:
	rm -rf qc-reports/*
	mkdir -p qc-reports
	touch qc-reports/.gitkeep
	rm -rf downloads/*owl* downloads/*.db
	mkdir -p downloads
	touch downloads/.gitkeep

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

assets/parse_robot_diff.tsv: assets/robot_diff.txt
	$(RUN) python nmdc_ontology/parse_robot_diff.py \
		--input $< \
		--output $@

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

.PHONY: envo_mixs_all
envo_mixs_all: envo_mixs_clean assets/mixs_environments_env_materials_subsets.yaml.txt

.PHONY: envo_mixs_clean
envo_mixs_clean: # todo update
	rm -rf assets/extension_report.yaml \
		assets/report_envo_environmental_material_annotations.tsv \
		assets/mixs_environments_env_materials_subsets.yaml.txt

assets/extension_report.yaml:
	$(RUN) python nmdc_ontology/report_mixs_extensions.py

assets/report_envo_biome_annotations.yaml:
	$(RUN) python nmdc_ontology/report_envo_biome_annotations.py

assets/report_envo_environmental_material_annotations.yaml:
	$(RUN) python nmdc_ontology/report_envo_environmental_material_annotations.py

assets/environments_with_no_biome_mappings.raw.yaml.txt: assets/extension_report.yaml assets/report_envo_biome_annotations.yaml assets/biome_subsets_accepted.yaml
	date && time $(RUN) python nmdc_ontology/mixs_environments_to_envo_classes_by_claude.py \
		--mixs-file $(word 1,$^) \
		--envo-file $(word 2,$^) \
		--mappings-file $(word 3,$^) \
		--envo-description biomes \
		--temperature 0.1 \
		--max-tokens 4096 \
		--model claude-3-opus-20240229 \
		--suffix "Please list any EnvO biomes that have not been mapped to any MIxS environment. Provide both the id and the label. Do not provide any introduction, commentary, summary or anything like that." > $@

assets/environments_with_no_biome_mappings.raw.txt: assets/extension_report.yaml assets/report_envo_biome_annotations.yaml assets/biome_subsets_accepted.yaml
	date && time $(RUN) python nmdc_ontology/mixs_environments_to_envo_classes_by_claude.py \
		--mixs-file $(word 1,$^) \
		--envo-file $(word 2,$^) \
		--mappings-file $(word 3,$^) \
		--envo-description biomes \
		--temperature 0.1 \
		--max-tokens 4096 \
		--model claude-3-opus-20240229 \
		--suffix "Please list any MIxS environments to which no EnvO biomes have been mapped. Do not provide any introduction, commentary, summary or anything like that." > $@

assets/material_environment_built_environment_mappings_raw.yaml.txt: assets/extension_report.yaml \
assets/report_envo_biome_annotations.yaml \
assets/materials_subsets_accepted.yaml
	date && time $(RUN) python nmdc_ontology/mixs_environments_to_envo_classes_by_claude.py \
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
