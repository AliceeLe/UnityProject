from datetime import datetime, date, timezone
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read csv file
df = pd.read_csv('./data/SampleData_Test_Lite.csv', encoding='latin1')
"""
Overview
1. Aggregate data from 2 dashboards into a single CSV file. May involve data cleaning and preprocessing. 
Create new columns for targetted data (Target, Actual, Product groups, etc.).
2. Create visualization using pandas, matplotlib, and seaborn to visualize each chart. 
3. Create dashboard using Dash or Streamlit
4. Send email using smtplib 

Look out for pipelining process 
"""

# Visualize target and actual 

# Clean data: Only keep rows with valid month and year
validMonthYear = ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06', '2024-07',
 '2024-08', '2024-09', '2024-10', '2024-11', '2024-12']
# Function change yearmonth into DateTime data type
def change_datetime_type(date_string:str) -> datetime:
    '''
    Type cast yearmonth column from string type to datetime type
        Parameters: date_string (str): yearmonth in string type
        Returns: date_string (datetime): yearmonth in datetime type
    '''
    date_format = "%Y-%m"
    return datetime.strptime(date_string, date_format)


# Filter the DataFrame to only include rows with valid month-year values
df_filtered = df[df['YearMonth'].isin(validMonthYear)].copy()

# Apply the change_datetime_type function to the filtered DataFrame
df_filtered['YearMonth'] = df_filtered['YearMonth'].apply(change_datetime_type)

print(df["YearMonth"].unique())

# # Filter based on month and sales rep, aggregate target and actual 
# df['filer_mtd'] = df['YearMonth'].dt.to_period('M')
# aggregated_df = df.groupby(['filer_mtd', 'SalesRep']).agg({'Target':'sum', 'Actual':'sum'}).reset_index()

# New column for percent 
# If target = 0 or NaN --> Percent = 100
# def percent(row):
#     if(row['Target'] == 0 or pd.isna(row['Target'])):
#         return 100
#     return (row['Actual']/row['Target']) * 100
# aggregated_df['Percent'] = aggregated_df.apply(percent, axis = 1)
# print(aggregated_df)

# # Filter out email that has ; 2 values, only take 1