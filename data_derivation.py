# Dataset Source https://www.kaggle.com/datasets/shriyashjagtap/e-commerce-customer-for-behavior-analysis/data
import pandas as pd
from faker import Faker
import random
import os

# Create an instance of the Faker class with the 'en_US' locale
fake = Faker('en_US')

# Read the existing CSV file
input_csv_file = 'Dataset/ecommerce_customer_data_large.csv'  # Replace with your input CSV file path
df = pd.read_csv(input_csv_file)

# Create a dictionary to store customerID-based city and membership level data
customer_data_mapping = {}

# Iterate through the DataFrame to create the mapping
for _, row in df.iterrows():
    customer_id = row['Customer ID']
    if customer_id not in customer_data_mapping:
        customer_data_mapping[customer_id] = {
            'Location': fake.city(),
            'MembershipLevel': fake.random_element(elements=('Bronze', 'Silver', 'Gold', 'Platinum')),
            'LastPurchaseDate': row['Purchase Date']
        }
    else:
        last_purchase_date = customer_data_mapping[customer_id]['LastPurchaseDate']
        current_purchase_date = row['Purchase Date']
        if current_purchase_date > last_purchase_date:
            customer_data_mapping[customer_id]['LastPurchaseDate'] = current_purchase_date

# Generate fake data for the 'Location' and 'MembershipLevel' columns based on Customer ID
df['Location'] = [customer_data_mapping[customer_id]['Location'] for customer_id in df['Customer ID']]
df['MembershipLevel'] = [customer_data_mapping[customer_id]['MembershipLevel'] for customer_id in df['Customer ID']]

# Add the 'LastPurchaseDate' column based on customerID
df['LastPurchaseDate'] = [customer_data_mapping[customer_id]['LastPurchaseDate'] for customer_id in df['Customer ID']]

# Determine the favorite category for each customer based on the category purchased in the most quantity
favorite_categories = df.groupby(['Customer ID', 'Product Category'])['Quantity'].sum().unstack().idxmax(axis=1)
df['FavouriteCategory'] = df['Customer ID'].map(favorite_categories)

# Save the updated DataFrame to a new CSV file
output_csv_file = 'Dataset/new_ecommerce_customer_data.csv'  # Replace with your output CSV file path
if os.path.exists(output_csv_file):
    os.remove(output_csv_file)  # Remove the existing file if it exists
df.to_csv(output_csv_file, index=False)

print(f"Fake city and membership level data has been generated and saved to '{output_csv_file}'.")
