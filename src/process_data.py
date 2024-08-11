import pandas as pd
import os
from datetime import datetime
import math 

country_name_mapping = {
    'kpi.OwnerId': 'kpi_tracker_userlevel[kpi.OwnerId]',
    'Name': 'kpi_tracker_userlevel[Name]',
    'AD_Group': 'Country',
}

hcp_mapping = {
    'kpi_tracker_userlevel[Name]':'Name',
    'kpi_tracker_useraccountlevel[account.Name]':'HCP_Name',
    'kpi_tracker_userlevel[KPI_Ref_Time]':'HCP_Month',
    "kpi_tracker_useraccountlevel[mc_cycle_plan_target.ZLG_Sales_Segment__c]":"HCP_Segment",
    "kpi_tracker_useraccountlevel[Compliance?]":"HCP_Compliance",
    "kpi_tracker_useraccountlevel[account.External_ID_vod__c]":"HCP_ID",
    "[Sumactual_MTD]":"HCP_Actual_Call",
    "[Sumtarget_MTD]":"HCP_Target_MTD",
    "[Sumtarget_QTD]":"HCP_Target_QTD"
}

general_mapping = {
    'kpi_tracker_userlevel[kpi.OwnerId]': 'ID',
    'kpi_tracker_userlevel[Name]': 'Name',
    'kpi_tracker_userlevel[UserName_Level1]': 'Manager_name',
    'kpi_tracker_userlevel[UserId_Level1]': 'Manager_id',
    '[KPI_ACT_MTD_CallRate]': 'Call_Rate_MTD',
    '[KPI_ACT_MTD_CallVolume]': 'Call_Volume_MTD',
    '[KPI_ACT_MTD_CallCompliance]': 'Call_Compliance_MTD',
    '[KPI_ACT_MTD_CallComplianceA]': 'Call_Compliance_A_MTD',
    '[Value_Qty_Transaction_Market]': 'Actual_Sales_MTD',
    '[Value_QTY_Target]': 'Target_MTD',
    '[v__Done]': '%Achievement_MTD',
    '[Gap]': 'Balance_MTD',
    '[QTD_Value_QTY_Transaction_Market]': 'Actual_Sales_QTD',
    '[QTD_Value_QTY_Target]': 'Target_QTD',
    '[QTD___Done]': '%Achievement_QTD',
    '[QTD_Gap]': 'Balance_QTD',
    '[KPI_ACT_QTD_CallRate]': 'Call_Rate_QTD',
    '[KPI_ACT_QTD_CallVolume]': 'Call_Volume_QTD',
    '[KPI_ACT_QTD_CallCompliance]': 'Call_Compliance_QTD',
    '[KPI_ACT_QTD_CallComplianceA]': 'Call_Compliance_A_QTD',
    'kpi_tracker_userlevel[Profile_Name_vod__c]':'Role',
    "[Summtd_event_count]":"Event_MTD",
    "[Sumqtd_event_count]":"Event_QTD",
    "[Sumytd_event_count]":"Event_YTD",
    "[Summtd_touchpoint_count]":"Touchpoint_MTD",
    "[Sumqtd_touchpoint_count]":"Touchpoint_QTD",
    "[Summtd_emailusercount]":"Email_Sent_MTD",
    "[Sumqtd_emailusercount]":"Email_Sent_QTD",
    "[Sumytd_emailusercount]":"Email_Sent_YTD",
    "[KPI_ACT_MTD_OpenRate]":"Mail_Open_Rate_MTD",
    "[KPI_ACT_QTD_OpenRate]":"Mail_Open_Rate_QTD",
    "[KPI_ACT_YTD_OpenRate]":"Mail_Open_Rate_YTD",
    "[KPI_ACT_MTD_ClickRate]":"Clickrate_MTD",
    "[KPI_ACT_QTD_ClickRate]":"Clickrate_QTD",
    "[KPI_ACT_YTD_ClickRate]":"Clickrate_YTD",
    "kpi_tracker_userlevel[Latest_Active_User]":"Active_User"}

