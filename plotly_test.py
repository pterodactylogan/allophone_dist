import plotly.express as px
import pandas

df = pandas.read_csv("sibilant_formants.csv")
print(len(df["Frequency"]))

fig = px.scatter(df, x="Frequency",
                 y=[1 for i in range(len(df["Frequency"]))],
                 color="Language",
                 symbol="Symbol",
                 log_x=True)
fig.show()
