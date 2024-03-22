The MIxS standard says that [Biosamples](https://microbiomedata.github.io/nmdc-schema/Biosample/)
should be annotated with their [env_broad_scale](https://genomicsstandardsconsortium.github.io/mixs/0000012/),
[env_local_scale](https://genomicsstandardsconsortium.github.io/mixs/0000013/)
and [env_medium](https://genomicsstandardsconsortium.github.io/mixs/0000014/),
so we ask for users to fill those columns out in our SubmissionPortal.

The expected value is some reasonable class from a reasonable ontology,
in the format `term label [term id]` like "agricultural soil
[[ENVO:00002259](https://www.ebi.ac.uk/ols4/ontologies/envo/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FENVO_00002259)]".
EnvO provides pretty clear guidance on which parent classes provide reasonable subclasses
for `env_broad_scale` and `env_medium`.

However, those are general guidelines
and don't take into consideration that MIxS has a concept of samples coming from
[nameable environments](https://genomicsstandardsconsortium.github.io/mixs/#extensions).
(When people talk about MIxS environments, they sometimes use the terms "packages", "extensions" or "checklists").

In order to improve data consistency and simplify the data entry process,
we want to make subsets of reasonable ontology classes for `env_broad_scale` and `env_medium`
in the context of several of the MIxS environments.
Various NMDC people have been working on this for a few years.
I want to automate the process of bootstrapping these subsets and have set up a pipeline with Claude,
because it has the large context window and I'm more familiar with it that other LLMs now.
I think EnvO will provide all of the classes we need for the Soil and Water environments,
but we will probably need to use Uberon for HostAssociated and the Plant Ontology for PlantAssociated.

My goals are to generate exhaustive subsets (covering as many applicable EnvO terms as possible)
with the absolute minimal hallucination.
I would like for the implementation to

- Use a BBOP approved LLM and wrapper application if possible
- Avoid bad assumptions I have made about LLMs in previous tasks Harry, Sujay and I have discussed
- Improve abstraction to minimize repetitive scripts and makefile targets
- Not cost me personal money or be wasteful of BBOP money. Using Claude was my decision. I had hoped to get exhaustive
  mappings over all EnvO classes and all MIxS Environments for either of `env_broad_scale` or `env_medium` in a single
  conversation, but that's not working, so I am breaking the task into smaller parts and submitting the same large
  context multiple times. That is getting expensive.

- I have half-heartedly tried this task in NotebookLM, but it's results are anything but exhaustive. I have also tried
  asking Claude without providing the definitions of the MIxS and EnvO terms (trusting it was already trained with them)
  but that leads to lots of hallucination.

Harry (and Chris?) are skeptical of whether a LLM is the right tool.

Here is a post from Nico to Sujay regarding a somewhat related mapping between NMDC Biosample slots and fields from
NCBI, GOLD, etc.

From [#chat-gpt-n-llms on obo-community slack](https://obo-communitygroup.slack.com/archives/C050178F14P/p1710499635984109?thread_ts=1710459944.590769&cid=C050178F14P)

> Interesting subject. You are aware of the new “validate mappings” method in oak and the implementation we used in
> ontogpt for the mappergpt paper?
>
> Many workflows are best implemented like this:

- provide an overestimation mapping with a lexical matcher
- Use LLMs to review the corresponding mappings
- Use cardinality constraints and other techniques to further clean the resulting mapping
- Manually review

> Generally, remember to try and use SSSOM as much as possible for your mapping representations, which allows us to use
> a common interface for the various tools you need to leverage to achieve what you want.
>
> I am certainly interested in participating in any discussions towards this!

Here are the
[current makefile targets](https://github.com/microbiomedata/nmdc-ontology/blob/8f4785956d9df940d1470e6992b9f2dcfc113fe5/qc.Makefile#L160-L193)

Here's my understanding of the prioritization of the MIxS environments:

## Highest priority. Just use EnvO.

- Soil
- Water

## Medium priority.

- Air
- BuiltEnvironment
- MicrobialMatBiofilm
- MiscellaneousNaturalOrArtificialEnvironment
- Sediment

### Will require additional source ontologies

- HostAssociated... use uberon?
- PlantAssociated... use plant ontology?

### Hydrocarbons-related

- HydrocarbonResourcesCores
- HydrocarbonResourcesFluidsSwabs

## Lower priority Human-related

- HumanAssociated
- HumanGut
- HumanOral
- HumanSkin
- HumanVaginal

## Lowest priority

### Food-related

- FoodAnimalAndAnimalFeed
- FoodFarmEnvironment
- FoodFoodProductionFacility
- FoodHumanFoods

### Others

- Agriculture
- SymbiontAssociated
- WastewaterSludge

![Screenshot from 2024-03-22 10-56-05.png](Screenshot%20from%202024-03-22%2010-56-05.png)