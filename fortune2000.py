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
dffiltered = df[(df['Total Employees']>1000) & (df['Country']=='United States')]

# establishing columns to be used in calculations and performing the calc below
calcColumns = calcColumns[:-1]
newColumns = ['Revenue per Employee', 'Profits per Employee', 'Market Value per Employee']
for x,y in zip(newColumns,calcColumns):
    dffiltered[x] = (dffiltered[y] / (df['Total Employees'])) * 1000000000

# checking to make things look right
# print(dffiltered.info())
print(dffiltered)

#SOMETHING ISNT WORKING!!!!!!
dfsummary = dffiltered[['Organization Name', 'Industry', 'Total Employees', 'Profits (Billions)', 'Revenue per Employee',
                      'Profits per Employee', 'Market Value per Employee']].groupby([
                        'Industry']).sum(['Revenue per Employee','Total Employees', 'Profits (Billions)',
                                          'Profits per Employee', 'Market Value per Employee']).sort_values(by=[
                                            'Profits per Employee'],ascending=False)

pd.options.display.float_format = '${:0,.0f}'.format
print(dfsummary)

# df.plot(kind='bar', x='Date', y='Random Walk')
# plt.show()
