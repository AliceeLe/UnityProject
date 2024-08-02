import pandas as pd
import os
from datetime import datetime

def get_current_month_year():
    # Get the current date
    now = datetime.now()
    # Format the date as YYYYMM
    formatted_date = now.strftime("%Y%m")
    return formatted_date

# Example usage
current_month_year = get_current_month_year()
print(current_month_year)


def merge_all():
    # Define the paths to the CSV files
    # path_name = get_current_month_year()
    path_name = 202406
    csv_file_1_path = f'data/raw/Unity_Export_MTDCall_{path_name}.csv'
    csv_file_2_path = f'data/raw/Unity_Export_S360_{path_name}.csv'  
    csv_file_3_path = 'data/merged/merged_qtd.csv'
    csv_file_4_path = 'data/raw/Unity_Export_Others_202406.csv'


    # Read the CSV files into DataFrames
    df1 = pd.read_csv(csv_file_1_path)
    df2 = pd.read_csv(csv_file_2_path)
    df3 = pd.read_csv(csv_file_3_path)
    df4 = pd.read_csv(csv_file_4_path)

    # Merge the DataFrames on the common columns
    merged_df = pd.merge(df1, df2, on=["kpi_tracker_userlevel[kpi.OwnerId]","kpi_tracker_userlevel[Name]", "kpi_tracker_userlevel[UserName_Level1]","kpi_tracker_userlevel[UserId_Level1]"])
    merged_df = pd.merge(merged_df, df3, on=["kpi_tracker_userlevel[kpi.OwnerId]","kpi_tracker_userlevel[Name]", "kpi_tracker_userlevel[UserName_Level1]","kpi_tracker_userlevel[UserId_Level1]"])
    merged_df = pd.merge(merged_df, df4, on=["kpi_tracker_userlevel[kpi.OwnerId]","kpi_tracker_userlevel[Name]", "kpi_tracker_userlevel[UserName_Level1]","kpi_tracker_userlevel[UserId_Level1]"])

    # Define the path to save the merged DataFrame
    output_file_path = 'data/merged/output.csv'

    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv(output_file_path, index=False)

    print(f"Merged CSV file successfully saved as {output_file_path}")

def merge_qtd():
    # path_name = get_current_month_year()
    path_name = 202406

    # Define the paths to the CSV files
    csv_files = [
        f'data/Unity_Export_QTDCall_HKMMTWVN_{path_name}.csv',
        f'data/Unity_Export_QTDCall_ID_{path_name}.csv',
        f'data/Unity_Export_QTDCall_MYSGBNKH_{path_name}.csv',
        f'data/Unity_Export_QTDCall_PHTH_{path_name}.csv'
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

# def rename_columns(csv_file_path, new_column_names, output_file_path):
#     # Read the CSV file into a DataFrame
#     df = pd.read_csv(csv_file_path)

#     df = df.round(2)

#     # List the original column names
#     original_column_names = df.columns.tolist()
#     print(f"Original column names: {original_column_names}")

#     # Check if the number of new column names matches the number of original column names
#     if len(new_column_names) != len(original_column_names):
#         print("Error: The number of new column names must match the number of original column names.")
#         return

#     # Rename the columns
#     df.columns = new_column_names

#     # List the new column names
#     print(f"New column names: {df.columns.tolist()}")

#     # Save the DataFrame with the new column names to a new CSV file
#     df.to_csv(output_file_path, index=False)
#     print(f"DataFrame successfully saved with new column names as {output_file_path}")


# # Define the paths to the input and output CSV files
# input_csv_file_path = 'data/Unity_sample.csv'
# output_csv_file_path = 'data/Sample_renamed.csv'

# # Define the new column names
# new_column_names = ['ID', 'Name', 'Manager_name', 'Manager_id', 'Call_Rate_MTD', 'Call_Volume_MTD', 'Call_Compliance_MTD', 'Call_Compliance_A_MTD', 'Actual_Sales_MTD', 'Target_MTD', '%Achievement_MTD', 'Balance_MTD', 'Actual_Sales_QTD', 'Target_QTD', '%Achievement_QTD', 'Balance_QTD', 'Call_Rate_QTD', 'Call_Volume_QTD', 'Call_Compliance_QTD', 'Call_Compliance_A_QTD', 'Email']  # Replace with your new column names


def rename_columns(column_name_mapping):
    # Read the CSV file into a DataFrame
    df = pd.read_csv("data/merged/output.csv")

    df = df.round(2)

    # List the original column names
    original_column_names = df.columns.tolist()

    # Check if all keys in the mapping exist in the original columns
    missing_columns = [col for col in column_name_mapping.keys() if col not in original_column_names]
    if missing_columns:
        print(f"Error: The following columns in the mapping are missing in the CSV: {missing_columns}")
        return

    # Rename the columns using the mapping
    df.rename(columns=column_name_mapping, inplace=True)

    # Save the DataFrame with the new column names to a new CSV file
    df.to_csv("data/processed/output_renamed.csv", index=False)
    print(f"DataFrame successfully saved with new column names as output_renamed.csv")


# Define the mapping from old column names to new column names
column_name_mapping = {
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

def format_thousand(value):
    """
    This function takes a float or integer value, removes the decimal points,
    and adds commas as thousand separators.
    """
    try:
        # Convert the number to an integer (this removes the decimal points)
        int_value = int(value)
        # Format the number with commas as thousand separators
        formatted_value = f"{int_value:,}"
        return formatted_value
    except (ValueError, TypeError):
        return value  # Return the original value if conversion fails
    
def process_data():
    # Read the CSV file into a DataFrame
    df = pd.read_csv("data/processed/output_renamed.csv")

    columns_percent = ['%Achievement_MTD', '%Achievement_QTD','Call_Volume_MTD','Call_Volume_QTD','Call_Compliance_MTD','Call_Compliance_QTD','Call_Compliance_A_MTD','Call_Compliance_A_QTD',"Mail_Open_Rate_MTD","Mail_Open_Rate_QTD","Mail_Open_Rate_YTD","Clickrate_MTD","Clickrate_QTD","Clickrate_YTD"]
    columns_thousand = ['Target_MTD','Target_QTD','Actual_Sales_MTD','Actual_Sales_QTD','Balance_MTD','Balance_QTD','Email_Sent_MTD','Email_Sent_QTD','Email_Sent_YTD']
    # Convert specified columns from decimal format to percentage format
    for column in columns_percent:
        if column in df.columns:
            df[column] = df[column].apply(lambda x: f"{int(round(x * 100))}%" if pd.notnull(x) else "")
        else:
            print(f"Warning: Column '{column}' not found in the CSV file.")

    # Process rows with thousands
    for column in columns_thousand:
        if column in df.columns:
            df[column] = df[column].apply(format_thousand)
        else:
            print(f"Warning: Column '{column}' not found in the CSV file.")

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


# merge_qtd()
# merge_all()
rename_columns(column_name_mapping)
process_data()


