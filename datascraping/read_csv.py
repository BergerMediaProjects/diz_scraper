import pandas as pd

# Read the CSV file
df = pd.read_csv("seminars.csv")

# Set display options
pd.set_option("display.max_colwidth", 40)  # Limit column width for better readability
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 150)  # Set a fixed width for better formatting

# Check description field
print("\nDescription field analysis:")
print(f"Number of seminars with description: {df['description'].notna().sum()}")
print(f"Number of seminars without description: {df['description'].isna().sum()}")

# Print example of a description if any exists
if df["description"].notna().any():
    print("\nExample of a description:")
    sample_desc = df[df["description"].notna()].iloc[0]
    print(f"\nTitle: {sample_desc['title']}")
    print(f"Description: {sample_desc['description'][:200]}...")
else:
    print("\nNo descriptions found in the data.")

# Print debug file information
print("\nDebug files:")
print(f"Number of seminars with debug files: {df['debug_file'].notna().sum()}")
if df["debug_file"].notna().any():
    print("\nExample debug files:")
    print(df["debug_file"].dropna().head())
