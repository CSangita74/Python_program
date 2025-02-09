import pandas as pd
import numpy as np

class SalesData:
    def __init__(self, file_path):
        self.file_path = file_path
        try:
            self.df = pd.read_csv(file_path)
            print(self.df.columns)
            required_columns = {'Date', 'Product', 'Quantity', 'Price_per_unit'}
            if not required_columns.issubset(self.df.columns):
                raise ValueError("CSV file is missing required columns.")
        except FileNotFoundError:
            print("Error: File not found.")
            self.df = None
        except pd.errors.EmptyDataError:
            print("Error: File is empty.")
            self.df = None
        except ValueError as ve:
            print(f"Error: {ve}")
            self.df = None
    
    def calculate_revenue(self):
        if self.df is None:
            return None
        self.df['Revenue'] = self.df['Quantity'] * self.df['Price_per_unit']
        revenue_per_product = self.df.groupby('Product')['Revenue'].sum()
        return revenue_per_product.nlargest(3)
    
    def get_max_min_sales(self):
        if self.df is None:
            return None
        total_sales = self.df.groupby('Product')['Quantity'].sum()
        max_selling = total_sales.idxmax()
        min_selling = total_sales.idxmin()
        return max_selling, min_selling
    
    def filter_sales_by_year(self, year):
        if self.df is None:
            return None
        self.df['Date'] = pd.to_datetime(self.df['Date'], errors='coerce')
        return self.df[self.df['Date'].dt.year == year]
    
    def get_quantity_statistics(self):
        if self.df is None:
            return None
        quantities = self.df['Quantity'].to_numpy()
        return {
            'Mean': np.mean(quantities),
            'Median': np.median(quantities),
            'Std Dev': np.std(quantities)
        }

# Example usage
file_path = "sales_data.csv"
sales_data = SalesData(file_path)

# Fetch top 3 products by revenue
print("Top 3 Products by Revenue:", sales_data.calculate_revenue())

# Get best and worst selling products
print("Best and Worst Selling Products:", sales_data.get_max_min_sales())

# Filter sales for a specific year (example: 2023)
print("Sales in 2023:", sales_data.filter_sales_by_year(2023))

# Get quantity statistics
print("Quantity Statistics:", sales_data.get_quantity_statistics())
