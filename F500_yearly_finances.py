import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# find the dataset source here:
# https://www.kaggle.com/datasets/yashsrivastava51213/revenue-and-profit-of-fortune-500-companies?select=fortune500.csv
pd.read_csv(r'C:\Users\ekopen\Documents\Kaggle\fortune500.csv').to_pickle('./fortune500.pkl')
df_original = pd.read_pickle('fortune500.pkl')

# print(df_original.keys())

df_grouped = df_original[['Year','Revenue (in millions)','Profit (in millions)']].groupby('Year').agg('sum')

x = df_grouped['Year']
y1 = df_grouped['Revenue (in millions']
# y2 = df_grouped['Profit (in millions']

plt.plot(x, y1)
plt.xlabel("X-axis")  # add X-axis label
plt.ylabel("Y-axis")  # add Y-axis label
plt.title("Any suitable title")  # add title
plt.show()
