import pandas as pd
import os

def merge_all():
    # Define the paths to the CSV files
    csv_file_1_path = 'data/Unity_Export_MTDCall_202406.csv'
    csv_file_2_path = 'data/Unity_Export_S360_202406.csv'  
    csv_file_3_path = 'data/merged_qtd.csv'

    # Read the CSV files into DataFrames
    df1 = pd.read_csv(csv_file_1_path)
    df2 = pd.read_csv(csv_file_2_path)
    df3 = pd.read_csv(csv_file_3_path)

    # Merge the DataFrames on the common columns
    merged_df = pd.merge(df1, df2, on=["kpi_tracker_userlevel[kpi.OwnerId]","kpi_tracker_userlevel[Name]", "kpi_tracker_userlevel[UserName_Level1]","kpi_tracker_userlevel[UserId_Level1]"])
    merged_df = pd.merge(merged_df, df3, on=["kpi_tracker_userlevel[kpi.OwnerId]","kpi_tracker_userlevel[Name]", "kpi_tracker_userlevel[UserName_Level1]","kpi_tracker_userlevel[UserId_Level1]"])

    # Define the path to save the merged DataFrame
    output_file_path = 'data/output.csv'

    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv(output_file_path, index=False)

    print(f"Merged CSV file successfully saved as {output_file_path}")

def merge_qtd():
    # Define the paths to the CSV files
    csv_files = [
        'data/Unity_Export_QTDCall_HKMMTWVN_202406.csv',
        'data/Unity_Export_QTDCall_ID_202406.csv',
        'data/Unity_Export_QTDCall_MYSGBNKH_202406.csv',
        'data/Unity_Export_QTDCall_PHTH_202406.csv'
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
    output_file_path = 'data/merged_qtd.csv'

    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv(output_file_path, index=False)

    print(f"Merged CSV file successfully saved as {output_file_path}")

def rename_columns(csv_file_path, new_column_names, output_file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    df = df.round(2)

    # List the original column names
    original_column_names = df.columns.tolist()
    print(f"Original column names: {original_column_names}")

    # Check if the number of new column names matches the number of original column names
    if len(new_column_names) != len(original_column_names):
        print("Error: The number of new column names must match the number of original column names.")
        return

    # Rename the columns
    df.columns = new_column_names

    # List the new column names
    print(f"New column names: {df.columns.tolist()}")

    # Save the DataFrame with the new column names to a new CSV file
    df.to_csv(output_file_path, index=False)
    print(f"DataFrame successfully saved with new column names as {output_file_path}")

# Define the paths to the input and output CSV files
input_csv_file_path = 'data/Unity_sample.csv'
output_csv_file_path = 'data/Sample_renamed.csv'

# Define the new column names
new_column_names = ['ID', 'Name', 'Manager_name', 'Manager_id', 'Call_Rate_MTD', 'Call_Volume_MTD', 'Call_Compliance_MTD', 'Call_Compliance_A_MTD', 'Actual_Sales_MTD', 'Target_MTD', '%Achievement_MTD', 'Balance_MTD', 'Actual_Sales_QTD', 'Target_QTD', '%Achievement_QTD', 'Balance_QTD', 'Call_Rate_QTD', 'Call_Volume_QTD', 'Call_Compliance_QTD', 'Call_Compliance_A_QTD', 'Email']  # Replace with your new column names

# Call the function to rename columns
rename_columns(input_csv_file_path, new_column_names, output_csv_file_path)

# merge_qtd()
# merge_all()
