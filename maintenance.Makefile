RUN=poetry run

local/envo-idranges.owl.omn:
	@echo "Downloading..."
ifeq ($(shell command -v wget 2> /dev/null),)
	@echo "wget is not installed, trying with curl..."
	@curl -o $@ https://raw.githubusercontent.com/EnvironmentOntology/envo/master/src/envo/envo-idranges.owl
else
	@echo "Downloading with wget..."
	@wget -O $@ https://raw.githubusercontent.com/EnvironmentOntology/envo/master/src/envo/envo-idranges.owl
endif

local/envo-idranges.owl.ttl: local/envo-idranges.owl.omn
	@echo "Converting..."
	@robot convert --input $< --output $@

envo_id_ranges_report.tsv: local/envo-idranges.owl.ttl
	@echo "Generating report..."
	$(RUN) report-id-ranges \
		--id-ranges-ttl $< \
		--output $@