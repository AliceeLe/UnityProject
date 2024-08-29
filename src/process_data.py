import pandas as pd
import os
from datetime import datetime
import math 

hcp_mapping = {
    'kpi_tracker_userlevel[Name]':'Owner_Name',
    "kpi_tracker_userlevel[kpi.OwnerId]":"Owner_Id",
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
    "summary[kpi.OwnerId]":"Owner_Id",
    "summary[Name]":"Owner_Name",
    "summary[Profile_Name_vod__c]":"Role",

    "[Summtd_event_count]":"Event_MTD",
    "[Sumqtd_event_count]":"Event_QTD",
    "[Sumytd_event_count]":"Event_YTD",
    "[Summtd_touchpoint_count]":"Touchpoint_MTD",
    "[Sumqtd_touchpoint_count]":"Touchpoint_QTD",
    "[Sumytd_touchpoint_count]":"Touchpoint_YTD",
    "[Summtd_emailusercount]":"Email_Sent_MTD",
    "[Sumqtd_emailusercount]":"Email_Sent_QTD",
    "[Sumytd_emailusercount]":"Email_Sent_YTD",

    "[SumKPI_ACT_MTD_CoachingDays_M]":"Coaching_MTD",
    "[SumKPI_ACT_QTD_CoachingDays_M]":"Coaching_QTD",
    "[SumKPI_ACT_YTD_CoachingDays_M]":"Coaching_YTD",

    "[SumKPI_ACT_MTD_CallRate]":"Call_Rate_MTD",
    "[SumKPI_ACT_QTD_CallRate]":"Call_Rate_QTD",
    "[SumKPI_ACT_YTD_CallRate]":"Call_Rate_YTD",

    "[SumKPI_ACT_QTD_CallVolume]":"Call_Volume_QTD",
    "[SumKPI_ACT_YTD_CallVolume]":"Call_Volume_YTD",
    "[SumKPI_ACT_MTD_CallVolume]":"Call_Volume_MTD",

    "[SumKPI_ACT_MTD_CallCompliance]":"Call_Compliance_MTD",
    "[SumKPI_ACT_YTD_CallCompliance]":"Call_Compliance_YTD",
    "[SumKPI_ACT_QTD_CallCompliance]":"Call_Compliance_QTD",

    "[SumKPI_ACT_MTD_CallComplianceA]":"Call_Compliance_A_MTD",
    "[SumKPI_ACT_YTD_CallComplianceA]":"Call_Compliance_A_YTD",
    "[SumKPI_ACT_QTD_CallComplianceA]":"Call_Compliance_A_QTD",

    "[SumKPI_ACT_MTD_ClickRate]":"Clickrate_MTD",
    "[SumKPI_ACT_QTD_ClickRate]":"Clickrate_QTD",
    "[SumKPI_ACT_YTD_ClickRate]":"Clickrate_YTD",
    "[SumKPI_ACT_MTD_OpenRate]":"Mail_Open_Rate_MTD",
    "[SumKPI_ACT_QTD_OpenRate]":"Mail_Open_Rate_QTD",
    "[SumKPI_ACT_YTD_OpenRate]":"Mail_Open_Rate_YTD",
    }

contact_mapping = {
    "user[userrole.Name]": "UserKey_4Map",
    "kpi_tracker_userlevel[Username]": "Owner_Email",
    "kpi_tracker_userlevel[Name]":"Owner_Name",
    "kpi_tracker_userlevel[Profile_Name_vod__c]":"Role",
    "kpi_tracker_userlevel[UserName_Level1]":"Manager_Name",
    "kpi_tracker_userlevel[UserId_Level1]":"Manager_Id",
    "kpi_tracker_userlevel[kpi.OwnerId]":"Owner_Id",
    "kpi_tracker_userlevel[Userid_Level1.Username]":"Manager_Email",
    "kpi_tracker_userlevel[Latest_Active_User]":"Status"
}

