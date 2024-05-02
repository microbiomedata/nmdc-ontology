## Mapping env\_broad\_scale Values to ENVO Biomes: A Comprehensive Attempt

Due to the complexity and potential ambiguity in the `env_broad_scale` values, a perfect and complete mapping to ENVO terms is challenging. However, I can provide the most thorough mapping possible based on the available information and considerations discussed previously. 

**Assumptions and Approach:**

* The provided ENVO biome list is used as the reference for matching.
* The matching algorithm described previously is conceptually applied, prioritizing exact matches, then partial matches, and finally considering broader ENVO categories.
* Ambiguous cases are noted, and potential alternative matches are suggested.
* Values identified as indicators of missing data are flagged as such.

**Mapping Results (Non-Exhaustive):** 

| env\_broad\_scale Value       | Potential ENVO Biome Match(es)                                      | Notes                                                         |
|-------------------------------|-----------------------------------------------------------------------|----------------------------------------------------------------|
| missing, not applicable, not collected, unkown, Missing, missing: control sample, NA, ?plains  | (flagged as missing data)                                               |                                                                |
| soil, Soil                   | ENVO_00001998: soil biome (broad category)                         | Consider more specific terms if available.                   |
| forest, Forest              | ENVO_01000174: forest biome (broad category)                          | Consider forest type (e.g., temperate, tropical, coniferous). | 
| forest biome, forest biome [ENVO:01000174]  | ENVO_01000174: forest biome                                         |                                                                |
| Agricultural soil, agricultural soil, agricultural soil [ENVO:00002259], Agriculture soil | ENVO_00002259: agricultural soil                               | Consider specific crop or land use if available.             |
| agricultural field, agricultural field, agricultural ecosystem [ENVO:00000077], argricultural field, agricultral fields | ENVO_00000077: agricultural ecosystem                          | Could also be ENVO_01000245: cropland biome.                 | 
| temperate desert biome        | ENVO_01000182: temperate desert biome                               |                                                                |
| [ENVO:00000428], ENVO:00000428, 00000428, biome [ENVO:00000428], subclasses of biome [ENVO:00000428], subbasses of biome [ENVO:000000428] | ENVO_00000428: terrestrial biome                              |                                                                |
| temperate grassland, temperate grassland biome, temperate grassland biome [ENVO:01000193], Temperate grasslands, Temperate grassland [ENVO:01000193] | ENVO_01000193: temperate grassland biome                        |                                                                |
| temperate forest, Temperate forest, Temperate_Forest, Temperate_forest | ENVO_01000202: temperate broadleaf forest biome (likely)         | Could also consider ENVO_01000211 (temperate coniferous) or ENVO_01000212 (temperate mixed forest) based on context. |
| desert grassland/shrubland  | ENVO_01000218: xeric shrubland biome (possible)                     | Could also consider ENVO_01000182 (temperate desert) or other desert/shrubland combinations. |
| ENVO:01000198                | ENVO_01000198: mixed forest biome                                |                                                                |
| permafrost, Permafrost       | (no exact match)                                                      | Consider ENVO_01001834 (subpolar biome) as permafrost is often found in these regions. |
| ENVO_01000180               | ENVO_01000180: tundra biome                                      |                                                                |
| boreal forest biome, Boreal forest, Boreal_forest | ENVO_01000250: subpolar coniferous forest biome                 |                                                                |
| grassland biome, grassland biome [ENVO:01000177], Grassland, Grassland biome, "Grassland biome, temperate biome" | ENVO_01000177: grassland biome                                |                                                                |
| woodland area[ENVO:00000109] | ENVO_00000109: woodland                                        |                                                                | 
| anthropogenic terrestrial biome [ENVO:01000219], anthropogenic terrestrial biome, anthropogenic | ENVO_01000219: anthropogenic terrestrial biome                 |                                                                |
| farmland, farmland biome    | (no exact match)                                                      | Consider ENVO_01000245 (cropland biome) or ENVO_01000247 (rangeland biome) depending on context. |
| ENVO:00001998, ENVO_00001998, ENVO_01001998, soil [ENVO:00001998], soil [ENVO:00001998] | ENVO_00001998: soil biome                                       |                                                                |
| soil biome, Soil biome      | ENVO_00001998: soil biome                                       |                                                                | 
| ENVO:01000245, cropland biome [ENVO:01000245], cropland (ENVO:01000245), cropland, croplandbiome[ENVO_01000245], Crop land, area of cropland [ENVO:01000892], area of cropland, crop | ENVO_01000245: cropland biome                                 | Consider specific crop or land use if available.             |
| apple root microbiome        | (no exact match)                                                      | Consider ENVO_01000999: rhizosphere environment and the biome of the apple orchard (e.g., temperate broadleaf forest). |
| Coal mine, Coal gangue      | (no exact match)                                                      | Consider broader categories like terrestrial biome or anthropogenic terrestrial biome. |
| temperate dry conifer forest biome | (no exact match)                                                      | Consider ENVO_01000211: temperate coniferous forest biome.   | 
| dryland, dryland biome, drylands, drylands, [ENVO:01001838]       | ENVO_01001838: arid biome                                        | Consider specific type of dryland (e.g., desert, steppe).    |
| soil ecosystem               | ENVO_00001998: soil biome                                       | Consider more specific terms if available.                   | 
| ENVO:01000206                | ENVO_01000206: temperate deciduous forest biome                   |                                                                |
| Temperate biome [ENVO: 01001831]temperate woodland biome [ENVO:01000221], temperate woodland, temperate woodland biome, Temperate Woodland biome, Temperate Woodland Biome | ENVO_01000221: temperate woodland biome                        |                                                                |
| Agricultural Field, Agricultural, agriculture, agriculture [01001442], agriculture [ENVO:01001442], AGRO-ECOSYSTEM, Agricultral Soil | ENVO_00000077: agricultural ecosystem                          | Could also be ENVO_01000245: cropland biome.                 | 
| pH                           | (refers to soil property, not biome)                             |                                                                |
| cropland biome, cropland biome [ENVO:01000245] | ENVO_01000245: cropland biome                                 |                                                                |
| village biome, village biome [ENVO:01000246], village              | ENVO_01000246: village biome                                    |                                                                | 
| agricultural soil           | ENVO_00002259: agricultural soil                               | Consider specific crop or land use if available.             |
| grassland, grassland area, grassland ecosystem [ENVO:01001206], Grass, grass, "dry grassland pastures, fungi", "dry grassland pastures, prokaryotes" | ENVO_01000177: grassland biome                                |                                                                |
| ENVO:01000193, Temperate grassland, temperate grassland biome  | ENVO_01000193: temperate grassland biome                        |                                                                |
| ENVO:00002259                | ENVO_00002259: agricultural soil                               | Consider specific crop or land use if available.             |
| arctic_soils, arctic, arctic biome, Arctic biome, Arctic          | ENVO_01000180: tundra biome                                      |                                                                |
| low managed grassland         | ENVO_01000177: grassland biome (likely)                           |  Could also consider ENVO_01000247: rangeland biome.           |
| Laboratory, laboratory, lab experiment   | (not a biome)                                                        | Consider the biome where the laboratory is located.         | 
| field, field soil, Field      | (ambiguous)                                                         | Consider the context to determine the specific biome.         |
| Boreal forest               | ENVO_01000250: subpolar coniferous forest biome                 |                                                                | 
| beech forest, Beech forest, beech forest soil | (no exact match)                                                      | Consider ENVO_01000202 (temperate broadleaf forest) or a more specific ENVO term for beech forests. |
| root biome, root, Root, rhizosphere soil, rhizosphere, rhizosphere environment [ENVO: 01000999], rhizosphere environment[ENVO01000999], rhizsophere, rhizoplane biome, Rhizosphere soil, Rhizosphere micriobiome, Rhizosphere microbiome, Rhizosphere-Agricole-Soil, Rhizosphere-Non-Agricole-Soil | ENVO_01000999: rhizosphere environment                        | Consider the biome and plant species for further specificity. |
| terrestrial biome [ENVO:00000446], terrestrial biome[ENVO:00000446], terrestrial biome, terrestrial, Terrestrial, Terrestrial [ENVO:00000446], Terrestria, terresterial biome, Tresstrial biome, ENVO:00000446 (terrestrial) | ENVO_00000446: terrestrial biome                              |                                                                |
| orchard biome, orchard, orcard | (no exact match)                                                      | Consider the biome of the orchard (e.g., temperate broadleaf forest) and the type of fruit tree. |
| tundra, tundra [ENVO:01000180], tundra biome [ENVO:01000180], alpine tundra [ENVO:01001505]  | ENVO_01000180: tundra biome                                      |                                                                | 
| ENVO_01000221, temperate woodland biome [ENVO:01000221], temperate woodland biome, Temperate Woodland biome, Temperate Woodland Biome  | ENVO_01000221: temperate woodland biome                        |                                                                |
| grassland area               | ENVO_01000177: grassland biome                                |                                                                |
| temperate broadleaf forest biome [ENVO: 01000202], temperate broadleaf forest, Temperate Broadleaf forest, temperate broadleaf  | ENVO_01000202: temperate broadleaf forest biome                   |                                                                |
| plateau biome                | (no exact match)                                                      | Consider the specific type of plateau and its vegetation.      |
| soil microbiome, Soil microbiome | ENVO_00001998: soil biome                                       | Consider more specific terms if available.                   |
| semi-arid soil, semiarid biome, Semiarid, Semi-arid region, semi-arid heathland, Semi-arid shrubland | ENVO_01001838: arid biome (likely)                                | Consider more specific terms like desert or steppe if possible. |
| soil mesocosm, soil mescosms  | (no exact match)                                                      | Consider the biome being modeled in the mesocosm.             | 
| rangeland, rangeland biome, Rangeland biome | ENVO_01000247: rangeland biome                                    |                                                                | 
| Soil [ENVO:00001998], soil [ENVO: 00001998], soil [ENVO:00001998] | ENVO_00001998: soil biome                                       |                                                                |
| agricultural land, agricultural land, Agricultural Land | ENVO_00000077: agricultural ecosystem                          | Could also be ENVO_01000245: cropland biome.                 |
| desert biome, desert biome [ENVO:01000179], desert, Desert, deserts | ENVO_01000179: desert biome                                     | Consider desert type (e.g., temperate, tropical) if possible.  |
| crop, crop, crop rotation, Crop, cropland, Cropland | ENVO_01000245: cropland biome                                 | Consider the specific crop or land use.                    |
| alpine biome, alpine biome [ENVO:01001835], Alpine, Alpine soil, alpine meadow, alpine meadow and alpine scrub, alpine meadow biome, alpine steppe, alpine grassland,  | ENVO_01001835: alpine biome                                     | Consider the specific type of alpine ecosystem if possible.   |
| mixed forest biome, mixed forest biome [ENVO:01000198], mixed forest | ENVO_01000198: mixed forest biome                                | Consider forest type (e.g., temperate, tropical) if possible. |
| paddy soil, paddy field, paddy field soil, paddy field soil [ENVO:00005740], paddy field near Sb mining area, paddy, Paddy, paddy soil biome, Rice paddy, Rice paddy soil, Rice paddy field, rice field [ENVO_00000296], rice field biome, rice microbiome, Rice, Rice ecosystem | (complex case)                                                      | Consider a combination of ENVO_00005740: paddy field soil and the broader biome (e.g., temperate grassland, tropical grassland). |
| wetland ecosystem(ENVO:01001209), wetland, Wetland, wetlands, wetlands, "wetlands, bacteria", "wetlands, fungi", wetland mofette soil, wetland reference soil, freshwater wetland, freshwater wetland soil, Forested Wetland, wetland ecosystem [ENVO01001209], Wetland [ENVO:00000043] | ENVO_01001209: wetland ecosystem                              | Consider wetland type (e.g., marsh, swamp, bog) if possible.   | 
| coniferous forest biome, coniferous forest, Conifer Forest, temperate coniferous forest biome [ENVO:01000211], subpolar coniferous forest biome [ENVO:01000250], subtropical coniferous forest biome, "coniferous forest biome, cold" | ENVO_01000196: coniferous forest biome                          | Consider the specific type of coniferous forest (e.g., temperate, boreal, subpolar). |
| tundra biome, tundra biome [ENVO:01000180] | ENVO_01000180: tundra biome                                      |                                                                |
| desert, Desert, deserts     | ENVO_01000179: desert biome                                     | Consider desert type (e.g., temperate, tropical) if possible.  |
| woodland, woodland area[ENVO:00000109], Woodland, Woodland biome, wood land biome, wooded land under tree, wooded land grass patch | ENVO_01000175: woodland biome                                    |                                                                |
| Upland Forest, Upland Grass/Shrubs | (ambiguous)                                                         | Consider the dominant vegetation type (forest or shrubland) and the broader biome. |
| cultivated environment [ENVO:01000311], Cultivatied, Cultivated soil  | ENVO_01000311: cultivated environment                         | Consider the specific type of cultivation (e.g., cropland, orchard). | 
| temperate woodland, temperate woodland biome, temperate woodland biome [ENVO:01000221], Temperate Woodland biome, Temperate Woodland Biome | ENVO_01000221: temperate woodland biome                        |                                                                |
| ENVO:00000260                | ENVO_00000260: mudflat                                         |                                                                | 
| mudflat[ENVO:00000192], mud flat | ENVO_00000192: mudflat                                         |                                                                |
| ENVO:01000197                | ENVO_01000197: broadleaf forest biome                          | Consider forest type (e.g., temperate, tropical) if possible. |
| fen, Fen Biome               | (no exact match)                                                      | Consider ENVO_01001209: wetland ecosystem and the specific type of fen. |
| corn, corn, Corn, Corn continuous cropping | (ambiguous)                                                         | Consider ENVO_01000245: cropland biome and the specific type of corn field. |
| area of gramanoid or herbaceous vegetation [ENVO:01000888] | ENVO_01000888: area of gramanoid or herbaceous vegetation       | Consider the broader biome where the vegetation is found.    |
| Soil incubated under flooded condition, flooded paddy soil | (complex case)                                                      | Consider a combination of ENVO_00005740: paddy field soil and the broader biome (e.g., temperate grassland, tropical grassland). |
| Secondary forest Biome, secondary forest, Secondaryforesty | (no exact match)                                                      | Consider the type of secondary forest and its successional stage. | 
| temperate, temperate regions   | ENVO_01001831: temperate biome                                    | Consider a more specific biome within the temperate zone.   | 
| Greenhouse, greenhouse, green house, green house soil | (not a biome)                                                        | Consider the biome being simulated or the plants grown in the greenhouse. |
| Compost, compost, compost biome, compost biome under annmonia exposure | (no exact match)                                                      | Consider ENVO_01000311: cultivated environment or ENVO_00001998: soil biome depending on context. | 
| paddy field soil [ENVO:00005740], Paddy soil, Paddy  | ENVO_00005740: paddy field soil                                | Consider the broader biome (e.g., temperate grassland, tropical grassland). |
| Mediterranean pine forest, meditteranean, Mediterranean, mediterranean, Mediterranean Biome | ENVO_01001833: mediterranean biome                             | Consider the specific type of mediterranean forest.          |
| temperate mixed forest biome   | ENVO_01000212: temperate mixed forest biome                       |                                                                | 
| Tropical grassland           | ENVO_01000192: tropical grassland biome                        |                                                                |
| Huang Huai Plain             | (geographic region, not biome)                                      | Consider the dominant biome in this region.                  |
| Taiga                         | ENVO_01000250: subpolar coniferous forest biome                 |                                                                |
| subboreal forest             | (no exact match)                                                      | Consider a more specific forest type within the boreal or temperate zone. |
| spruce forest                 | (no exact match)                                                      | Consider ENVO_01000196: coniferous forest biome and the type of spruce forest. |
| Pinus pinaster forest        | (no exact match)                                                      | Consider ENVO_01000196: coniferous forest biome and the specific type of pine forest. |
| Temperate Conifer Forest     | ENVO_01000211: temperate coniferous forest biome                   |                                                                |
| subpolar biome [ENVO:01001834]|peatland [ENVO:00000044], subpolar biome[ENVO:01001834]|peatland[ENVO:00000044] | (complex case)                                                      | Consider either ENVO_01001834 (subpolar biome) or ENVO_00000044 (peatland) depending on context. | 
| Soil fungi                   | (not a biome)                                                        | Consider the biome where the soil fungi were found.           |
| temperate biome [ENVO_01001831], temperate, temperate regions | ENVO_01001831: temperate biome                                    | Consider a more specific biome within the temperate zone.   | 
| mangrove biome, mangrove biome [ENVO:01000181], mangrove, Mangrove, mangrove soil, coastal mangrove | ENVO_01000181: mangrove biome                                   |                                                                |
| Pot, pot, pot soil, Pot soil | (not a biome)                                                        | Consider the biome where the pot is located or the plants being grown. |
| Antarctic soil, Antarctic biome, antarctic, Antarctic | (complex case)                                                      | Consider ENVO_01001838 (arid biome) and ENVO_01000339 (polar biome) as Antarctica is a cold desert. |
| ENVO:01001206                | ENVO_01001206: grassland ecosystem                               |                                                                |
| Biofilm(ENVO:00002034)       | ENVO_00002034: biofilm                                           | Consider the environment where the biofilm is found.          |
| ENVO_01001044, soil environment [ENVO:01001044], soil environment, soil/sediment | ENVO_01001044: soil environment                                 | Consider more specific terms if available.                   |
| agroecosystem                | ENVO_00000077: agricultural ecosystem                          |                                                                |
| subantarctic forest          | (no exact match)                                                      | Consider ENVO_01001831 (temperate biome) or ENVO_01001834 (subpolar biome) as possible broader categories. | 
| temperate woodland biome [ENVO:01000221], temperate woodland biome | ENVO_01000221: temperate woodland biome                        |                                                                |
| industrial building, industrial soil biome, industraial waste | (not a biome)                                                        | Consider the broader environment where the building is located (e.g., urban, industrial area). | 
| mountain, Mountain, mountain biome, mountain[ENVO:00000081], Temerperate mountain system, Mountain_Forest, HIGH ALTITUDE SOIL, High altitude Soil | ENVO_00000081: mountain                                        | Consider the specific type of mountain ecosystem (e.g., alpine, subalpine). |
| Orchard soil                | (no exact match)                                                      | Consider the biome of the orchard (e.g., temperate broadleaf forest) and the type of fruit tree. |
| freshwater                  | ENVO_00000873: freshwater biome                                    | Consider the specific freshwater ecosystem (e.g., lake, river). | 
| grassland biome [ENVO:01000177], grassland biome [ENVO:01000177]|mediterranean grassland [ENVO:01000224]  | ENVO_01000177: grassland biome                                |                                                                | 
| Not applicable              | (flagged as missing data)                                               |                                                                | 
| polar biome [ENVO:01000339], polar environment ENVO:01001703 | ENVO_01000339: polar biome                                      | Consider a more specific polar biome (e.g., tundra).        |
| subpolar environment [ENVO_01001704] | ENVO_01001704: subpolar environment                             | Consider a more specific subpolar biome (e.g., boreal forest). | 
| soil environment [ENVO:01001044] | ENVO_01001044: soil environment                                 | Consider more specific terms if available.                   |
| ENVO:01000254                | ENVO_01000254: temperate dry conifer forest biome                   |                                                                |
| tropical dry broadleaf forest, tropical dry broadleaf forest [ENVO:01001799] | ENVO_01001799: tropical dry broadleaf forest biome                   |                                                                |
| alkaline salt lake           | (no exact match)                                                      | Consider a combination of ENVO_00000873 (freshwater biome) and ENVO_00000173 (salt lake) or a more specific saline lake biome. |
| temperate shrubland biome, temperate shrubland biome [ENVO_01000215] | ENVO_01000215: temperate shrubland biome                        |                                                                |
| Temperate grassland biome    | ENVO_01000193: temperate grassland biome                        |                                                                |
| sandy beach biome           | (no exact match)                                                      | Consider ENVO_00000168: beach as a starting point.            | 
| flood plain                  | (no exact match)                                                      | Consider the biome associated with the floodplain (e.g., riparian, wetland). |
| rural village, rural field  | (ambiguous)                                                         | Consider ENVO_01000246 (village biome) or the surrounding biome (e.g., agricultural land, grassland). |
| North American Great Plains, Great plains, North American grassland | (geographic region, not biome)                                      | Consider ENVO_01000193 (temperate grassland biome) or ENVO_01000189 (temperate savanna biome) as potential matches. | 
| Wheat, wheat biome, wheat pot | ENVO_01000245: cropland biome (likely)                                 | Consider the specific type of wheat field.                    |
| glacier biom, glacier retreat | (no exact match)                                                      | Consider ENVO_01001835 (alpine biome) or ENVO_01000339 (polar biome) as glaciers are often found in these regions. |
| estuarine biome [ENVO:01000020], estuary, estuarine biome [ENVO:01000020]|marine sediment [ENVO:03000033]|marine benthic biome [ENVO:01000024] | ENVO_01000020: estuarine biome                                   |                                                                |
| contaminated soil, contaminated soil | (not a biome)                                                        | Consider the type of contamination and the original biome.      | 
| Fynbos, Cape_fynbos          | (no exact match in current ENVO)                                       | This is a specific shrubland biome found in South Africa.    |
| sand                         | (not a biome)                                                        | Consider the biome where the sand is found (e.g., beach, desert). |
| arid biome, arid subtropical [ENVO:01000378], Arid, arid land, arid forest, Hyper arid desert, Hyperarid desert, arid desert | ENVO_01001838: arid biome                                        | Consider specific type of arid environment (e.g., desert, steppe). | 
| Temperate Broadleaf forest   | ENVO_01000202: temperate broadleaf forest biome                   |                                                                |
| soil [ENVO:00001998] | polar biome [ENVO:01000339] | (complex case)                                                      | Consider either ENVO_00001998 (soil biome) or ENVO_01000339 (polar biome) depending on context. | 
| subtropical, subtropics       | ENVO_01001832: subtropical biome                                    | Consider a more specific subtropical biome.                   |
| tropical biome [ENVO:01001830], tropical biome [ENVO_01001830]|peatland [ENVO:00000044], tropical biome [ENVO_01001830], tropical biome [ENVO:01001830]|histosol [ENVO:00002243]|anthropogenic terrestrial biome, tropical biome (ENVO:01001830), Tropics, tropic orchard, tropical region | ENVO_01001830: tropical biome                                    | Consider specific type of tropical environment if possible.   |
| coking plant industrial wasteland soil | (no exact match)                                                      | Consider ENVO_01000219: anthropogenic terrestrial biome.     |
| sugar plantation             | (no exact match)                                                      | Consider ENVO_01000245: cropland biome and the specific crop (sugarcane). | 
| deciduous woodland, deciduous forest | (ambiguous)                                                         | Consider the specific type of deciduous woodland and the broader biome. | 
| Tailing, tailings, Tailings microbial communities, mine tailing soil biome | (no exact match)                                                      | Consider ENVO_01000219: anthropogenic terrestrial biome or a more specific mining-related environment. |
| bacteria, Bacterial and archeal community, wetland bacteria and archaea, soil virome, soil metagenome, soil_metagenome, soil microbiota | (not a biome)                                                        | Consider the biome where the bacteria were found.            | 
| highland, highland soil      | (ambiguous)                                                         | Consider the specific type of highland environment (e.g., mountain, plateau). | 
| fractionation                | (not a biome)                                                        | Consider the context to determine the relevant environment.    | 
| montane shrubland            | ENVO_01000216: montane shrubland biome                            |                                                                |
| Sub-arctic soil biome       | (no exact match)                                                      | Consider ENVO_01001834 (subpolar biome) or ENVO_01000180 (tundra biome). |
| Prokaryotes, Prokaryote        | (not a biome)                                                        | Consider the biome where the prokaryotes were found.           |
| alpine soil [ENVO:00005741] | ENVO_00005741: alpine soil                                      |                                                                |
| pedosphere[ENVO_01000820]    | ENVO_01000820: pedosphere                                        |                                                                | 
| cotton biome                 | (no exact match)                                                      | Consider ENVO_01000245: cropland biome and the specific crop (cotton). |
| plantation                   | (ambiguous)                                                         | Consider the type of plantation (e.g., forest plantation, crop plantation) and the broader biome. |
| dried-soil                   | (not a biome)                                                        | Consider the original biome of the soil.                     |
| ENVO:01000177 (grassland biome) | ENVO_01000177: grassland biome                                |                                                                | 
| microbial community, microbial community [PCO:1000004] |derives from [RO:0001000]| soil biocrust [ENVO:01000910], soil microbial community, microbial feature | (complex cases)                                                      | Consider ENVO_01000910 (soil biocrust) or the specific environment where the microbial community is found. |
| temperate grassland biome [ENVO:01000193] | ENVO_01000193: temperate grassland biome                        |                                                                | 
| wetlands                     | ENVO_01001209: wetland ecosystem                              | Consider wetland type (e.g., marsh, swamp, bog) if possible.   |
| xeric shrubland biome        | ENVO_01000218: xeric shrubland biome                             |                                                                |
| flooded grassland biome [ENVO:01000195] | ENVO_01000195: flooded grassland biome                         |                                                                |
| beach, beach sediment, Beach  | ENVO_00000168: beach                                           | Consider the specific type of beach environment.               | 
| the Yellow Sea Cold Water Mass | (geographic region, not biome)                                      | Consider the marine biomes in this region.                     |
| Soils, soil [ENVO: 00001998] | ENVO_00001998: soil biome                                       |                                                                |
| oil palm seedling biome     | (no exact match)                                                      | Consider the biome of the oil palm plantation.                 |
| ENVO:01000182, "Temperate ""mediterranean"" desert biome [ENVO_01000182]", Mediterranean1, Mediterranean2, Mediterranean3, Mediterranean4, Mediterranean5, Mediterranean6, Mediterranean7, Mediterranean8, Mediterranean9, Mediterranean_vegetation | ENVO_01000182: temperate desert biome                               | Consider the specific type of mediterranean ecosystem.         | 
| pasture, Pasture             | (ambiguous)                                                         | Consider ENVO_01000247 (rangeland biome) or ENVO_01000177 (grassland biome) depending on context. |
