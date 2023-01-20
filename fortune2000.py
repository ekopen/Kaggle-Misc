import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read in the data
pd.read_csv(r'C:\Users\ekopen\Documents\Kaggle\Forbes_2000_top_company_CLNQ11.csv').to_pickle("./fortune2000.pkl")
df = pd.read_pickle("fortune2000.pkl")

# there was an issue with weird brackets in the employee column (column 10) so getting ride of these
for x in range(len(df.index)):
    if df.iloc[x,10][-1] == "]":
        df.iloc[x,10] = df.iloc[x,10][:-1]

# converting some columns to float values so they can be used in formulas
calcColumns = ['Revenue (Billions)','Profits (Billions)','Market Value (Billions)','Total Employees']
for x in calcColumns:
    df[x] = pd.to_numeric(df[x])

#filtering out holding companies with low employee count (these have weird metrics that skew the analysis)
# and any non-US companies (not sure what their reporting standards are)
# also grouping by industry
dffiltered1 = df[(df['Total Employees']>1000) & (df['Country']=='United States')]
dffiltered2 = dffiltered1[['Industry','Revenue (Billions)','Profits (Billions)',
                           'Market Value (Billions)','Total Employees']].groupby('Industry').agg('sum')

# establishing columns to be used in calculations and performing the calc below
calcColumns = calcColumns[:-1]
newColumns = ['Revenue per Employee', 'Profits per Employee', 'Market Value per Employee']
for x,y in zip(newColumns,calcColumns):
    dffiltered2[x] = (dffiltered2[y] / (dffiltered2['Total Employees'])) * 1000000000

dffiltered3 = dffiltered2.sort_values(by=['Profits per Employee'], ascending=False)

pd.options.display.float_format = '${:0,.0f}'.format

dffinal = dffiltered3

print(dffinal)