manager_mapping = {
    "summary2[UserId_Level1]":"Manager_Id",
    "summary2[UserName_Level1]":"Manager_Name",
    "summary2[UserProfileName_Level1]":"Role",

    "[SumValue_Qty_Transaction_Market]":"Team_Sales_MTD",
    "[SumValue_QTY_Target]":"Team_Target_MTD",
    "[SumGap]":"Team_Balance_MTD",
    "[Sumv__Done]":"%Team_Achievement_MTD",
    "[SumQTD_Value_Qty_Transaction_Market]":"Team_Sales_QTD",
    "[SumQTD_Value_QTY_Target]":"Team_Target_QTD",
    "[SumQTD_Gap]":"Team_Balance_QTD",
    "[SumQTD___Done]":"%Team_Achievement_QTD",

    "[SumKPI_ACT_MTD_CallRate]":"Team_Call_Rate_MTD",
    "[SumKPI_ACT_QTD_CallRate]":"Team_Call_Rate_QTD",
    "[SumKPI_ACT_YTD_CallRate]":"Team_Call_Rate_YTD",
    "[SumKPI_ACT_MTD_CallVolume]":"Team_Call_Volume_MTD",
    "[SumKPI_ACT_QTD_CallVolume]":"Team_Call_Volume_QTD",
    "[SumKPI_ACT_YTD_CallVolume]":"Team_Call_Volume_YTD",
    "[SumKPI_ACT_MTD_CallCompliance]":"Team_Compliance_MTD",
    "[SumKPI_ACT_QTD_CallCompliance]":"Team_Compliance_QTD",
    "[SumKPI_ACT_YTD_CallCompliance]":"Team_Compliance_YTD",
    "[SumKPI_ACT_MTD_CallComplianceA]":"Team_Compliance_A_MTD",
    "[SumKPI_ACT_QTD_CallComplianceA]":"Team_Compliance_A_QTD",
    "[SumKPI_ACT_YTD_CallComplianceA]":"Team_Compliance_A_YTD",

    "[Summtd_emailusercount]":"Team_Email_Sent_MTD",
    "[Sumqtd_emailusercount]":"Team_Email_Sent_QTD",
    "[Sumytd_emailusercount]":"Team_Email_Sent_YTD",
    "[Summtd_event_count]":"Team_Event_MTD",
    "[Sumqtd_event_count]":"Team_Event_QTD",
    "[Sumytd_event_count]":"Team_Event_YTD",
    "[Summtd_touchpoint_count]":"Team_Touchpoing_MTD",
    "[Sumqtd_touchpoint_count]":"Team_Touchpoing_QTD",
    "[Sumytd_touchpoint_count]":"Team_Touchpoing_YTD",
    "[SumKPI_ACT_MTD_ClickRate]":"Team_Clickrate_MTD",
    "[SumKPI_ACT_QTD_ClickRate]":"Team_Clickrate_QTD",
    "[SumKPI_ACT_YTD_ClickRate]":"Team_Clickrate_YTD",
    "[SumKPI_ACT_MTD_OpenRate]":"Team_Open_Rate_MTD",
    "[SumKPI_ACT_QTD_OpenRate]":"Team_Open_Rate_QTD",
    "[SumKPI_ACT_YTD_OpenRate]":"Team_Open_Rate_YTD",
    "[SumKPI_ACT_QTD_CoachingDays_M]":"Team_Coaching_QTD",
    "[SumKPI_ACT_YTD_CoachingDays_M]":"Team_Coaching_YTD",
    "[SumKPI_ACT_MTD_CoachingDays_M]":"Team_Coaching_MTD"
}