product_mapping = {
    'REF_TIME[KPI_Ref_Time]':'Product_Month',
    'SplitRep_BQ[Product Group]':'Product_Group',
    "user[Name]": 'Name',
    "user[Id]":'ID',
    "[QTD_Value_QTY_Transaction_Market]":'Product_QTD',
    "[Value_Qty_Transaction_Market]":'Product_MTD'
}

def find_month():
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-01")
    print(formatted_time)
    return formatted_time

def get_current_month_year():
    # Get the current date
    now = datetime.now()
    # Format the date as YYYYMM
    formatted_date = now.strftime("%Y%m")
    return formatted_date

def merge_country():
    # Define the paths to the CSV files
    # path_name = get_current_month_year()
    path_name = 202406
    csv_file_1_path = f'data/raw/Country_Master_{path_name}.csv'
    csv_file_2_path = f'data/raw/Unity_Export_S360_{path_name}.csv'  

    # Read the CSV files into DataFrames
    df1 = pd.read_csv(csv_file_1_path)
    df2 = pd.read_csv(csv_file_2_path)

    # Merge the DataFrames on the common columns
    merged_df = pd.merge(df1, df2, on=["kpi_tracker_userlevel[kpi.OwnerId]","kpi_tracker_userlevel[Name]"])
    
    # Define the path to save the merged DataFrame
    output_file_path = f'data/raw/Country_Master_{path_name}.csv'

    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv(output_file_path, index=False)

    print(f"Merged CSV file successfully saved")

def merge_all():
    # Define the paths to the CSV files
    # path_name = get_current_month_year()
    path_name = 202406
    csv_file_1_path = f'data/raw/Unity_Export_MTDCall_{path_name}.csv'
    csv_file_2_path = f'data/raw/Unity_Export_S360_{path_name}.csv'  
    csv_file_3_path = 'data/merged/merged_qtd.csv'
    csv_file_4_path = f'data/raw/Unity_Export_Others_{path_name}.csv'
    csv_file_5_path = f'data/raw/Country_Master_{path_name}.csv'


    # Read the CSV files into DataFrames
    df1 = pd.read_csv(csv_file_1_path)
    df2 = pd.read_csv(csv_file_2_path)
    df3 = pd.read_csv(csv_file_3_path)
    df4 = pd.read_csv(csv_file_4_path)
    df5 = pd.read_csv(csv_file_5_path)

    # Merge the DataFrames on the common columns
    merged_df = pd.merge(df1, df2, on=["kpi_tracker_userlevel[kpi.OwnerId]","kpi_tracker_userlevel[Name]", "kpi_tracker_userlevel[UserName_Level1]","kpi_tracker_userlevel[UserId_Level1]"])
    merged_df = pd.merge(merged_df, df3, on=["kpi_tracker_userlevel[kpi.OwnerId]","kpi_tracker_userlevel[Name]", "kpi_tracker_userlevel[UserName_Level1]","kpi_tracker_userlevel[UserId_Level1]"])
    merged_df = pd.merge(merged_df, df4, on=["kpi_tracker_userlevel[kpi.OwnerId]","kpi_tracker_userlevel[Name]", "kpi_tracker_userlevel[UserName_Level1]","kpi_tracker_userlevel[UserId_Level1]"])
    merged_df = pd.merge(merged_df, df5, on=["kpi_tracker_userlevel[kpi.OwnerId]","kpi_tracker_userlevel[Name]"])

    # Define the path to save the merged DataFrame
    output_file_path = 'data/merged/output_merged.csv'

    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv(output_file_path, index=False)

    print(f"Merged CSV file successfully saved as {output_file_path}")

def merge_qtd():
    # path_name = get_current_month_year()
    path_name = 202406

    # Define the paths to the CSV files
    csv_files = [
        f'data/raw/Unity_Export_QTDCall_HKMMTWVN_{path_name}.csv',
        f'data/raw/Unity_Export_QTDCall_ID_{path_name}.csv',
        f'data/raw/Unity_Export_QTDCall_MYSGBNKH_{path_name}.csv',
        f'data/raw/Unity_Export_QTDCall_PHTH_{path_name}.csv'
    ]

    # List to hold DataFrames
    data_frames = []

    # Read each CSV file into a DataFrame and add it to the list
    for csv_file in csv_files:
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            data_frames.append(df)
        else:
            print(f"File not found: {csv_file}")
            exit(1)

    # Concatenate all DataFrames
    merged_df = pd.concat(data_frames, ignore_index=True)

    # Define the path to save the merged DataFrame
    output_file_path = 'data/merged/merged_qtd.csv'

    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv(output_file_path, index=False)

    print(f"Merged CSV file successfully saved as {output_file_path}")

