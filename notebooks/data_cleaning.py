import pandas as pd

# Loading the data
df = pd.read_csv("../data/Brew_n_Beans_sales.csv")

# Converting 'datetime' to proper datetime format
df['datetime'] = pd.to_datetime(df['datetime'], format="%d/%m/%y %H:%M")

# check to confirm conversion
print("Data type of 'datetime':", df['datetime'].dtype)
print(df[['datetime']].head())
# Step 3B: Handling Missing Values

# Reporting missing before
print("Missing before:\n", df.isnull().sum(), "\n")

# Dropping rows missing essential categorical fields
essential = ['store', 'store_type', 'product', 'category']
df.dropna(subset=essential, inplace=True)

# Inferring missing 'quantity' from unit_price and total_price
qty_missing = df['quantity'].isnull()
df.loc[qty_missing, 'quantity'] = (
    df.loc[qty_missing, 'total_price'] / df.loc[qty_missing, 'unit_price']
).round().astype(int)

# Replace missing 'temperature' with overall mean
mean_temp = df['temperature'].mean()
df['temperature'].fillna(mean_temp, inplace=True)

# Checking missing after to confirm
print("Missing after:\n", df.isnull().sum())
