import pandas as pd

phoible_url = "https://github.com/phoible/dev/blob/master/data/phoible.csv?raw=true"

#May need: Allophones, Marginal, InventoryID
phoible_frame = pd.read_csv(phoible_url, usecols=["strident",
                                                  "continuant",
                                                  "periodicGlottalSource",
                                                  "LanguageName",
                                                  "Phoneme",
                                                  "InventoryID",
                                                  "Allophones",
                                                  "Marginal"])

def count_allophones(inventory_id):
    lang_df = phoible_frame[phoible_frame["InventoryID"] == inventory_id]
    lang_df.reset_index()
    num_phonemes = len(lang_df)
    num_phon_with_allophones = len(lang_df[lang_df.apply(lambda x:
                                    len(x["Allophones"].split()) > 1, axis=1)])
    print(lang_df.iloc[0]["LanguageName"])
    print("number of phonemes:", num_phonemes)
    print("number with allophones:", num_phon_with_allophones)
    print("percent with allophones:", 100 * num_phon_with_allophones / num_phonemes)
    print()

def main():
    #Xoo
    count_allophones(1379)

    #English
    count_allophones(2175)

    #Nasoi
    count_allophones(60)

if __name__ == "__main__":
    main()
