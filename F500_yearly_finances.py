import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None  # default='warn'

# find the dataset source here:
# https://www.kaggle.com/datasets/yashsrivastava51213/revenue-and-profit-of-fortune-500-companies?select=fortune500.csv
# pd.read_csv(r'C:\Users\ekopen\Documents\Kaggle\fortune500.csv').to_pickle('./fortune500.pkl')
# df = pd.read_pickle('fortune500.pkl')
#

# #cleaning the dataset
# df = df[df['Rank'] <= 500]
# df['Revenue (in millions)'] = pd.to_numeric(df['Revenue (in millions)'].str.replace(',',''))
# df['Profit (in millions)'] = df['Profit (in millions)'].str.replace(',','')
# df['Profit Margin'] = 0
# average_pm = .08
# for x in range(len(df.index)):
#     if df.iloc[x,4] != 'N.A.':
#         df.iloc[x,5] = pd.to_numeric(df.iloc[x,4])/df.iloc[x,3]
#     else:
#         df.iloc[x,5] = average_pm
# df['Profit (in millions)'] = df['Revenue (in millions)'] * df['Profit Margin']
# df.to_pickle('./cleaneddf.pkl')

#group the dataset for initial analysis
df = pd.read_pickle(r"C:\Users\ekopen\PycharmProjects\pythonProject\cleaneddf.pkl")
df_focus = df[(df['Year'] >= 1955) & (df['Year'] <= 2009)]
dfgrouped = df_focus.groupby('Year').agg('sum').reset_index()
dfgrouped['Profit Margin'] = dfgrouped['Profit (in millions)'] / dfgrouped['Revenue (in millions)']

#create a dictionary with some statistical info to get rid of outliers
df_dict = {}
for x in dfgrouped['Year']:
    year_dict = {}
    year_dict['DF'] = df_focus[df_focus['Year'] == x]
    year_dict['Average PM'] = np.average(year_dict['DF']['Profit Margin'], weights=year_dict['DF']['Revenue (in millions)'])
    year_dict['Std Dev PM'] = np.std(year_dict['DF']['Profit Margin'])
    year_dict['Upper Bound'] = (year_dict['Std Dev PM'] + year_dict['Std Dev PM'] * 2)
    year_dict['Lower Bound'] = (year_dict['Std Dev PM'] + year_dict['Std Dev PM'] * -2)
    bound_test = []
    for y in range(len(year_dict['DF']['Profit Margin'])):
        if (year_dict['DF'].iloc[y,5] > year_dict['Upper Bound']) or (year_dict['DF'].iloc[y,5] < year_dict['Lower Bound']):
            bound_test.append(0)
        else:
            bound_test.append(1)
    year_dict['DF']['In Bounds?'] = bound_test
    df_dict[x] = year_dict

#reconsolidate the dictionary with stat info
filtereddf = pd.DataFrame()
for keys in df_dict:
    filtereddf = filtereddf.append(df_dict[keys]['DF'], ignore_index=True)
filtereddf = filtereddf[filtereddf['In Bounds?'] == 1]
filtereddf = filtereddf.groupby('Year').agg('sum').reset_index()
filtereddf['Profit Margin'] = filtereddf['Profit (in millions)'] / filtereddf['Revenue (in millions)']

#create an annual standard deviation distribution by year to append on graph

#graph it
x2 = filtereddf['Year']
y3 = filtereddf['Profit Margin']
z = np.polyfit(x2, y3, 1)
p = np.poly1d(z)
plt.plot(x2, y3, label="Profit Margin")
plt.plot(x2, p(x2), label="Profit Margin")
plt.xlabel("Year")
plt.ylabel("%")
plt.title("F500 Profit Margin Over Time")
plt.show()