columns_numeric_general = [
"Sales_MTD",
"Target_MTD",
"Sales_QTD",
"Target_QTD",
"Balance_MTD",
"Balance_QTD",
"%Achievement_MTD",
"%Achievement_QTD",
"Call_Rate_MTD",
"Call_Rate_QTD",
"Call_Rate_YTD",
"Call_Volume_MTD",
"Call_Volume_QTD",
"Call_Compliance_MTD",
"Call_Compliance_QTD",
"Call_Compliance_A_MTD",
"Call_Compliance_A_QTD",
"Email_Sent_MTD",
"Email_Sent_QTD",
"Email_Sent_YTD",
"Event_MTD",
"Event_QTD",
"Event_YTD",
"Touchpoint_MTD",
"Touchpoint_QTD",
"Touchpoint_YTD",
"Clickrate_MTD",
"Clickrate_QTD",
"Clickrate_YTD",
"Mail_Open_Rate_MTD",
"Mail_Open_Rate_QTD",
"Mail_Open_Rate_YTD",
"Coaching_QTD",
"Coaching_YTD",
"Call_Volume_YTD",
"Call_Compliance_YTD",
"Call_Compliance_A_YTD",
"Coaching_MTD",
"Team_Sales_MTD",
"Team_Sales_QTD",
"Team_Target_MTD",
"Team_Target_QTD",
"%Team_Achievement_MTD",
"%Team_Achievement_QTD"
]

columns_numeric_hcp = [
    "HCP_Actual_Call",
    "HCP_Target_MTD",
    "HCP_Target_QTD",
]

columns_numeric_customer = [
    "Customer_MTD",
    "Customer_QTD",
    "Customer_Total_MTD",
    "Customer_Total_QTD",
    "Customer_Max_MTD",
    "Customer_Max_QTD",
    "Customer_Percent_MTD",
    "Customer_Percent_QTD",
]

columns_numeric_product = [
    "Product_MTD",
    "Product_QTD",
    "Product_Total_MTD",
    "Product_Total_QTD",
    "Product_Max_MTD",
    "Product_Max_QTD",
    "Product_Percent_MTD",
    "Product_Percent_QTD",
]



def find_month():
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-01")
    print(formatted_time)
    return formatted_time

def rename_csv_column(col_dict,
 csv_input, csv_output):
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

    col_dict = {
        "MTD Sales": "Sales_MTD",
        "MTD Target": "Target_MTD"
    }

    # Rename the columns using the mapping
    df.rename(columns=col_dict, inplace=True)

    # Group using UserKey & yearmonth
    df_sorted = df.groupby(['UserKey_4Map', 'yearmonth'], as_index=False).agg({
        'Country': 'first',  # Retain the first value (assuming it's consistent)
        'SalesRep_Code': 'first',  # Retain the first value (assuming it's consistent)
        'salesrepemployeeid_z': 'first',  # Retain the first value (assuming it's consistent)
        'Sales_MTD': 'sum',  # Sum the sales
        'Target_MTD': 'sum'  # Sum the targets
    })

    # Create QTD Sales & Target by grouping UserKey, then finding sum of Sales_MTD and Target_MTD
    df_sorted['Sales_QTD'] = df_sorted.groupby('UserKey_4Map')['Sales_MTD'].transform('sum')
    df_sorted['Target_QTD'] = df_sorted.groupby('UserKey_4Map')['Target_MTD'].transform('sum')

    # Create MTD, QTD Balance by subtracting the columns
    df_sorted['Balance_MTD'] =  df_sorted['Sales_MTD'] - df_sorted['Target_MTD']
    df_sorted['Balance_QTD'] =  df_sorted['Sales_QTD'] - df_sorted['Target_QTD'] 

    # Create MTD, QTD % Achievement by divding the columns
    # Neu Target = 0 thi sao. Hien tai dang de 100%
    def calculate_achievement_mtd(row):
        if pd.isna(row['Target_MTD']) or row['Target_MTD'] == 0:
            if pd.isna(row['Sales_MTD']) or row['Sales_MTD'] == 0:
                return 0
            else:
                return 1  # 100% in decimal
        else:
            return row['Sales_MTD'] / row['Target_MTD']

    # Define the function to calculate %Achievement_QTD
    def calculate_achievement_qtd(row):
        if pd.isna(row['Target_QTD']) or row['Target_QTD'] == 0:
            if pd.isna(row['Sales_QTD']) or row['Sales_QTD'] == 0:
                return 0
            else:
                return 1  # 100% in decimal
        else:
            return row['Sales_QTD'] / row['Target_QTD']

    # Apply the functions to the DataFrame
    df_sorted['%Achievement_MTD'] = df_sorted.apply(calculate_achievement_mtd, axis=1)
    df_sorted['%Achievement_QTD'] = df_sorted.apply(calculate_achievement_qtd, axis=1)


    # Filter out other months
    filtered_df = df_sorted[df_sorted['yearmonth'] ==  find_month()]

    filtered_df.to_csv('data/processed/SvT_Unity_Processed.csv', index=False)
    print("Finished processing SvT Unity")

