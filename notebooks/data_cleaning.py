import pandas as pd

# Loading the data
df = pd.read_csv("../data/Brew_n_Beans_sales.csv")

# Converting 'datetime' to proper datetime format
df['datetime'] = pd.to_datetime(df['datetime'], format="%d/%m/%y %H:%M")

# check to confirm conversion
print("Data type of 'datetime':", df['datetime'].dtype)

# Handling Missing Values

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

# Verify and Correct total_price

# Calculate a new total column
df['calculated_total'] = df['unit_price'] * df['quantity']

# Identify where it doesn’t match the existing total_price
mismatch_mask = df['calculated_total'] != df['total_price']
num_mismatches = mismatch_mask.sum()

# Overwrite total_price where necessary
df.loc[mismatch_mask, 'total_price'] = df.loc[mismatch_mask, 'calculated_total']

# Drop the helper column
df.drop(columns='calculated_total', inplace=True)

# Feature Extraction

# Extract hour, date, weekday, and month
df['hour']        = df['datetime'].dt.hour
df['date']        = df['datetime'].dt.date
df['weekday']     = df['datetime'].dt.weekday    # 0=Monday, 6=Sunday
df['weekday_name']= df['datetime'].dt.day_name()
df['month']       = df['datetime'].dt.month

# Flag weekends
df['is_weekend']  = df['weekday'].isin([5, 6]).astype(int)

# reorder columns so date/time features are up front
cols = ['datetime','date','hour','weekday','weekday_name','is_weekend','month'] + \
       [c for c in df.columns if c not in 
        ['datetime','date','hour','weekday','weekday_name','is_weekend','month']]
df = df[cols]

# Saving cleaned data
df.to_csv("../data/cleaned_sales_data.csv", index=False)

print("Feature extraction complete. Cleaned file saved to ../outputs/cleaned_brew_and_bean_sales.csv")


