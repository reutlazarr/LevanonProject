import os
import pandas as pd

def find_invalid_sites(csv_file_path, output_file_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Define a condition that checks if the editing_site_location is within the specified ranges
    condition = (
        ((df['editing_site_location'] >= df['start_first_strand']) & (df['editing_site_location'] <= df['end_first_strand'])) |
        ((df['editing_site_location'] >= df['start_second_strand']) & (df['editing_site_location'] <= df['end_second_strand']))
    )

    # Filter the rows where the editing_site_location does not follow the rule
    invalid_sites = df[~condition]

    # Save the invalid sites to a new CSV file if any invalid sites were found
    if not invalid_sites.empty:
        invalid_sites.to_csv(output_file_path, index=False)
        print(f"Invalid sites saved to {output_file_path}.")
    else:
        print(f"All sites follow the rule in file: {csv_file_path}")

def process_all_final_df_files_in_directory(base_directory, output_directory):
    # Iterate through all directories and subdirectories in the base directory
    for root, dirs, files in os.walk(base_directory):
        for file_name in files:
            if file_name == "final_df.csv":
                csv_file_path = os.path.join(root, file_name)
                # Create a unique output file name based on the directory structure
                dir_name = os.path.relpath(root, base_directory).replace(os.sep, '_')
                output_file_path = os.path.join(output_directory, f"invalid_sites_{dir_name}.csv")
                find_invalid_sites(csv_file_path, output_file_path)

# Example usage:

# /private10/Projects/Reut_Shelly/our_tool/data/969-40000_no_multi/
base_directory = "/private10/Projects/Reut_Shelly/our_tool/data/969-40000_no_multi"
output_directory = "/private10/Projects/Reut_Shelly/our_tool/data/969-40000_no_multi/check/invalid_sites_results/"
os.makedirs(output_directory, exist_ok=True)  # Create output directory if it doesn't exist

process_all_final_df_files_in_directory(base_directory, output_directory)
