import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.options.display.float_format = '${:0,.0f}'.format

# read in the data
pd.read_csv(r'C:\Users\ekopen\Documents\Kaggle\Forbes_2000_top_company_CLNQ11.csv').to_pickle("./fortune2000.pkl")
df_original = pd.read_pickle("fortune2000.pkl")

def data_clean_filter(df):
    # there was an issue with weird brackets in the employee column (column 10) so getting ride of these
    for x in range(len(df.index)):
        if df.iloc[x,10][-1] == "]":
            df.iloc[x,10] = df.iloc[x,10][:-1]
    # converting some columns to float values so they can be used in formulas
    dirty_Columns = ['Revenue (Billions)','Profits (Billions)','Market Value (Billions)','Total Employees']
    for x in dirty_Columns:
        df[x] = pd.to_numeric(df[x])
    #filtering out holding companies with low employee count (these have weird metrics that skew the analysis)
    # and any non-US companies (not sure what their reporting standards are)
    # also grouping by industry
    df = df[(df['Total Employees']>1000) & (df['Country']=='United States')]
    return df

def analysis1(df):
    # attempting to analyze financial metrics by employee over each industry
    # group by industry
    df = df[['Industry','Revenue (Billions)','Profits (Billions)','Market Value (Billions)',
         'Total Employees']].groupby('Industry').agg('sum')
    # establishing columns to be used in calculations and performing the calc below
    calc_Columns = ['Revenue (Billions)','Profits (Billions)','Market Value (Billions)']
    newColumns = ['Revenue per Employee', 'Profits per Employee', 'Market Value per Employee']
    for x,y in zip(newColumns,calc_Columns):
        df[x] = (df[y] / (df['Total Employees'])) * 1000000000
    df = df.sort_values(by=['Profits per Employee'], ascending=False)
    return df

def analysis2(df, top_industry):
    # THIS ISNT WORKING!!!!!!
    df = df.filter(items = ['Diversified Financials'], axis=0)
    return df

df_cleaned_filtered = data_clean_filter(df_original)
df_grouped_analysis = analysis1(df_cleaned_filtered)
top_industry = df_grouped_analysis.head(1)

#THIS ISNT WORKING!!!!!!
df_top_industry = analysis2(df_cleaned_filtered, top_industry)




