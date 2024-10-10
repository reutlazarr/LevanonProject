import pandas as pd

def check_for_U_in_csv(csv_file_path, output_file_path):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Filter rows where 'editing_base' equals 'U'
    filtered_df = df[df['editing_base'] == 'U']
    
    # Check if there are any rows with 'U'
    if not filtered_df.empty:
        filtered_df.to_csv(output_file_path, index=False)
        print(f"Found {len(filtered_df)} rows where 'editing_base' is 'U'. Results saved to {output_file_path}.")
    else:
        print("No 'U' found in 'editing_base' column.")

# Example usage:
check_for_U_in_csv("/private10/Projects/Reut_Shelly/our_tool/data/division_to_500/100001_100500/final_df.csv","/private10/Projects/Reut_Shelly/our_tool/data/division_to_500/check_u.csv" )
