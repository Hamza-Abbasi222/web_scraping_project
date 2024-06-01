# T10_pivot_table_to_excel.py

import pandas as pd

# Sample data (replace this with your actual data)
data = {
    'Date': ['2022-01-01', '2022-01-01', '2022-01-02', '2022-01-02', '2022-01-03'],
    'Category': ['A', 'B', 'A', 'B', 'A'],
    'Value': [10, 20, 30, 40, 50]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Create a pivot table
pivot_table = df.pivot_table(index='Date', columns='Category', values='Value', aggfunc='sum')

# Export the pivot table to an Excel file
excel_file = 'pivot_table.xlsx'
pivot_table.to_excel(excel_file)

print(f"Pivot table exported to '{excel_file}'.")
