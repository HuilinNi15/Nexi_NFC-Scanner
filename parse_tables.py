import pandas as pd
from tabula import read_pdf 
import json

tables = read_pdf("tag_tables.pdf", pages = 'all')
df = pd.concat(tables)

df[['Tmp1', 'Tmp2']] = df['Template'].str.split('or', 1, expand = True)
df = df.drop(['Template'], axis = 1)

tags = pd.melt(df, id_vars=['Name', 'Tag'], value_vars=['Tmp1', 'Tmp2']).drop(['variable'], axis=1)
tags = tags.rename(mapper={'value': 'Templates'}, axis=1)
templates = tags['Templates'].str.replace("'", '').str.strip()
tags = tags['Tag'].str.replace("'", '').str.strip()

templates.to_csv('Templates.csv', index=False)
tags.to_csv('Tags.csv', index=False)
tags.to_json('Tags.json', orient='split')
