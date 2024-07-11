from datetime import datetime, date, timezone
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Read csv file
df = pd.read_csv('./data/Unity_data.csv', encoding='latin1')
"""
Overview
1. Aggregate data from 2 dashboards into a single CSV file. May involve data cleaning and preprocessing. 
Create new columns for targetted data (Target, Actual, Product groups, etc.).
2. Create visualization using pandas, matplotlib, and seaborn to visualize each chart. 
3. Create dashboard using Dash or Streamlit
4. Send email using smtplib 

Look out for pipelining process 
"""

# Clean data: Only keep rows with valid month and year
validMonthYear = ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06', '2024-07',
 '2024-08', '2024-09', '2024-10', '2024-11', '2024-12']

df['KPI_Ref_Time'] = df['KPI_Ref_Time'].astype('string')
df = df[df['KPI_Ref_Time'].isin(validMonthYear)]

# Function change YearMonth into DateTime data type
def change_datetime_type(date_string:str) -> datetime:
    '''
    Type cast YearMonth column from string type to datetime type
        Parameters: date_string (str): YearMonth in string type
        Returns: date_string (datetime): YearMonth in datetime type
    '''
    date_format = "%Y-%m"
    return datetime.strptime(date_string, date_format)

df["KPI_Ref_Time"] = df['KPI_Ref_Time'].apply(change_datetime_type)

# # Filter based on month and sales rep, aggregate target and actual 
df['filter_mtd'] = df['KPI_Ref_Time'].dt.to_period('M')
aggregated_df = df.groupby(['filter_mtd', 'SplitRep_salesrepcode_z']).agg({'Target':'sum', 'Actual':'sum'}).reset_index()

# # New column for percent 
# # If target = 0 or NaN --> Percent = 100
def percent(row):
    target = row['Target']
    actual = row['Actual']
    if pd.isna(target) or target == 0:
        return 100
    return (actual / target) * 100

# aggregated_df['Percent'] = aggregated_df.apply(percent, axis = 1)
# # Suppress scientific notation 
aggregated_df['Target'] = aggregated_df['Target'].apply('{:.2f}'.format).astype(float)
aggregated_df['Percent'] = aggregated_df['Percent'].apply('{:.2f}'.format).astype(float)
print(aggregated_df.dtypes)

# Visualization

