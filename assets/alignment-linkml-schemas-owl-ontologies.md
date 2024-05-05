This may not be the best long term home for this document. I have also been using `llm` in the `main` branch
of `berkeley-schema-fy24`

See also `mapping_problem_statement.md` in this repo

And

- https://artificialanalysis.ai/
- https://llm.datasette.io/en/stable/
- https://llm.datasette.io/en/stable/plugins/directory.html#plugin-directory
- https://www.futurepedia.io/

## Ways to use LLMs

- web interface
- programmatically, esp Python
- `llm` CLI (or in Python)
    - prompt mode
    - chat mode

## Goals

- large input context
    - What are the densest formats for providing context to LLMs?
    - How can they be introduced through the different interfaces?
    - Some (esp web interfaces) may accept JSON, YAML and CSV but not TSV.
    - Tabular formats introduce a lot of delimiter characters but no repeated field names.
- high precision and high recall
    - how good does our training data have to be
- comprehensive output, either in a single large response or in a series of responses with minimal resubmission of input
  context
- emission in a constrained format, according to a LinkML schema (which therefore has to be part of the input)

Not prioritizing speed. Haven't been prioritizing cost but should start monitoring that more carefully.

## globally exporting environment variables like API keys

Loading from a `.env` file

```shell
set -a  # This ensures all variables defined from now on are exported automatically
source local/.env
set +a  # Turn off auto-export
```

Example of loading keys into `llm`

```shell
llm keys set openai
```

`llm` saves keys in `~/.config/io.datasette.llm/keys.json` by default

```shell
llm keys path
```

But models have to be installed on a project-by-project basis. See more below.

```shell
llm models list
```

### Here are the plugins for models that perform well on these tasks

* `llm-claude-3` supports Anthropic’s Claude 3 family of models.
* `llm-gemini` adds support for Google’s Gemini models.

```shell
llm install llm-claude-3
```

```shell
llm keys set llm-claude-3
```

```shell
llm install llm-gemini
```

```shell
llm keys set llm-gemini
```

### Here are some recommended models

Costs are in USD per million tokens

