import pandas as pd

df = pd.read_pickle('dataframe.pkl')
print(df.loc[df.found == True])
