import pandas as pd

# Loading the data
df = pd.read_csv("../data/Brew_n_Beans_sales.csv")

# Converting 'datetime' to proper datetime format
df['datetime'] = pd.to_datetime(df['datetime'], format="%d/%m/%y %H:%M")

# check to confirm conversion
print("Data type of 'datetime':", df['datetime'].dtype)
print(df[['datetime']].head())