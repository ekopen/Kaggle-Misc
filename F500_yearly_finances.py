import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# find the dataset source here:
# https://www.kaggle.com/datasets/yashsrivastava51213/revenue-and-profit-of-fortune-500-companies?select=fortune500.csv
pd.read_csv(r'C:\Users\ekopen\Documents\Kaggle\fortune500.csv').to_pickle('./fortune500.pkl')
df = pd.read_pickle('fortune500.pkl')

df = df[df['Rank'] <= 500]
average_pm = .08
df['Profit Margin'] = 0

df['Revenue (in millions)'] = pd.to_numeric(df['Revenue (in millions)'].str.replace(',',''))

df['Profit (in millions)'] = df['Profit (in millions)'].str.replace(',','')

for x in range(len(df.index)):
    if df.iloc[x,4] != 'N.A.':
        df.iloc[x,5] = pd.to_numeric(df.iloc[x,4])/df.iloc[x,3]
    else:
        df.iloc[x,5] = average_pm

df['Profit (in millions)'] = df['Revenue (in millions)'] * df['Profit Margin']
df_focus = df[df['Year'] == 2003].sort_values(by=['Profit (in millions)'], ascending=True)
dfgrouped = df.groupby('Year').agg('sum').reset_index()
dfgrouped['Profit Margin'] = dfgrouped['Profit (in millions)'] / dfgrouped['Revenue (in millions)']

df_dict = {}

for x in dfgrouped['Year']:
    df_dict[x] = df[df['Year'] == x]

print(df_dict)

# x2 = df['Year']
# y3 = df['Profit Margin']
# z = np.polyfit(x2, y3, 1)
# p = np.poly1d(z)
#
# plt.plot(x2, y3, label="Profit Margin")
# plt.plot(x2, p(x2), label="Profit Margin")
# plt.xlabel("Year")
# plt.ylabel("%")
# plt.title("F500 Profit Margin Over Time")
# plt.show()

