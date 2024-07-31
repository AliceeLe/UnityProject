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

merge_qtd()
merge_all()