def rename_csv_column(col_dict, csv_input, csv_output):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_input)

    # List the original column names
    original_column_names = df.columns.tolist()

    # Check if all keys in the mapping exist in the original columns
    missing_columns = [col for col in col_dict.keys() if col not in original_column_names]
    if missing_columns:
        print(f"Error: The following columns in the mapping are missing in the CSV: {missing_columns}")
        return

    # Rename the columns using the mapping
    df.rename(columns=col_dict, inplace=True)

    # Save the DataFrame with the new column names to a new CSV file
    df.to_csv(csv_output, index=False)
    print(f"{csv_output} successfully renamed")
    
def process_general():
    # Read the CSV file into a DataFrame
    df = pd.read_csv("data/processed/output_renamed.csv")

    # Process Role row
    def process_role(role):
        if isinstance(role, str) and role.startswith('ZLG_') and role.endswith('_CRM'):
            return role[4:-4]
        return None

    # Apply the process_role function to the Role column
    df['Role'] = df['Role'].apply(process_role)

    # Remove rows with None in the Role column or where Status is 'inactive'
    df = df[df['Role'].notnull() & (df['Active_User'].str.lower() != 'inactive')]


    # Save the DataFrame with the converted columns to a new CSV file
    df.to_csv("data/processed/output_processed.csv", index=False)
    print(f"DataFrame successfully saved with converted columns as data/processed/output_processed")

def process_product():
    df = pd.read_csv('data/raw/Unity_Export_Product_202406.csv')

    # Sort by 'Name' and then by 'Product_QTD' within each name group in descending order
    df_sorted = df.sort_values(by=['Name', 'Product_QTD'], ascending=[True, False])

    # Save the formatted and sorted DataFrame back to a CSV file
    df_sorted.to_csv('data/raw/Unity_Export_Product_202406.csv', index=False)
    print("Finished processing product")

def split_xlsx(file_path):
    excel_data = pd.ExcelFile(file_path)

    # Iterate through each sheet and save it as a CSV file
    for sheet_name in excel_data.sheet_names:
        # Read each sheet into a DataFrame
        df = pd.read_excel(excel_data, sheet_name=sheet_name)
        
        # Define the CSV file name
        csv_file_name = f"data/raw/{sheet_name}.csv"
        
        # Save the DataFrame to a CSV file
        df.to_csv(csv_file_name, index=False)
        
        print(f"Saved {sheet_name} as {csv_file_name}")

    print("All sheets have been saved as CSV files.")