| vendor      | model                                                                            | aliases                  | quality_index | cost_input | cost_output | max_input_tokens_k |                                                      | notes                    |
|-------------|----------------------------------------------------------------------------------|--------------------------|---------------|------------|-------------|--------------------|------------------------------------------------------|--------------------------|
| OpenAI Chat | [gpt-4-turbo-preview](https://artificialanalysis.ai/models/gpt-4-turbo)          | gpt-4-turbo, 4-turbo, 4t | 100           | 10         | 30          | 128                |                                                      | doesn’t require a plugin |
| Google      | [gemini-1.5-pro-latest](https://artificialanalysis.ai/models/gemini-1-5-pro)     |                          | 88            | 7          | 21          | 1000               |                                                      |                          |
| Anthropic   | [claude-3-opus-20240229](https://artificialanalysis.ai/models/claude-3-opus)     | claude-3-opus            | 100           | 15         | 75          | 200                |                                                      |                          |
| Anthropic   | [claude-3-sonnet-20240229](https://artificialanalysis.ai/models/claude-3-sonnet) | claude-3-sonnet          | 85            | 3          | 15          | 200                |                                                      |                          |
| Anthropic   | [claude-3-haiku-20240307](https://artificialanalysis.ai/models/claude-3-haiku)   | claude-3-haiku           | 78            | 0.25       | 1.25        | 200                |                                                      |                          |

## Examples of interleaving strings and files for `llm prompt`

```shell
{
  echo -e "\n Here is a CSV report of biomes according to the environment ontology, EnvO. \n" ;
  cat assets/biome-class-annotations.csv ;
  echo -e "\n Here is a CSV report of environmental extensions according to MIxS. \n";
  cat local/mixs-extensions-schemasheets-template.csv ;
  echo -e "\n Here is a YAML-serialized LinkML schema that specifies how EnvO biomes can be mapped to MIxS environmental extensions. \n" ;
  cat assets/mixs_context_subsets_schema.yaml ;
  echo -e "\n Here is a YAML-serialized data file with examples of records that follow the schema. \n" ;
  cat assets/mixs_context_subsets_example.yaml ;
  echo -e "Based on the information I have provided, generate the most exhaustive possible mapping of EnvO biomes where the mixs_environment_label is Soil and the mixs_context_label is env_broad_scale." ;
  echo -e "You must follow the schema exactly." ;
  echo -e "If you have mapped term X and X appears in the superclasses column for biome Y, then you don't need to map biome Y.  I will add them programmatically later." ;
  echo -e "Don't bother reporting unacceptable mappings. I just included some to help train you." ;
  echo -e "Don't bother reporting that your mappings have an accepted value of true. I will take that for granted." ;
  echo -e "Don't emit any introduction, commentary or summary outside the YAML format. You can add a comment at any level in the YAML file " ;
} > soil-biome-prompt.txt
```

```shell
cat soil-biome-prompt.txt | llm -m gemini-1.5-pro-latest > soil-biome-results.yaml
```

## `llm chat` hints

- Type `!multi` to enter multiple lines, then `!end` to finish
- resume crashed chats with `llm chat --continue`
    - does this resubmit the whole prior context?
    - does each round of chatting?!

## Google Gemini directly through the Vertex API

Requires installing a client app. Once it is installed, a list of project codes can be retrieved with

```shell
gcloud projects list
```

----

## SPARQL query for extracting class annotations

For use in input contexts

### esp EnvO

First determine what properties should be included in the query

```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
select
?p ?plslug (count(?s) as ?count)
where {
    values ?root {
        obo:ENVO_00000428
        obo:ENVO_00010483
    }
    ?s rdfs:subClassOf* ?root ;
    ?p ?o .
    ?p a owl:AnnotationProperty
    optional {
        ?p rdfs:label ?pl .
        bind(lcase(replace(?pl," ", "_")) as ?plslug)
    }
}
group by ?p ?plslug
```

Then build the query

```sparql
# biome obo:ENVO_00000428
# environmental material obo:ENVO_00010483
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>
select
?class ?alternative_term ?comment ?definition ?editor_note ?has_broad_synonym ?has_exact_synonym ?has_narrow_synonym ?has_related_synonym ?hasSynonym ?in_subset ?label (GROUP_CONCAT(distinct ?super_slug;
SEPARATOR=", ") AS ?superclasses)
where {
    ?s rdfs:subClassOf+ obo:ENVO_00010483 .
    minus {
        ?s rdfs:subClassOf* obo:FOODON_00002403
    }
    bind(replace(str(?s), "http://purl.obolibrary.org/obo/", "") as ?class)
    optional {
        ?s rdfs:subClassOf ?superclass .
        filter(isiri(?superclass) = true)
        bind(replace(str(?superclass), "http://purl.obolibrary.org/obo/", "") as ?super_slug)
    }
    optional {
        ?s obo:IAO_0000115 ?definition .
    }
    optional {
        ?s obo:IAO_0000116 ?editor_note .
    }
    optional {
        ?s obo:IAO_0000118 ?alternative_term .
    }
    optional {
        ?s oboInOwl:hasExactSynonym ?has_exact_synonym .
    }
    optional {
        ?s oboInOwl:hasBroadSynonym ?has_broad_synonym .
    }
    optional {
        ?s oboInOwl:hasNarrowSynonym ?has_narrow_synonym .
    }
    optional {
        ?s oboInOwl:hasRelatedSynonym ?has_related_synonym .
    }
    optional {
        ?s oboInOwl:hasSynonym ?hasSynonym .
    }
    optional {
        ?s oboInOwl:inSubset ?in_subset .
    }
    optional {
        ?s rdfs:comment ?comment .
    }
    optional {
        ?s rdfs:label ?label .
    }
}
group by ?class ?alternative_term ?comment ?definition ?editor_note ?has_broad_synonym ?has_exact_synonym ?has_narrow_synonym ?has_related_synonym ?hasSynonym ?in_subset ?label
```

Sometimes the CSV downloads from the GraphDB web interface behave better than their TSV downloads.

## Subsetting LinkML schemas

```makefile
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
	$(RUN) in2csv --format csv --tabs $< > $@ # from csvtoolkit
```

### don't forget to ask about unmappeds


## Examples of asking the LLM to keep a categorized status report
### env_broad_scale from gemini 1.5 pro on the morning of 2024-05-02
* Completed:
  * BuiltEnvironment
  * HydrocarbonResourcesCores
  * HydrocarbonResourcesFluidsSwabs
  * MicrobialMatBiofilm
  * MiscellaneousNaturalOrArtificialEnvironment
  * PlantAssociated
  * Sediment
  * Soil
  * Water
* Completed despite absence of template:
  * Agriculture
* Skipped not advertised:
  * FoodAnimalAndAnimalFeed
  * FoodFarmEnvironment
  * FoodFoodProductionFacility
  * FoodHumanFoods
  * Skipped pending template:
* HumanAssociated
  * HumanGut
  * HumanOral
  * HumanSkin
  * HumanVaginal
  * Unfulfilled:
  * Air
  * HostAssociated

### env_medium from gemini 1.5 pro on the morning of 2024-05-02
* Completed:
  * Air
  * BuiltEnvironment
  * HostAssociated
  * HydrocarbonResourcesCores
  * HydrocarbonResourcesFluidsSwabs
  * MicrobialMatBiofilm
  * MiscellaneousNaturalOrArtificialEnvironment
  * PlantAssociated
  * Sediment
  * Soil
  * Water
* Completed despite absence of template:
  * Agriculture
* Pending:
  * None
* Skipped not advertised:
  * FoodAnimalAndAnimalFeed
  * FoodFarmEnvironment
  * FoodFoodProductionFacility
  * FoodHumanFoods
* Skipped pending template:
  * HumanAssociated
  * HumanGut
  * HumanOral
  * HumanSkin
  * HumanVaginal
* Unfulfilled:
  * None

----

## Pre-subsetting for non-host-associated env_local_scale values

### Exclude
* occurrent BFO:0000003 (~553 processes, ~11 temporal regions)
* generically dependent continuant BFO:0000031 (~13 ICEs)
* specifically dependent continuant BFO:0000020 (~716 BFO qualities, PATO qualities and realizable entities 

which basically leaves independent continuant BFO:0000004
  
### limited applicability
* anatomical entity UBERON:0001062
* immaterial entity BFO:0000141
  * continuant fiat boundary BFO:0000140
  * site BFO:0000029
    * except MAYBE for cave entrance ENVO:00000102, shoreline ENVO:00000486 and two dimensional flat water ice surface ENVO:01001545
  * spatial region BFO:0000006

which basically leaves material entity BFO:0000040

### Keep 
* astronomical body part ENVO:01000813
* construction ENVO:01001813
* fiat object BFO:0000024
* layer ENVO:01000281
* manufactured product ENVO:00003074
* system RO:0002577

### limited cases
* material anatomical entity UBERON:0000465


----

## Extract *noisy* examples from the relational biosample database

Could be more rough input for the kinds of vales that we should be able to support

* Requires a NERSC account
* Obtaining and using NERSC's sshproxy tool makes it possible to do multiple NERSC logins in a given day, without typing
  in the password + MFA code each time

see https://docs.nersc.gov/connect/mfa/#sshproxy

### Do this once for each computer that you use. You will have to enter your NERSC password + MFA code.

```shell
scp <NERSC_USERNAME>@dtn01.nersc.gov:/global/cfs/cdirs/mfa/NERSC-MFA/sshproxy.sh .
```

### Do this once per day (on each computer that you use)

```shell
./sshproxy.sh -u <NERSC_USERNAME>
```

### Do this to establish a tunnel to the relational biosample database

```shell
ssh -i ~/.ssh/nersc -L 15432:biosample-postgres-loadbalancer.mam.production.svc.spin.nersc.org:5432 <NERSC_USERNAME>@dtn01.nersc.gov
```

### Here's the connection string

Ask Mark, Sujay or Eric for the password

```sql
postgres
://biosample_guest:<PASSWORD>@localhost:15432/ncbi_biosamples_feb26
```

Here are some [NCBI Biosample packages](https://www.ncbi.nlm.nih.gov/biosample/docs/packages/) that are common for our
samples

* MIMS.me.soil.6.0
* MIMS.me.water.6.0

```sql
select package,
       env_broad_scale,
       sum(sample_count)
from triads_per_package_mv tppm
where package = 'MIMS.me.soil.6.0'
group by package,
         env_broad_scale
having sum(sample_count) > 499
order by sum(sample_count) desc
;
```

You probably wouldn't want to apply such a high (or even any) `having` constraint in production

| package          | env_broad_scale                                                          |  sum |
|------------------|--------------------------------------------------------------------------|-----:|
| MIMS.me.soil.6.0 | missing                                                                  | 8599 |
| MIMS.me.soil.6.0 | not applicable                                                           | 3331 |
| MIMS.me.soil.6.0 | not collected                                                            | 2887 |
| MIMS.me.soil.6.0 | forest biome                                                             | 2656 |
| MIMS.me.soil.6.0 | soil                                                                     | 2512 |
| MIMS.me.soil.6.0 | forest                                                                   | 1736 |
| MIMS.me.soil.6.0 | Agricultural soil                                                        | 1684 |
| MIMS.me.soil.6.0 | ENVO:01000198                                                            | 1562 |
| MIMS.me.soil.6.0 | temperate desert biome                                                   | 1505 |
| MIMS.me.soil.6.0 | agricultural field                                                       | 1468 |
| MIMS.me.soil.6.0 | eroded soil                                                              | 1426 |
| MIMS.me.soil.6.0 | [ENVO:00000428]                                                          | 1372 |
| MIMS.me.soil.6.0 | temperate grassland                                                      | 1362 |
| MIMS.me.soil.6.0 | temperate forest                                                         | 1279 |
| MIMS.me.soil.6.0 | desert grassland/shrubland                                               | 1215 |
| MIMS.me.soil.6.0 | ENVO:00000446                                                            | 1183 |
| MIMS.me.soil.6.0 | permafrost                                                               | 1055 |
| MIMS.me.soil.6.0 | ENVO_01000180                                                            | 1022 |
| MIMS.me.soil.6.0 | boreal forest biome                                                      | 1014 |
| MIMS.me.soil.6.0 | grassland biome                                                          |  999 |
| MIMS.me.soil.6.0 | Agricultural field                                                       |  974 |
| MIMS.me.soil.6.0 | woodland area[ENVO:00000109]                                             |  944 |
| MIMS.me.soil.6.0 | anthropogenic terrestrial biome [ENVO:01000219]                          |  881 |
| MIMS.me.soil.6.0 | farmland                                                                 |  812 |
| MIMS.me.soil.6.0 | ENVO:00001998                                                            |  741 |
| MIMS.me.soil.6.0 | soil biome                                                               |  739 |
| MIMS.me.soil.6.0 | ENVO:01000245                                                            |  709 |
| MIMS.me.soil.6.0 | apple root microbiome                                                    |  648 |
| MIMS.me.soil.6.0 | Coal mine                                                                |  646 |
| MIMS.me.soil.6.0 | temperate dry conifer forest biome                                       |  645 |
| MIMS.me.soil.6.0 | dryland                                                                  |  627 |
| MIMS.me.soil.6.0 | soil ecosystem                                                           |  564 |
| MIMS.me.soil.6.0 | ENVO:01000206                                                            |  563 |
| MIMS.me.soil.6.0 | temperate deciduous forest biome [ENV 01000385]                          |  555 |
| MIMS.me.soil.6.0 | Temperate biome [ENVO: 01001831]temperate woodland biome [ENVO:01000221] |  537 |
| MIMS.me.soil.6.0 | Agricultural Field                                                       |  507 |

### What does ChatGPT 4 think of that?
Even without having been supplied with explicit EnvO biome knowledge?

### Analysis of env\_broad\_scale Values in NCBI Biosamples for MIMS.me.soil.6.0 Package

The provided data shows the distribution of `env_broad_scale` values used in NCBI Biosamples submitted against the MIMS.me.soil.6.0 package. This package appears to be related to soil environments and the associated microbiome.

**Key Observations:**

* **Missing Values:** A significant portion of submissions (8599) have missing values for `env_broad_scale`. This indicates a lack of information about the broader environmental context for these samples, which could limit the analysis and interpretation of the data.
* **Generic Terms:** The most frequent terms, after missing values, are generic terms like "not applicable" (3331), "not collected" (2887), "soil" (2512), and "forest" (1736). These terms provide limited ecological context.
* **ENVO Terms:** Several submissions use ENVO (Environment Ontology) terms to describe the environment, such as "ENVO:01000198" (mixed forest biome), "ENVO:00000428" (terrestrial biome), and "ENVO:00000446" (land biome). This provides a more standardized and controlled vocabulary for describing the environment.
* **Specific Biomes:** A variety of specific biomes are represented, including forest biomes (e.g., temperate forest, boreal forest), grassland biomes, desert biomes, tundra, and agricultural land.  This suggests a wide range of soil environments have been sampled.
* **Agricultural Environments:** A substantial number of samples come from agricultural contexts, with terms like "Agricultural soil" (1684), "agricultural field" (1468), and "farmland" (812) appearing frequently. This highlights the importance of understanding soil microbial communities in agricultural systems. 
* **Other Environments:**  The data also includes less frequent but noteworthy terms like "permafrost", "wetland", "rhizosphere", "compost", and "cave". These terms point to the diversity of soil environments represented in the dataset. 

**Recommendations:**

* **Standardization:** Encourage the use of controlled vocabularies like ENVO for `env_broad_scale` to improve data consistency and facilitate comparisons across studies.
* **Completeness:**  Promote efforts to provide complete environmental information for Biosample submissions, reducing the number of missing values.
* **Specificity:** When possible, use more specific terms to describe the environment beyond generic terms like "soil" or "forest". This will provide a more accurate and informative representation of the ecological context.

**Additional Considerations:**

*  Explore the use of additional environmental descriptors beyond `env_broad_scale`, such as `env_local_scale` and `env_medium`, to capture more detailed information about the sampling locations.
* Investigate the potential biases in the data, such as overrepresentation of certain biomes or environments.
* Utilize the environmental information to analyze and interpret the microbial community data in the context of ecological factors. 

By addressing the missing values and encouraging the use of standardized and specific environmental descriptors, the value and usability of the data in NCBI Biosamples can be greatly enhanced for researchers studying soil microbial ecology.

# Then I asked
> please give a complete list of values in this dataset that could be considered indicators of missing data

### Indicators of Missing Data in the env\_broad\_scale Dataset

Based on the provided data, here's a list of values that could indicate missing data for the `env_broad_scale` field:

* **Explicit Mentions:**
    * missing
    * not applicable 
    * not collected
    * unkown (misspelling of "unknown")
    * Missing (capitalized)
    * missing: control sample
* **Ambiguous or Uninformative Terms:**
    * NA 
    * ?plains  (question mark indicates uncertainty) 
    * Soil (capitalized, could imply a general category rather than specific environment)
    * pH (refers to a soil property, not broad-scale environment) 

**Justification:**

* The terms "missing," "not applicable," "not collected," and "unknown" directly indicate the absence of information about the broader environment. 
* "Missing" with capitalization could be a variant used inconsistently.
* "missing: control sample" suggests missing environmental data specifically for control samples. 
* "NA" and "?plains" represent uncertainty or lack of specific information.
* While "Soil" with capitalization could be a valid descriptor in certain controlled vocabularies, in this context, it appears as a general categorization rather than a specific environmental term.
* "pH" refers to a soil characteristic, not the broad-scale environment.

**Additional Notes:**

* The distinction between "not applicable" and "not collected" is unclear and might require further investigation into the data submission guidelines or context.
* The presence of generic terms like "soil" and "forest" could also indicate missing data if more specific information about the environment was available but not recorded.

It's important to consider these indicators of missing data when analyzing and interpreting the `env_broad_scale` information. Addressing these missing values and using more specific environmental descriptors will improve the quality and value of the data for ecological research. 


# Then I provided the EnvO biomes CSV file

## Matching env\_broad\_scale Values with ENVO Biomes

To match the `env_broad_scale` values with ENVO biomes, we need to consider several factors:

* **Exact Matches:** Some values may directly correspond to ENVO labels or synonyms.
* **Partial Matches and Synonyms:** We need to account for variations in wording, capitalization, and the use of synonyms.
* **Hierarchical Relationships:** ENVO has a hierarchical structure, so broader terms might encompass multiple specific biomes. 
* **Ambiguity and Missing Data:** Some values might be ambiguous or represent missing data, as identified previously.

Here's a possible approach:

**1. Create a Lookup Table:**

* Compile a list of ENVO biome labels, alternative terms, and synonyms from the provided data.
* This table will serve as a reference for matching `env_broad_scale` values.

**2. Matching Algorithm:**

1. **Preprocessing:**
    * Standardize the `env_broad_scale` values by converting them to lowercase and removing extra spaces.
    * Address misspellings and obvious typos (e.g., "unkown" to "unknown").
2. **Exact Matching:**
    * Check for exact matches between the standardized values and the ENVO labels/synonyms.
3. **Partial Matching:**
    * If no exact match is found, look for partial matches using string similarity measures (e.g., Levenshtein distance). 
    * Prioritize matches with higher similarity scores and consider the context of the values.
4. **Hierarchical Matching:**
    * If a specific biome cannot be identified, consider broader ENVO categories that might encompass the value (e.g., "terrestrial biome" for "land"). 
5. **Ambiguity and Missing Data:**
    * Flag values identified as potential indicators of missing data as "unidentified" or "missing."

**3. Implementation:**

This matching process can be implemented using various programming languages and tools for string manipulation and data matching.  For example, Python with libraries like `fuzzywuzzy` for fuzzy string matching could be utilized.

**4. Example Matches:**

| env\_broad\_scale Value       | Potential ENVO Biome Match                       |
|-------------------------------|--------------------------------------------------|
| temperate forest              | ENVO_01000202: temperate broadleaf forest biome   |
| Agricultural soil            | ENVO_01000245: cropland biome                   |
| ENVO:00000446                | ENVO_00000446: terrestrial biome                 |
| grassland biome               | ENVO_01000177: grassland biome                   |
| arctic                       | ENVO_01000339: polar biome (consider tundra biome) |
| missing                      | (flagged as missing data)                         |

**5. Challenges and Limitations:**

* Ambiguous terms with multiple possible matches (e.g., "forest" could be various forest biomes).
* Inconsistent use of terminology and spelling variations.
* The hierarchical nature of ENVO might require additional steps to determine the most appropriate level of specificity.

**6. Additional Recommendations:**

* **Validation:** Manually review a subset of the matches to ensure accuracy and identify potential issues.
* **Feedback Mechanism:** If possible, provide a way for users to report mismatches or suggest improvements to the matching algorithm.
* **Documentation:** Clearly document the matching process and any assumptions made to ensure transparency and reproducibility. 

> please give the most thorough mapping of the observed env_broad_scale values to EnvO terms, as you started to do above

See separate huge table in `assets/ncbio-biosample-ebs-suggestions.md` !

## Getting higher-quality NMDC annotations from a triple store

```sparql
PREFIX nmdc: <https://w3id.org/nmdc/>
PREFIX MIXS: <https://w3id.org/mixs/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX env_broad_scale: <https://w3id.org/mixs/0000012>
PREFIX env_local_scale: <https://w3id.org/mixs/0000013>
PREFIX env_medium: <https://w3id.org/mixs/0000014>
select
?context_predicate ?predicate_label ?term (str(?term_label_raw) as ?term_label) ?context_raw_value (count(?bs) as ?count)
where {
    values ?context_predicate {
        env_broad_scale:
    }
    graph <https://api.microbiomedata.org> {
        ?bs a nmdc:Biosample ;
        ?context_predicate ?context .
        ?context nmdc:term ?term .
        optional {
            ?context nmdc:has_raw_value ?context_raw_value
        }
    }
    optional {
        graph obo:nmdco.owl {
            ?term rdfs:label ?term_label_raw .
        }
    }
    optional {
        graph nmdc:nmdc-no-use-native-uris {
            ?context_predicate rdfs:label ?predicate_label .
        }
    }
}
group by ?context_predicate ?predicate_label ?term ?term_label_raw ?context_raw_value
order by desc(count(?bs))
```

| context_predicate | predicate_label | term          | term_label                        | context_raw_value                               | count |
|-------------------|-----------------|---------------|-----------------------------------|-------------------------------------------------|------:|
| MIXS:0000012      | env_broad_scale | ENVO:00000446 | terrestrial biome                 |                                                 |  4475 |
| MIXS:0000012      | env_broad_scale | ENVO:00000446 | terrestrial biome                 | ENVO:00000446                                   |   643 |
| MIXS:0000012      | env_broad_scale | ENVO:01000253 | freshwater river biome            |                                                 |   573 |
| MIXS:0000012      | env_broad_scale | ENVO:01000252 | freshwater lake biome             | ENVO_01000252                                   |   484 |
| MIXS:0000012      | env_broad_scale | ENVO:01000253 | freshwater river biome            | ENVO_01000253                                   |   417 |
| MIXS:0000012      | env_broad_scale | ENVO:00000446 | terrestrial biome                 | ENVO_00000446                                   |   416 |
| MIXS:0000012      | env_broad_scale | ENVO:01000174 | forest biome                      | ENVO:01000174                                   |   192 |
| MIXS:0000012      | env_broad_scale | ENVO:01001442 | agriculture@en                    | agricultural biome [ENVO:01001442]              |   192 |
| MIXS:0000012      | env_broad_scale | ENVO:03605008 | freshwater stream biome@en        |                                                 |   104 |
| MIXS:0000012      | env_broad_scale | ENVO:01001002 | animal-associated environment@en  | ENVO_01001002                                   |    95 |
| MIXS:0000012      | env_broad_scale | ENVO:01000252 | freshwater lake biome             |                                                 |    75 |
| MIXS:0000012      | env_broad_scale | ENVO:00000446 | terrestrial biome                 | terrestrial biome [ENVO:00000446]               |    72 |
| MIXS:0000012      | env_broad_scale | ENVO:01001002 | animal-associated environment@en  | Animal-associated environment [ENVO:01001002]   |    61 |
| MIXS:0000012      | env_broad_scale | ENVO:01000177 | grassland biome                   | grassland biome [ENVO:01000177]                 |    60 |
| MIXS:0000012      | env_broad_scale | ENVO:00000108 | meadow ecosystem                  | ENVO:00000108                                   |    53 |
| MIXS:0000012      | env_broad_scale | ENVO:01000253 | freshwater river biome            | ENVO:01000253                                   |    50 |
| MIXS:0000012      | env_broad_scale | ENVO:00000873 | freshwater biome                  | ENVO:00000873                                   |    38 |
| MIXS:0000012      | env_broad_scale | ENVO:01000250 | subpolar coniferous forest biome  | ENVO:01000250                                   |    31 |
| MIXS:0000012      | env_broad_scale | ENVO:01000221 | temperate woodland biome          | ENVO:01000221                                   |    19 |
| MIXS:0000012      | env_broad_scale | ENVO:01001837 | subalpine biome@en                | subalpine biome [ENVO:01001837]                 |    18 |
| MIXS:0000012      | env_broad_scale | ENVO:01000219 | anthropogenic terrestrial biome   | ENVO:01000219                                   |    12 |
| MIXS:0000012      | env_broad_scale | ENVO:01000219 | anthropogenic terrestrial biome   | anthropogenic terrestrial biome [ENVO:01000219] |    12 |
| MIXS:0000012      | env_broad_scale | ENVO:01000245 | cropland biome                    | ENVO:01000245                                   |     9 |
| MIXS:0000012      | env_broad_scale | ENVO:01000221 | temperate woodland biome          | __temperate woodland biome [ENVO:01000221]      |     8 |
| MIXS:0000012      | env_broad_scale | ENVO:01000249 | urban biome                       | urban biome [ENVO:01000249]                     |     8 |
| MIXS:0000012      | env_broad_scale | ENVO:01000249 | urban biome                       | ENVO:01000249                                   |     7 |
| MIXS:0000012      | env_broad_scale | ENVO:01000215 | temperate shrubland biome         | __temperate shrubland biome [ENVO:01000215]     |     6 |
| MIXS:0000012      | env_broad_scale | ENVO:01000216 | montane shrubland biome           | __montane shrubland biome [ENVO:01000216]       |     6 |
| MIXS:0000012      | env_broad_scale | ENVO:01000179 | desert biome                      | ENVO:01000179                                   |     6 |
| MIXS:0000012      | env_broad_scale | ENVO:01000189 | temperate savanna biome           | __temperate savanna biome [ENVO:01000189]       |     4 |
| MIXS:0000012      | env_broad_scale | ENVO:01000211 | temperate coniferous forest biome | ENVO:01000211                                   |     3 |
| MIXS:0000012      | env_broad_scale | ENVO:01000247 | rangeland biome                   | ENVO:01000247                                   |     3 |
| MIXS:0000012      | env_broad_scale | ENVO:01000247 | rangeland biome                   | __rangeland biome [ENVO:01000247]               |     2 |
| MIXS:0000012      | env_broad_scale | ENVO:01000183 | tropical desert biome             | ENVO:01000183                                   |     2 |
| MIXS:0000012      | env_broad_scale | ENVO:01000252 | freshwater lake biome             | ENVO:01000252                                   |     1 |
| MIXS:0000012      | env_broad_scale | ENVO:01000215 | temperate shrubland biome         | ENVO:01000215                                   |     1 |

There's probably some way to do that through the NMDC API and a little python cleanup code. I did some manual cleanup on
teh result above anyway.