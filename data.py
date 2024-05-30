import pandas as pd

# Define the data
data = {
    'Date': ['2024-01-01', '2024-01-01', '2024-01-02', '2024-01-02'],
    'Category': ['Product A', 'Product B', 'Product A', 'Product B'],
    'Value': [100, 200, 150, 250]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Define the file path
csv_file_path = 'sales_data.csv'

# Save the DataFrame to a CSV file
df.to_csv(csv_file_path, index=False)

print(f"CSV file created and saved at: {csv_file_path}")

