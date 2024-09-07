import os
import pandas as pd

def sort_df(orig_path, file_name):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(orig_path)
    
    # Sort the DataFrame by the 'editing_site' column
    df_sorted = df.sort_values(by='editing_site_location')
    
    # Extract the directory from the original path
    dir_name = os.path.dirname(orig_path)
    
    # Create the output file path
    output_path = os.path.join(dir_name, f'{file_name}.csv')
    
    # Save the sorted DataFrame to the output file
    df_sorted.to_csv(output_path, index=False)
    
    # Return the output path if you want to confirm the location
    return output_path

final_df_path = "/private10/Projects/Reut_Shelly/our_tool/data/10_sites_new_df_3108/final_df.csv"
no_segment_df_path = "/private10/Projects/Reut_Shelly/our_tool/data/10_sites_new_df_3108/no_segment_df.csv"
sorted_final_df = sort_df(final_df_path, "sorted_finall_df")
sorted_no_segment_df = sort_df(no_segment_df_path, "sorted_no_segmentt")