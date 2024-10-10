import pandas as pd

def check_sites_in_bed(csv_file_path, bed_file_path, csv_site_column, bed_site_column):
    # Read the CSV file and filter rows where 'editing base' equals 'U'
    df = pd.read_csv(csv_file_path)
    filtered_df = df[df['editing_base'] == 'U']
    
    # Extract the editing site locations from the specified column in the CSV
    csv_sites = filtered_df[csv_site_column].unique()
    
    # Read the BED file (assuming tab-separated with no headers)
    bed_df = pd.read_csv(bed_file_path, sep='\t', header=None)
    
    # Check each site from the CSV if it appears twice in the specified BED column
    for site in csv_sites:
        site_count = bed_df[bed_site_column].value_counts().get(site, 0)
        if site_count == 2:
            print(f"Site {site} appears twice in column {bed_site_column} of the BED file.")
        else:
            print(f"Site {site} appears {site_count} times in column {bed_site_column}.")

# Example usage:
check_sites_in_bed("/private10/Projects/Reut_Shelly/our_tool/data/969-40000_no_multi/final_df.csv", "/private10/Projects/Reut_Shelly/our_tool/data/convert_sites/sites_for_analysis/all_sites_converted.bed", "editing_site_location", 2)