def process_product_unity():
    df = pd.read_csv('data/raw/Product_List_Unity.csv')

    col_dict = {
        "MTD Sales": "Product_MTD",
    }

    # Rename the columns using the mapping
    df.rename(columns=col_dict, inplace=True)

    # Sort the DataFrame by 'MTD Sales' in descending order
    sorted_df = df.sort_values(by=['UserKey_4Map','Product_Group_Use','Product_MTD'], ascending=False)

    # Filter out rows if Product_MTD is NaN or 0
    # Drop rows where Product_MTD is NaN
    filtered_df = sorted_df.dropna(subset=['Product_MTD'])

    # Filter out rows where Product_MTD is 0
    filtered_df = filtered_df[filtered_df['Product_MTD'] != 0]

    # QTD Sales 
    filtered_df['Product_QTD'] = filtered_df.groupby(['UserKey_4Map','Product_Group_Use'])['Product_MTD'].transform('sum')

    filtered_df['Product_Total_MTD'] = filtered_df.groupby(['UserKey_4Map','yearmonth'])['Product_MTD'].transform('sum')
    filtered_df['Product_Total_QTD'] = filtered_df.groupby('UserKey_4Map')['Product_MTD'].transform('sum')

    filtered_df['Product_Max_MTD'] = filtered_df.groupby(['UserKey_4Map','yearmonth'])['Product_MTD'].transform('max')
    filtered_df['Product_Max_QTD'] = filtered_df.groupby('UserKey_4Map')['Product_QTD'].transform('max')

    def calculate_percent_mtd(row):
        if pd.isna(row['Product_Max_MTD']) or row['Product_Max_MTD'] == 0:
            if pd.isna(row['Product_MTD']) or row['Product_MTD'] == 0:
                return 0
            else:
                return 1  # 100% in decimal
        else:
            percent_mtd = row['Product_MTD'] / row['Product_Max_MTD']
            if percent_mtd < 0:
                return 0
            else:
                return percent_mtd

    def calculate_percent_qtd(row):
        if pd.isna(row['Product_Max_QTD']) or row['Product_Max_QTD'] == 0:
            if pd.isna(row['Product_QTD']) or row['Product_QTD'] == 0:
                return 0
            else:
                return 1  # 100% in decimal
        else:
            percent_qtd = row['Product_QTD'] / row['Product_Max_QTD']
            if percent_qtd < 0:
                return 0
            else:
                return percent_qtd

    filtered_df['Product_Percent_MTD'] = filtered_df.apply(calculate_percent_mtd, axis=1)
    filtered_df['Product_Percent_QTD'] = filtered_df.apply(calculate_percent_qtd, axis=1)

    # Sort the DataFrame by 'MTD Sales' in descending order
    filtered_df = filtered_df.sort_values(by=['UserKey_4Map','Product_QTD'], ascending=False)

    # Filter out other months
    filtered_month_df = filtered_df[filtered_df['yearmonth'] ==  find_month()]

    # Filter out NaN value to be 0
    filtered_month_df.loc[:, columns_numeric_product] = filtered_month_df.loc[:, columns_numeric_product].fillna(0)

    filtered_month_df.to_csv('data/processed/Product_List_Unity_Processed.csv', index=False)
    
    print("Finished processing product")

