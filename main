import pandas as pd
import numpy as np

pd.read_csv(r'C:\Users\ekopen\Documents\Kaggle\Hotel Reservations.csv').to_pickle("./hotel_data.pkl")
df = pd.read_pickle("hotel_data.pkl")

#print(df.info())
print(df[['arrival_month','arrival_year','avg_price_per_room']].groupby(['arrival_month','arrival_year','avg_price_per_room']).mean('avg_price_per_room'))
#print(df['no_of_adults'].groupby('no_of_adults').sum('avg_price_per_room'))
