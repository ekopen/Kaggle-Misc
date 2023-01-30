import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.options.display.float_format = '${:0,.0f}'.format
#I know I shouldnt be doing this, but I am not patient enough right now to figure out why I kept getting these warnings
pd.options.mode.chained_assignment = None  # default='warn'

# read in the data
pd.read_csv(r'C:\Users\ekopen\Documents\Kaggle\Forbes_2000_top_company_CLNQ11.csv').to_pickle('./fortune2000.pkl')
df_original = pd.read_pickle('fortune2000.pkl')

def data_clean_filter(df):
    # there was an issue with weird brackets in the employee column (column 10) so getting ride of these
    for x in range(len(df.index)):
        if df.iloc[x,10][-1] == ']':
            df.iloc[x,10] = df.iloc[x,10][:-1]
    # converting some columns to float values so they can be used in formulas
    dirty_Columns = ['Revenue (Billions)','Profits (Billions)','Market Value (Billions)','Total Employees']
    for x in dirty_Columns:
        df[x] = pd.to_numeric(df[x])
    #filtering out holding companies with low employee count (these have weird metrics that skew the analysis)
    # and any non-US companies (not sure what their reporting standards are)
    # filtering out automotive which only has two companies for some reason
    df = df[(df['Total Employees']>1000) & (df['Country']=='United States') & (df['Industry'] != 'Automotive') &
    (df['Industry'] != 'Consumer Durables')]
    # creating nicknames for the columns, as industry names are a bit long
    df['Industry Nickname'] = df['Industry']
    df['Industry Nickname'] = df['Industry Nickname'].replace({
        'Diversified Financials' : 'Finance',
        'Oil & Gas Operations': 'Oil',
        'Semiconductors': 'Chips',
        'IT Software & Services': 'IT',
        'Technology Hardware & Equipment': 'Tech Hardware',
        'Drugs & Biotechnology': 'Biotech',
        'Banking': 'Banking',
        'Telecommunications Services': 'Telecomm',
        'Chemicals': 'Chemicals',
        'Utilities': 'Utilities',
        'Insurance': 'Insurance',
        'Business Services & Supplies': 'Biz Supplies',
        'Materials': 'Materials',
        'Household & Personal Products': 'Household Items',
        'Conglomerates': 'Conglomerates',
        'Food, Drink & Tobacco': 'Food, Drink & Tobacco',
        'Media': 'Media',
        'Capital Goods': 'Capital Goods',
        'Construction': 'Construction',
        'Aerospace & Defense': 'Aero/Defense',
        'Health Care Equipment & Services': 'Healthcare Support',
        'Trading Companies': 'Commodity Trading',
        # 'Consumer Durables': 'CHECK',
        'Transportation': 'Transport',
        'Retailing': 'Retail',
        'Food Markets': 'Food',
        'Hotels, Restaurants & Leisure': 'Leisure' })
    df = df.sort_values(by=['Total Employees'], ascending=False)
    return df

def calculate_columns(df):
    #creating some calculation columns
    calc_Columns = ['Revenue (Billions)','Profits (Billions)','Market Value (Billions)']
    newColumns = ['Revenue per Employee', 'Profits per Employee', 'Market Value per Employee']
    for x,y in zip(newColumns,calc_Columns):
        df[x] = (df[y] / (df['Total Employees'])) * 1000000000
    return df

def analysis1(df):
    # attempting to analyze financial metrics by employee over each industry
    # group by industry
    # the industry nickname is throwing an error here.... i think it is based on how i renamed it? Not sure
    df = df[['Industry','Industry Nickname','Revenue (Billions)','Profits (Billions)','Market Value (Billions)',
         'Total Employees']].groupby('Industry Nickname').agg('sum')
    df = calculate_columns(df)
    df = df.sort_values(by=['Profits per Employee'], ascending=False).reset_index()
    return df

def analysis2(df, industry):
    #creating a way to drill down into certain industries
    df = df[df['Industry'] == industry]
    df = calculate_columns(df)
    df = df.sort_values(by=['Profits per Employee'], ascending=False)
    return df

def analysis3_v2(df):
    # top # of companies by industry
    dfgrouped = analysis1(df)
    num_top_companies = 5
    #get top 'x'' companies by industry and add some calculated columns
    df = df[['Organization Name','Industry Nickname','Revenue (Billions)','Profits (Billions)','Market Value (Billions)',
         'Total Employees']].groupby('Industry Nickname').head(num_top_companies)
    df = calculate_columns(df)

    dfgrouped = dfgrouped['Industry Nickname'].to_dict()
    dfgrouped_inv = {v: k for k, v in dfgrouped.items()}

    df['Industry Rank'] = df['Industry Nickname'].map(dfgrouped_inv)
    df = df.sort_values(by=['Industry Rank','Profits per Employee'], ascending=[True, False])

    return df



df_cleaned_filtered = data_clean_filter(df_original)

# DF_grouped_analysis = analysis1(df_cleaned_filtered)
DF_grouped_analysis_2 = analysis3_v2(df_cleaned_filtered)

print(DF_grouped_analysis_2)

# for x in range(len(DF_grouped_analysis.index)):
#     print(DF_grouped_analysis.index.tolist()[x])
# print('The five MOST profitable industries per employee are: ' +  str((DF_grouped_analysis.index.tolist()[0:5])))
# print('The five LEAST profitable industries per employee are: ' +  str((DF_grouped_analysis.index.tolist()[-5:])))

# bar = DF_grouped_analysis['Profits per Employee'].plot(x='Industry', y='Profit/Employee', kind='bar')

# df = pd.DataFrame({'lab':['A', 'B', 'C'], 'val':[10, 30, 20]})
# ax = df.plot.bar(x='lab', y='val', rot=0)


# print('Select one industry to retrieve a dataframe for: ')
# industry_specifier = input()
# DF_detailed_industry_analysis = analysis2(df_cleaned_filtered, industry_specifier)