def process_customer_unity():
    df = pd.read_csv('data/raw/Customer_List_Unity.csv')

    col_dict = {
        "MTD Sales": "Customer_MTD",
    }

    # Rename the columns using the mapping
    df.rename(columns=col_dict, inplace=True)

    df['Customer_Name'] = df['Customer_Name'].str.strip()

    # Sort the DataFrame by 'MTD Sales' in descending order
    sorted_df = df.sort_values(by=['UserKey_4Map','j_soldtocustomercode','Customer_MTD'], ascending=False)

    # Filter out rows if MTD is NaN or 0
        # Drop rows where Customer_MTD is NaN
    filtered_df = sorted_df.dropna(subset=['Customer_MTD'])

    # Filter out rows where Customer_MTD is 0
    filtered_df = filtered_df[filtered_df['Customer_MTD'] != 0]

    # QTD Sales 
    filtered_df['Customer_QTD'] = filtered_df.groupby(['UserKey_4Map','j_soldtocustomercode'])['Customer_MTD'].transform('sum')

    filtered_df['Customer_Total_MTD'] = filtered_df.groupby(['UserKey_4Map','yearmonth'])['Customer_MTD'].transform('sum')
    filtered_df['Customer_Total_QTD'] = filtered_df.groupby('UserKey_4Map')['Customer_MTD'].transform('sum')

    filtered_df['Customer_Max_MTD'] = filtered_df.groupby(['UserKey_4Map','yearmonth'])['Customer_MTD'].transform('max')
    filtered_df['Customer_Max_QTD'] = filtered_df.groupby('UserKey_4Map')['Customer_QTD'].transform('max')

    def calculate_percent_mtd(row):
        if pd.isna(row['Customer_Max_MTD']) or row['Customer_Max_MTD'] == 0:
            if pd.isna(row['Customer_MTD']) or row['Customer_MTD'] == 0:
                return 0
            else:
                return 1  # 100% in decimal
        else:
            percent_mtd = row['Customer_MTD'] / row['Customer_Max_MTD']
            if percent_mtd < 0:
                return 0
            else:
                return percent_mtd


    def calculate_percent_qtd(row):
        if pd.isna(row['Customer_Max_QTD']) or row['Customer_Max_QTD'] == 0:
            if pd.isna(row['Customer_QTD']) or row['Customer_QTD'] == 0:
                return 0
            else:
                return 1  # 100% in decimal
        else:
            percent_qtd = row['Customer_QTD'] / row['Customer_Max_QTD']
            if percent_qtd < 0:
                return 0
            else:
                return percent_qtd

    filtered_df['Customer_Percent_MTD'] = filtered_df.apply(calculate_percent_mtd, axis=1)
    filtered_df['Customer_Percent_QTD'] = filtered_df.apply(calculate_percent_qtd, axis=1)

    filtered_df = filtered_df.sort_values(by=['UserKey_4Map','Customer_QTD'], ascending=False)

    # Filter out other months
    filtered_month_df = filtered_df[filtered_df['yearmonth'] ==  find_month()]

    # Filter out NaN value to be 0
    filtered_month_df.loc[:, columns_numeric_customer] = filtered_month_df.loc[:, columns_numeric_customer].fillna(0)

    filtered_month_df.to_csv('data/processed/Customer_List_Unity_Processed.csv', index=False)
    print("Finished processing Customer")

