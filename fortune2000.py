import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.read_csv(r'C:\Users\ekopen\Documents\Kaggle\Forbes_2000_top_company_CLNQ11.csv').to_pickle("./fortune2000.pkl")
df = pd.read_pickle("fortune2000.pkl")

# there was an issue with weird brackets in the employee column (column 10) so getting ride of these
for x in range(len(df.index)):
    if df.iloc[x,10][-1] == "]":
        df.iloc[x,10] = df.iloc[x,10][:-1]

calcColumns = ['Revenue (Billions)','Profits (Billions)','Market Value (Billions)','Total Employees']
for x in calcColumns:
    df[x] = pd.to_numeric(df[x])

#attempting to filter out holding companies with low employee count
dffiltered = df[(df['Total Employees']>1000)]


calcColumns = calcColumns[:-1]
newColumns = ['Revenue per Employee', 'Profits per Employee', 'Market Value per Employee']

for x,y in zip(newColumns,calcColumns):
    dffiltered[x] = (dffiltered[y] / (df['Total Employees'])) * 1000000000

print(dffiltered.info())

dfsorted = dffiltered.sort_values(by=['Profits per Employee'],ascending=False)

pd.options.display.float_format = '${:0,.0f}'.format
print(dfsorted[['Organization Name','Revenue per Employee','Total Employees', 'Profits per Employee', 'Market Value per Employee']])

# df.plot(kind='bar', x='Date', y='Random Walk')
# plt.show()
