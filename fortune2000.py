import pandas as pd
import numpy as np

pd.read_csv(r'C:\Users\ekopen\Documents\Kaggle\Forbes_2000_top_company_CLNQ11.csv').to_pickle("./fortune2000.pkl")
df = pd.read_pickle("fortune2000.pkl")

# there was an issue with weird brackets in the employee column (column 10) so getting ride of these
for x in range(len(df.index)):
    if df.iloc[x,10][-1] == "]":
        df.iloc[x,10] = df.iloc[x,10][:-1]



calcColumns = ['Revenue (Billions)','Profits (Billions)','Market Value (Billions)','Total Employees']
for x in calcColumns:
    df[x] = pd.to_numeric(df[x])

calcColumns = calcColumns[:-1]
newColumns = ['Revenue per Employee', 'Profits per Employee', 'Market Value per Employee']

print(calcColumns)

#figure out a way to loop through both arrays at the same time
# for x in newColumns,  :
#     for y in calcColumns
#     df[x] = (float(df[calcColumns]) / float(df['Total Employees'])) * 1000000000

print(df.info())