def process_general_unity():
    df_svt = pd.read_csv('data/processed/SvT_Unity_Processed.csv')
    df_contact = pd.read_csv('data/raw/Unity_Export_Others.csv')
    df_kpi = pd.read_csv('data/raw/Unity_Export.csv')

    columns_to_delete = [
    "summary[KPI_Ref_Time]",
    '[SumValue_Qty_Transaction_Market]',
    '[SumValue_QTY_Target]',
    '[SumGap]',
    '[Sumv__Done]',
    '[SumQTD_Value_Qty_Transaction_Market]',
    '[SumQTD_Value_QTY_Target]',
    '[SumQTD_Gap]',
    '[SumQTD___Done]'
    ]

    # Rename the columns using the mapping
    df_contact.rename(columns=contact_mapping, inplace=True)
    df_contact.to_csv('data/processed/Unity_Export_Others_Processed.csv', index=False)

    df_kpi = df_kpi.drop(columns=columns_to_delete)
    df_kpi.rename(columns=general_mapping, inplace=True)
    df_kpi.to_csv('data/processed/Unity_Export_Processed.csv', index=False)

    # Merge the DataFrames on the common columns
    merged_df = pd.merge(df_svt, df_contact, on=["UserKey_4Map"])
    merged_df = pd.merge(merged_df, df_kpi, on=["Owner_Name", "Owner_Id", "Role"])

    # Group using Manager_Id
    # Create QTD Sales & Target by grouping UserKey, then finding sum of Sales_MTD and Target_MTD
    merged_df['Team_Sales_MTD'] = merged_df.groupby('Manager_Id')['Sales_MTD'].transform('sum')
    merged_df['Team_Sales_QTD'] = merged_df.groupby('Manager_Id')['Sales_QTD'].transform('sum')
    merged_df['Team_Target_MTD'] = merged_df.groupby('Manager_Id')['Target_MTD'].transform('sum')
    merged_df['Team_Target_QTD'] = merged_df.groupby('Manager_Id')['Target_QTD'].transform('sum')

    # Neu Target = 0 thi sao. Hien tai dang de 100%
    def calculate_achievement_mtd(row):
        if pd.isna(row['Team_Target_MTD']) or row['Team_Target_MTD'] == 0:
            if pd.isna(row['Team_Sales_MTD']) or row['Team_Sales_MTD'] == 0:
                return 0
            else:
                return 1  # 100% in decimal
        else:
            return row['Team_Sales_MTD'] / row['Team_Target_MTD']

    # Define the function to calculate %Achievement_QTD
    def calculate_achievement_qtd(row):
        if pd.isna(row['Team_Target_QTD']) or row['Team_Target_QTD'] == 0:
            if pd.isna(row['Team_Sales_QTD']) or row['Team_Sales_QTD'] == 0:
                return 0
            else:
                return 1  # 100% in decimal
        else:
            return row['Team_Sales_QTD'] / row['Team_Target_QTD']

    # Apply the functions to the DataFrame
    merged_df['%Team_Achievement_MTD'] = merged_df.apply(calculate_achievement_mtd, axis=1)
    merged_df['%Team_Achievement_QTD'] = merged_df.apply(calculate_achievement_qtd, axis=1)
    merged_df = merged_df[(merged_df['Status'].str.lower() != 'inactive')]

    # convert numeric values into 0
    merged_df.loc[:, columns_numeric_general] = merged_df.loc[:, columns_numeric_general].fillna(0)

    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv("data/output/general.csv", index=False)