def process_svt_unity():
    df = pd.read_csv('data/raw/SvT_Unity.csv')

    # Group using UserKey & yearmonth
    df_sorted = df.groupby(['UserKey_4Map', 'yearmonth'], as_index=False).agg({
        'Country': 'first',  # Retain the first value (assuming it's consistent)
        'SalesRep_Code': 'first',  # Retain the first value (assuming it's consistent)
        'salesrepemployeeid_z': 'first',  # Retain the first value (assuming it's consistent)
        'MTD Sales': 'sum',  # Sum the sales
        'MTD Target': 'sum'  # Sum the targets
    })

    # Create QTD Sales & Target by grouping UserKey, then finding sum of MTD Sales and MTD Target
    df_sorted['QTD Sales'] = df_sorted.groupby('UserKey_4Map')['MTD Sales'].transform('sum')
    df_sorted['QTD Target'] = df_sorted.groupby('UserKey_4Map')['MTD Target'].transform('sum')

    # Create MTD, QTD Balance by subtracting the columns
    # Neu Sales > Target thi Balance = 0 hay la mot gia tri am?
    df_sorted['MTD Balance'] = df_sorted['MTD Target'] - df_sorted['MTD Sales']
    df_sorted['QTD Balance'] = df_sorted['QTD Target'] - df_sorted['QTD Sales']

    # Create MTD, QTD % Achievement by divding the columns
    # Neu Target = 0 thi sao. Hien tai dang de 100%
    def calculate_achievement_mtd(row):
        if pd.isna(row['MTD Target']) or row['MTD Target'] == 0:
            if pd.isna(row['MTD Sales']) or row['MTD Sales'] == 0:
                return 0
            else:
                return 1  # 100% in decimal
        else:
            return row['MTD Sales'] / row['MTD Target']

    # Define the function to calculate %Achievement_QTD
    def calculate_achievement_qtd(row):
        if pd.isna(row['QTD Target']) or row['QTD Target'] == 0:
            if pd.isna(row['QTD Sales']) or row['QTD Sales'] == 0:
                return 0
            else:
                return 1  # 100% in decimal
        else:
            return row['QTD Sales'] / row['QTD Target']

    # Apply the functions to the DataFrame
    df_sorted['%Achievement_MTD'] = df_sorted.apply(calculate_achievement_mtd, axis=1)
    df_sorted['%Achievement_QTD'] = df_sorted.apply(calculate_achievement_qtd, axis=1)


    # Filter out other months
    filtered_df = df_sorted[df_sorted['yearmonth'] ==  find_month()]

    filtered_df.to_csv('data/raw/SvT_Unity_Processed.csv', index=False)
    print("Finished processing SvT Unity")


def process_product_unity():
    df = pd.read_csv('data/raw/Product_List_Unity.csv')

    # Group by yearmonth and UserKey_4Map
    grouped_df = df.groupby(['yearmonth', 'UserKey_4Map'], as_index=False).first()

    # Sort the DataFrame by 'MTD Sales' in descending order
    sorted_df = grouped_df.sort_values(by='MTD Sales', ascending=False)

    # QTD Sales 
    sorted_df['QTD Sales'] = sorted_df.groupby('UserKey_4Map')['MTD Sales'].transform('sum')

    # Filter out other months
    filtered_df = sorted_df[sorted_df['yearmonth'] ==  find_month()]

    filtered_df.to_csv('data/raw/Product_List_Unity_Processed.csv', index=False)
    print("Finished processing product")


def process_customer_unity():
    df = pd.read_csv('data/raw/Customer_List_Unity.csv')

    # Group by yearmonth and UserKey_4Map
    grouped_df = df.groupby(['yearmonth', 'UserKey_4Map'], as_index=False).first()

    # Sort the DataFrame by 'MTD Sales' in descending order
    sorted_df = grouped_df.sort_values(by='MTD Sales', ascending=False)

    # QTD Sales 
    sorted_df['QTD Sales'] = sorted_df.groupby('UserKey_4Map')['MTD Sales'].transform('sum')

    # Filter out other months
    filtered_df = sorted_df[sorted_df['yearmonth'] ==  find_month()]

    filtered_df.to_csv('data/raw/Customer_List_Unity_Processed.csv', index=False)
    print("Finished processing Customer")


"""
Define flow: 
1. Download files in sharepoint
2. Rename column in country 
"""
if __name__ == "__main__":
    # split_xlsx("data/raw/Sales360_Unity.xlsx")
    process_product_unity()
    process_svt_unity()
    process_customer_unity()
    # rename_csv_column(country_name_mapping,"data/raw/Country_Master_202406.csv","data/raw/Country_Master_202406.csv")
    # merge_qtd()
    # merge_all()
    # rename_csv_column(hcp_mapping,"data/raw/Unity_Export_HCP202407.csv","data/raw/Unity_Export_HCP202407.csv")
    # rename_csv_column(product_mapping,"data/raw/Unity_Export_Product_202406.csv","data/raw/Unity_Export_Product_202406.csv")
    # rename_csv_column(general_mapping,"data/merged/output_merged.csv","data/processed/output_renamed.csv")
    # process_general()
    # process_product()
