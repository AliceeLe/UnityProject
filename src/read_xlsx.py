import pandas as pd
import pyodbc

# Define the path to your Excel file
excel_file_path = 'data/raw/SplitRep_BQ_Unity.xlsx'

# Define the connection string for the Excel file
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=' + excel_file_path + ';'
    r'Extended Properties="Excel 12.0;HDR=Yes;IMEX=1";'
)

# Establish a connection to the Excel file
conn = pyodbc.connect(conn_str, autocommit=True)

# Define your SQL query to access the data model
# Replace 'your_table_or_query' with the actual name of the table or query
query = 'SELECT * FROM [your_table_or_query]'

# Read the data into a pandas DataFrame
df = pd.read_sql(query, conn)

# Close the connection
conn.close()

# Display the DataFrame
print(df.head())
