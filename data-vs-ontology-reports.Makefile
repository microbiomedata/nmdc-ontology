RUN=poetry run

ENVO_SEMSQL=downlaods/envo.db

.PHONY: data-vs-ontology-all data-vs-ontology-clean


data-vs-ontology-all: data-vs-ontology-clean \
	data-vs-ontology-reports/envo-id-ranges-report.tsv \
	data-vs-ontology-reports/fma-usage-report.tsv \
	data-vs-ontology-reports/report-class-ids.tsv \
	data-vs-ontology-reports/report-id-ranges.tsv


data-vs-ontology-clean:
	rm -rf data-vs-ontology-reports/*
	mkdir -p data-vs-ontology-reports
	touch data-vs-ontology-reports/.gitkeep
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

data-vs-ontology-reports/report-class-ids.tsv: downloads/envo.owl
	robot query \
		--input $< \
		--query $(subst .tsv,.rq,$(subst data-vs-ontology-reports,data-vs-ontology-sparql,$@)) $@

# requires a newer version of relation-graph from the rest of this repo?! Like 2+
# sbt is required for building relation-graph
# requires sqlite. ubuntu calls sqlite3 sqlite3 and an alisa/link is required
# requires robot
# building rdftab.rs requires rustup
downloads/envo.db: downloads/envo.owl
	@echo "Converting..."
	cd $(dir $@) ; $(RUN) semsql make $(notdir $@)


downloads/envo-idranges.owl.omn:
	@echo "Downloading..."
ifeq ($(shell command -v wget 2> /dev/null),)
	@echo "wget is not installed, trying with curl..."
	@curl -o $@ https://raw.githubusercontent.com/EnvironmentOntology/envo/master/src/envo/envo-idranges.owl
else
	@echo "Downloading with wget..."
	@wget -O $@ https://raw.githubusercontent.com/EnvironmentOntology/envo/master/src/envo/envo-idranges.owl
endif

data-vs-ontology-reports/report-id-ranges.tsv: downloads/envo-idranges.owl.omn
	@echo "Querying..."
	robot query \
		--input $< \
		--query $(subst .tsv,.rq,$(subst data-vs-ontology-reports,data-vs-ontology-sparql,$@)) $@

downloads/envo-idranges.owl.ttl: downloads/envo-idranges.owl.omn
	@echo "Converting..."
	@robot convert --input $< --output $@

data-vs-ontology-reports/envo-id-ranges-report.tsv: downloads/envo-idranges.owl.ttl
	@echo "Generating report..."
	$(RUN) report-id-ranges \
		--id-ranges-ttl $< \
		--output $@

data-vs-ontology-reports/biosample-triad-counts.tsv:
	@echo "Generating report..."
	$(RUN) report-instantiated-traids \
		--output $@ \
		--counts-output $(subst counts.tsv,report.tsv,$@)

data-vs-ontology-reports/fma-usage-report.tsv: data-vs-ontology-reports/biosample-triad-counts.tsv
	grep 'FMA:' $< > $@