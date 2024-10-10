import pandas as pd

def find_invalid_sites(csv_file_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Define a condition that checks if the editing_site_location is within the specified ranges
    condition = (
        ((df['editing_site_location'] >= df['start_first_strand']) & (df['editing_site_location'] <= df['end_first_strand'])) |
        ((df['editing_site_location'] >= df['start_second_strand']) & (df['editing_site_location'] <= df['end_second_strand']))
    )

    # Filter the rows where the editing_site_location does not follow the rule
    invalid_sites = df[~condition]

    # Print the sites that do not follow the rule
    if not invalid_sites.empty:
        print("Sites that do not follow the rule:")
        print(invalid_sites)
    else:
        print("All sites follow the rule.")

# Example usage
find_invalid_sites("/private10/Projects/Reut_Shelly/our_tool/data/969-40000_no_multi/final_df.csv")
