import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. Load the Data ---
# Make sure this path is correct relative to where you run the script.
# If analysis.py is in the same folder as books_data.csv, this is correct.
try:
    df = pd.read_csv('books_data.csv')
    print("Data loaded successfully from books_data.csv")
    print(f"Total books in dataset: {len(df)}")
    print("\nDataFrame Info:")
    df.info()
except FileNotFoundError:
    print("Error: 'books_data.csv' not found. Make sure you've run scraper.py first and the file is in the same directory.")
    exit() # Exit if the file isn't found

# --- 2. Data Cleaning & Type Conversion (Double-check, as we did this during scraping) ---
# It's good practice to re-verify or re-clean if loading from CSV,
# as CSVs inherently store data as strings.
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce').astype('Int64') # Int64 for nullable integer

print("\nData types after loading and final conversion:")
print(df.dtypes)

# Remove any rows where Price or Rating might be NaN after conversion (if any)
df.dropna(subset=['Price', 'Rating'], inplace=True)


# --- 3. Create Visualizations ---

# Set a style for the plots (optional, makes them look nicer)
sns.set_style("whitegrid")
plt.figure(figsize=(15, 5)) # Create a figure to hold multiple subplots

# --- Visualization 1: Distribution of Book Prices (Histogram) ---
plt.subplot(1, 2, 1) # 1 row, 2 columns, first plot
sns.histplot(df['Price'], bins=20, kde=True, color='skyblue')
plt.title('Distribution of Book Prices', fontsize=14)
plt.xlabel('Price (£)', fontsize=12)
plt.ylabel('Number of Books', fontsize=12)
plt.grid(axis='y', alpha=0.75)
# Save this plot
plt.savefig('price_distribution.png', dpi=300, bbox_inches='tight')


# --- Visualization 2: Distribution of Book Ratings (Count Plot) ---
plt.subplot(1, 2, 2) # 1 row, 2 columns, second plot
# Convert Rating to category for proper ordering on x-axis
df['Rating'] = df['Rating'].astype('category')
# Order categories from 1 to 5
rating_order = sorted(df['Rating'].unique())
# FIXED: Added hue='Rating', legend=False
sns.countplot(x='Rating', data=df, palette='viridis', order=rating_order, hue='Rating', legend=False)
plt.title('Distribution of Book Ratings', fontsize=14)
plt.xlabel('Rating (Stars)', fontsize=12)
plt.ylabel('Number of Books', fontsize=12)
plt.grid(axis='y', alpha=0.75)


# --- Visualization 3: Average Price by Rating (Bar Plot) ---
plt.figure(figsize=(8, 6))
# Updated line for groupby (add observed=False to silence warning)
avg_price_by_rating = df.groupby('Rating', observed=False)['Price'].mean().reset_index()
# Updated line for barplot
sns.barplot(x='Rating', y='Price', data=avg_price_by_rating, palette='coolwarm', hue='Rating', legend=False)
plt.title('Average Book Price by Rating', fontsize=16)
plt.xlabel('Rating (Stars)', fontsize=14)
plt.ylabel('Average Price (£)', fontsize=14)
plt.grid(axis='y', alpha=0.75)
plt.show()