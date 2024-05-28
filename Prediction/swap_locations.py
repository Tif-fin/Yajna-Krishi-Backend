import pandas as pd

# File paths
locations_path = "locations.csv"
locations_path_1 = "municipalities.csv"

# Read the CSV files into dataframes
sta = pd.read_csv(locations_path)
mun = pd.read_csv(locations_path_1)

# Ensure that both dataframes have the expected columns
if "Municipality" in mun.columns:
    # Assign the 'Municipality' column from 'mun' to 'sta' as a new column 'Location'
    sta["Location"] = mun["Municipality"]
    
    # Save the modified dataframe to a new CSV file
    sta.to_csv("final.csv", index=False)
else:
    print("Error: 'Municipality' column not found in municipalities.csv")
