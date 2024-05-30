# bar_chart_sales.py

import pandas as pd
import matplotlib.pyplot as plt

# Sample data (replace this with your actual data)
data = {
    'Product': ['Product A', 'Product B', 'Product C', 'Product D'],
    'Sales': [1000, 1500, 800, 2000]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Create a bar chart
plt.figure(figsize=(8, 6))
plt.bar(df['Product'], df['Sales'], color='skyblue')
plt.xlabel('Product')
plt.ylabel('Sales')
plt.title('Sales by Product Line')
plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility
plt.tight_layout()

# Save the chart as an image file (optional)
plt.savefig('sales_bar_chart.png')

# Show the chart
plt.show()
