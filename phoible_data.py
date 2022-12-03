import pandas as pd

phoible_url = "https://github.com/phoible/dev/blob/master/data/phoible.csv?raw=true"

#May need: Allophones, Marginal, InventoryID
phoible_frame = pd.read_csv(phoible_url, usecols=["strident",
                                                  "continuant",
                                                  "periodicGlottalSource",
                                                  "LanguageName",
                                                  "Phoneme",
                                                  "InventoryID"])

#+strident, +continuant, -voice = unvoiced sibilants
sibilant_frame = phoible_frame[phoible_frame["strident"] == "+"]
sibilant_frame = sibilant_frame[sibilant_frame["continuant"] == "+"]
sibilant_frame = sibilant_frame[sibilant_frame["periodicGlottalSource"]
                                == "-"]


print(sibilant_frame.columns)

lang_groups = sibilant_frame.groupby("InventoryID", group_keys=True)

inventories = []
counts = []
lengths = []

for lang in lang_groups:
    phoneme_list = sorted([ph for ph in lang[1]["Phoneme"]])
    sib_list_key = ", ".join(phoneme_list)
    if sib_list_key in inventories:
        counts[inventories.index(sib_list_key)] += 1
    else:
        inventories.append(sib_list_key)
        counts.append(1)
        lengths.append(len(phoneme_list))

output_frame = pd.DataFrame(data={"inventory": inventories,
                                  "inventory size": lengths,
                                  "count": counts})
output_frame.to_csv('sibilant_inventories.csv')

# print out most common inventories of sibilants
##for key, value in sorted(inventories.items(), key=lambda item: item[1]):
##    print(key + ": " + str(value))
