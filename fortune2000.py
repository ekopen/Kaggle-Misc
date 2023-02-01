import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.options.display.float_format = '${:0,.0f}'.format
#I know I shouldnt be doing this, but I am not patient enough right now to figure out why I kept getting these warnings
pd.options.mode.chained_assignment = None  # default='warn'


# find the dataset source here: https://www.kaggle.com/datasets/rakkesharv/forbes-2000-global-companies
pd.read_csv(r'C:\Users\ekopen\Documents\Kaggle\Forbes_2000_top_company_CLNQ11.csv').to_pickle('./fortune2000.pkl')
df_original = pd.read_pickle('fortune2000.pkl')

# the CSV file had some weird formatting issues and data I didn't want to use. Cleaning it and filtering it below
def data_clean_filter(df):
    # there was an issue with weird brackets in the employee column (column 10) so getting ride of these
    for x in range(len(df.index)):
        if df.iloc[x,10][-1] == ']':
            df  .iloc[x,10] = df.iloc[x,10][:-1]
    # converting some columns to float values so they can be used in formulas
    dirty_Columns = ['Revenue (Billions)','Profits (Billions)','Market Value (Billions)','Total Employees']
    for x in dirty_Columns:
        df[x] = pd.to_numeric(df[x])
    #filtering out holding companies with low employee count (these have weird metrics that skew the analysis)
    # and any non-US companies (not sure what their reporting standards are)
    # filtering out automotive which only has two companies for some reason, and consumer durables which is weird
    df = df[(df['Total Employees']>3000) & (df['Country']=='United States') & (df['Industry'] != 'Automotive') &
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
        'Transportation': 'Transport',
        'Retailing': 'Retail',
        'Food Markets': 'Food',
        'Hotels, Restaurants & Leisure': 'Leisure' })
    return df

# creating columns to analyze companies from a few different metrics
def calculate_columns(df):
    calc_Columns = ['Revenue (Billions)','Profits (Billions)','Market Value (Billions)']
    newColumns = ['Revenue per Employee', 'Profits per Employee', 'Market Value per Employee']
    for x,y in zip(newColumns,calc_Columns):
        df[x] = (df[y] / (df['Total Employees'])) * 1000000000
    return df

# analyze financial metrics by employee by industry
def analysis1(df):
    dfa1 = df[['Industry','Industry Nickname','Revenue (Billions)','Profits (Billions)','Market Value (Billions)',
         'Total Employees']].groupby('Industry Nickname').agg('sum', numeric_only=True)
    dfa1 = calculate_columns(dfa1)
    dfa1 = dfa1.sort_values(by=['Profits per Employee'], ascending=False).reset_index()
    return dfa1

# analyze financial metrics by employee by industry for a top amount of industries and companies
def analysis3(df):
    num_top_industries = 5
    dfgrouped = analysis1(df)
    num_top_companies = 10
    dfa3 = calculate_columns(df).sort_values(by=['Profits per Employee'], ascending=False)
    dfa3 = dfa3[['Organization Name','Industry Nickname','Revenue (Billions)','Profits (Billions)','Market Value (Billions)',
         'Total Employees']].groupby('Industry Nickname').head(num_top_companies)
    dfa3 = calculate_columns(dfa3)
    dfgrouped = dfgrouped['Industry Nickname'].to_dict()
    dfgrouped_inv = {v: k for k, v in dfgrouped.items()}
    dfa3['Industry Rank'] = dfa3['Industry Nickname'].map(dfgrouped_inv)
    dfa3 = dfa3.sort_values(by=['Industry Rank','Profits per Employee'], ascending=[True, False]).head(
        num_top_industries*num_top_companies)
    return dfa3

df_cleaned_filtered = data_clean_filter(df_original)
df_grouped_industries = analysis1(df_cleaned_filtered)
df_top_companies_by_top_industries = analysis3(df_cleaned_filtered)

"""Different views, charts, and analysis are commented out below"""
# print('The five MOST profitable industries per employee are: ' +  str((df_grouped_industries
#                                                                        ['Industry Nickname'].tolist()[0:5])))
# print('The five LEAST profitable industries per employee are: ' +  str((df_grouped_industries
#                                                                         ['Industry Nickname'].tolist()[-5:])))

# print('Select one industry to retrieve a dataframe for: ')
# industry_specifier = input()
# def analysis2(df, industry):
#     #creating a way to drill down into certain industries
#     dfa2 = df[df['Industry Nickname'] == industry]
#     dfa2 = calculate_columns(dfa2)
#     dfa2 = dfa2.sort_values(by=['Profits per Employee'], ascending=False)
#     return dfa2
# df_specific_industry_analysis = analysis2(df_cleaned_filtered, industry_specifier)

# industries = df_grouped_industries['Industry Nickname']
# profit_employee = df_grouped_industries['Profits per Employee']
# fig, ax = plt.subplots(figsize =(16, 9))
# ax.barh(industries, profit_employee)
# ax.set_title('Industries by average profit per employee',
#              loc ='left' )
# ax.xaxis.set_major_formatter('${x:1,.0f}')
# plt.show()

# companies = df_top_companies_by_top_industries['Organization Name']
# profit_employee_v2 = df_top_companies_by_top_industries['Profits per Employee']
# fig, ax = plt.subplots(figsize =(16, 9))
# ax.barh(companies, profit_employee_v2)
# ax.set_title('Industries by average profit per employee',
#              loc ='left' )
# ax.xaxis.set_major_formatter('${x:1,.0f}')
# plt.show()
