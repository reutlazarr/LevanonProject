import pandas as pd

def check_duplicate_combinations(csv_file_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Create a new DataFrame with relevant columns
    combinations = df[['editing_site_location', 'method']]

    # Count duplicates
    duplicates = combinations.value_counts()

    # Filter to find combinations that occur more than once
    duplicate_combinations = duplicates[duplicates > 1]

    # Print the results
    if not duplicate_combinations.empty:
        print("Duplicate combinations of editing_site_location and method:")
        print(duplicate_combinations)
    else:
        print("No duplicate combinations found.")

# Example usage
check_duplicate_combinations("/private10/Projects/Reut_Shelly/our_tool/data/969-40000_no_multi/final_df.csv")
