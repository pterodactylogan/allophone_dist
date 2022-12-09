import pandas as pd
import plotly.express as px

phoible_url = "https://github.com/phoible/dev/blob/master/data/phoible.csv?raw=true"

phoible_frame = pd.read_csv(phoible_url, usecols=["LanguageName",
                                                  "Phoneme",
                                                  "InventoryID",
                                                  "Allophones",
                                                  "Marginal",
                                                  "strident",
                                                  "continuant",
                                                  "periodicGlottalSource"])

# Remove rows with no Allophone information
phoible_frame.dropna(subset=["Allophones"], inplace=True)

#+strident, +continuant, -voice = unvoiced sibilants
sibilant_frame = phoible_frame[phoible_frame["strident"] == "+"]
sibilant_frame = sibilant_frame[sibilant_frame["continuant"] == "+"]
sibilant_frame = sibilant_frame[sibilant_frame["periodicGlottalSource"]
                                == "-"]
# laminal diacritic.
lam = chr(840)

# variable storing sibilant ordering
sibilant_order = ["ʂ", "ʃˤ", "ʃˠ", "ʃ", "ɕ", "ʃʷ", "sˤ", "sˠ", "sʲ", "s",
                  "s̪|s", "s̪ʲ", "s̪ˤ", "s̪", "sʷ"]

ignore = ["z", "ç", "h", "t", "ʒ", "ʐ", "ɦ", "n", "θ", "ð", "c",
          "f", "d", "ɧ", "n"]

# ejective, long, laminal, ??, syllabic, aspirated, glottalized, nasalized,
# half-long, labial+velar, apical, voiced, labial+palatal
diacritics_to_ignore = ["ʼ", "ː", lam, "͉", "̩", "ʰ", "ˀ", "̃", "ˑ", "ʷˠ",
                        "̺", "̬", "ᶣ"]

lang_groups = sibilant_frame.groupby("InventoryID", group_keys=True)

def getCanonicalSibilant(phoneme):
    for diac in diacritics_to_ignore:
        phoneme = phoneme.replace(diac, "")
    # 2 unicode values for dental symbol
    phoneme = phoneme.replace(chr(827), chr(810))
    if phoneme in sibilant_order:
        return phoneme
    if phoneme == "ʃʲ":
        return "ɕ"
    if phoneme[0] not in ignore:
        print(phoneme)
    return ""
    

num_well_behaved = 0
num_crossing = 0
for lang in lang_groups:
    lang_frame = lang[1]
    phoneme_list = [ph for ph in lang[1]["Phoneme"]]
    canonical_list = [getCanonicalSibilant(ph) for ph in phoneme_list]
    # remove blanks and duplicates, order by spectral mean
    canonical_list = list(filter(lambda x: x != "", canonical_list))
    canonical_list = sorted(list(set(canonical_list)),
                            key=lambda x: sibilant_order.index(x))
    for ph in phoneme_list:
        canon_ph = getCanonicalSibilant(ph)
        if canon_ph == "":
            continue
        invent_i = canonical_list.index(canon_ph)
        if invent_i == 0:
            left_bound = 0
        else:
            left_bound = sibilant_order.index(canonical_list[invent_i-1])
        if invent_i == len(canonical_list)-1:
            right_bound = len(sibilant_order)
        else:
            right_bound = sibilant_order.index(canonical_list[invent_i+1])

        allophones = lang_frame[lang_frame["Phoneme"] == ph].iloc[0]["Allophones"]
        for al in allophones.split():
            canon_al = getCanonicalSibilant(al)
            if al == ph or canon_al=="":
                continue
            al_i = sibilant_order.index(canon_al)
            if al_i >= left_bound and al_i <= right_bound:
                num_well_behaved += 1
            else:
                print(lang_frame.iloc[0]["LanguageName"])
                print(canonical_list)
                num_crossing += 1


print("well behaved:", num_well_behaved)
print("Crossing:", num_crossing)
# Test with specific languages
