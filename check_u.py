import os
import pandas as pd

def check_for_U_in_csv(csv_file_path, output_file_path):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Filter rows where 'editing_base' equals 'U'
    filtered_df = df[df['editing_base'] == 'U']
    
    # Check if there are any rows with 'U' and save them to a new CSV file
    if not filtered_df.empty:
        filtered_df.to_csv(output_file_path, index=False)
        print(f"Found {len(filtered_df)} rows where 'editing_base' is 'U'. Results saved to {output_file_path}.")
    else:
        print(f"No 'U' found in 'editing_base' column in file: {csv_file_path}")

def process_all_final_df_files_in_directory(base_directory, output_directory):
    # Iterate through all directories and subdirectories in the base directory
    for root, dirs, files in os.walk(base_directory):
        for file_name in files:
            if file_name == "final_df.csv":
                csv_file_path = os.path.join(root, file_name)
                # Extract a meaningful directory name from the root path
                dir_name = os.path.relpath(root, base_directory).replace(os.sep, '_')
                output_file_path = os.path.join(output_directory, f"filtered_U_rows_{dir_name}.csv")
                check_for_U_in_csv(csv_file_path, output_file_path)

# Example usage:
base_directory = "/private10/Projects/Reut_Shelly/our_tool/data/division_to_500"
output_directory = "/private10/Projects/Reut_Shelly/our_tool/data/division_to_500/check/filtered_U_results/"
os.makedirs(output_directory, exist_ok=True)  # Create output directory if it doesn't exist

process_all_final_df_files_in_directory(base_directory, output_directory)
