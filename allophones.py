import pandas as pd
import plotly.express as px

phoible_url = "https://github.com/phoible/dev/blob/master/data/phoible.csv?raw=true"

#May need: Allophones, Marginal, InventoryID
phoible_frame = pd.read_csv(phoible_url, usecols=["LanguageName",
                                                  "Phoneme",
                                                  "InventoryID",
                                                  "Allophones",
                                                  "Marginal"])
phoible_frame.dropna(subset=["Allophones"], inplace=True)

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

def create_allophone_table():
    # Group by language
    lang_groups = phoible_frame.groupby("InventoryID", group_keys=True)
    languages = []
    phoneme_counts = []
    counts_with_allophones = []
    percents_with_allophones = []

    for lang in lang_groups:
        lang_df = lang[1]
        lang_df.reset_index()
        languages.append(lang_df.iloc[0]["LanguageName"])
        num_phonemes = len(lang_df)
        num_phon_with_allophones = len(lang_df[lang_df.apply(lambda x:
                                    len(x["Allophones"].split()) > 1, axis=1)])
        phoneme_counts.append(num_phonemes)
        counts_with_allophones.append(num_phon_with_allophones)
        percents_with_allophones.append(100 * num_phon_with_allophones / num_phonemes)
        
    return pd.DataFrame(data={"language": languages,
                            "numPhonemes": phoneme_counts,
                            "numWithAllophones": counts_with_allophones,
                            "pctWithAllophones": percents_with_allophones})
        
    

def main():
    allophone_frame = create_allophone_table()
    
    fig = px.scatter(allophone_frame, x="numPhonemes",
                     y="pctWithAllophones")
    fig.show()

    allophones_no_zeros = allophone_frame[allophone_frame["pctWithAllophones"] > 0]
    fig = px.scatter(allophones_no_zeros, x="numPhonemes",
                     y="pctWithAllophones",
                     trendline="ols",
                     trendline_options=dict(log_x=True))
    fig.show()

if __name__ == "__main__":
    main()
