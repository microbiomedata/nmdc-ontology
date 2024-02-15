RUN=poetry run

.PHONY: data-vs-ontology-all data-vs-ontology-clean


data-vs-ontology-all: data-vs-ontology-clean \
	data-vs-ontology-reports/envo-id-ranges-report.tsv \
	data-vs-ontology-reports/fma-usage-report.tsv

data-vs-ontology-clean:
	rm -rf data-vs-ontology-reports/*
	mkdir -p data-vs-ontology-reports
	touch data-vs-ontology-reports/.gitkeep
	rm -rf downloads/*owl*
	mkdir -p downloads
	touch downloads/.gitkeep

downloads/envo-idranges.owl.omn:
	@echo "Downloading..."
ifeq ($(shell command -v wget 2> /dev/null),)
	@echo "wget is not installed, trying with curl..."
	@curl -o $@ https://raw.githubusercontent.com/EnvironmentOntology/envo/master/src/envo/envo-idranges.owl
else
	@echo "Downloading with wget..."
	@wget -O $@ https://raw.githubusercontent.com/EnvironmentOntology/envo/master/src/envo/envo-idranges.owl
endif

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
		--counts-output $(subst counts.tsv,report-counts.tsv,$@)

data-vs-ontology-reports/fma-usage-report.tsv: data-vs-ontology-reports/biosample-triad-counts.tsv
	grep 'FMA:' $< > $@