def process_hcp():
    rename_csv_column(hcp_mapping,"data/raw/Unity_Export_HCP.csv", "data/processed/hcp_processed.csv")
    add_manager_id_col("data/processed/hcp_processed.csv", "Owner_Name", "data/processed/hcp_processed.csv")

    df = pd.read_csv("data/processed/hcp_processed.csv")

    def calculate_rate(row):
        if pd.isna(row['HCP_Target_MTD']) or row['HCP_Target_MTD'] == 0:
            if pd.isna(row['HCP_Actual_Call']) or row['HCP_Actual_Call'] == 0:
                return 0
            else:
                return 1  # 100% in decimal
        else:
            percent_qtd = row['HCP_Actual_Call'] / row['HCP_Target_MTD']
            if percent_qtd < 0:
                return 0
            else:
                return percent_qtd

    df['Rate'] = df.apply(calculate_rate, axis=1)

    # Set HCP_Segment as a categorical type with a custom order
    segment_order = ['A', 'B', 'C']
    df['HCP_Segment'] = pd.Categorical(df['HCP_Segment'], categories=segment_order, ordered=True)

    # Sort the DataFrame first by 'HCP_Segment' and then by 'Rate' in descending order
    df = df.sort_values(by=['HCP_Segment', 'Rate'], ascending=[True, False])

    df.loc[:, columns_numeric_hcp] = df.loc[:, columns_numeric_hcp].fillna(0)

    df.to_csv("data/processed/hcp_processed.csv", index=False)
    print("Finished processing HCP")


def add_manager_id_col(input_csv, col_merged_by, output_csv):
    df_input = pd.read_csv(input_csv)
    df_manager = pd.read_csv("data/output/general.csv")

    result = df_input.merge(df_manager[[col_merged_by, 'Manager_Id']], on=col_merged_by, how='inner')

    result.to_csv(output_csv, index=False)


def create_sample_csv(email='vtvinh@zuelligpharma.com'):
    # Load the CSV file into a DataFrame
    df = pd.read_csv("data/output/general.csv")
    
    # Group by 'Country' and select the first 5 rows for each country
    df_selected = df.groupby('Country').head(5).reset_index(drop=True)
    
    # Add a new column 'Email' with the specified email address
    df_selected['Owner_Email'] = email
    
    df_selected.to_csv("data/output/sample.csv", index=False)

    # # Load the CSV file into a DataFrame
    # df = pd.read_csv("data/output/general_manager.csv")
    
    # # Group by 'Country' and select the first 5 rows for each country
    # df_selected = df.groupby('Country').head(5).reset_index(drop=True)
    
    # # Add a new column 'Email' with the specified email address
    # df_selected['Manager_Email'] = email
    
    # df_selected.to_csv("data/output/sample_manager.csv", index=False)
    
def process_manager():
    rename_csv_column(manager_mapping, "data/raw/Unity_Export_Manager.csv", "data/processed/Manager_Processed.csv")

    df_manager = pd.read_csv("data/processed/Manager_Processed.csv")
    df_manager = df_manager.drop(columns="summary2[KPI_Ref_Time]")

    df_general = pd.read_csv("data/output/general.csv")
    df_manager_contacts = df_general[['Manager_Id', 'Manager_Email', 'Country']]

    # Drop any duplicates, if needed
    df_manager_contacts = df_manager_contacts.drop_duplicates()

    merged_df = pd.merge(df_manager, df_manager_contacts, on=['Manager_Id'])

    merged_df.to_csv("data/output/general_manager.csv", index=False)



def final_process():
    # Split Sales360_Unity into 3 csv files: SvT, Product, Customer 
    split_xlsx("data/raw/Sales360_Unity.xlsx")

    # # Process 3 csv files: SvT, Product, Customer: Create columns for QTD
    process_product_unity()
    process_svt_unity()
    process_customer_unity()

    # Merge info about manager from Unity_Export into SvT -> Find %Team_Achievement 
    process_general_unity()

    # Process HCP 
    process_hcp()

    # Add manager id for HCP, Product, Customer
    add_manager_id_col("data/processed/hcp_processed.csv", "Owner_Name", "data/processed/hcp_processed.csv")
    add_manager_id_col("data/processed/Product_List_Unity_Processed.csv", "UserKey_4Map", "data/processed/Product_List_Unity_Processed.csv")
    add_manager_id_col("data/processed/Customer_List_Unity_Processed.csv", "UserKey_4Map", "data/processed/Customer_List_Unity_Processed.csv")

    # process_manager()

    create_sample_csv(email='vtvinh@zuelligpharma.com')

final_process()