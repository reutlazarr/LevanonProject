import pandas as pd
def add_line_to_final_df(final_df, chr, start_first_strand, end_first_strand, start_second_strand, end_second_strand, strand, editing_site_location, exp_level, method):
    # Create a new row as a DataFrame
    new_row = pd.DataFrame({
        'chr': [chr],
        'start_first_strand': [start_first_strand],
        'end_first_strand': [end_first_strand],
        'start_second_strand': [start_second_strand],
        'end_second_strand': [end_second_strand],
        'strand': [strand],
        'editing_site_location': [editing_site_location],
        'exp_level': [exp_level],
        'method': [method]
    })
    
    # Append the new row to the existing DataFrame
    final_df = pd.concat([final_df, new_row], ignore_index=True)
    
    return final_df

def create_final_table_structure():
    data = {
        'chr': [],
        'start_first_strand': [],
        'end_first_strand': [],
        'start_second_strand': [],
        'end_second_strand': [],
        'strand': [],
        'editing_site_location': [],
        'exp_level': [],
        'method': []
    }
    df = pd.DataFrame(data)
    
    # Ensure specific columns are treated as integers
    df = df.astype({
        'start_first_strand': 'int',
        'end_first_strand': 'int',
        'start_second_strand': 'int',
        'end_second_strand': 'int',
        'editing_site_location': 'int'
    })
    
    return df


final_df = create_final_table_structure()

# Add lines to the DataFrame
final_df = add_line_to_final_df(final_df, "chr1", 3, 4, 5, 6, "strand", 7, "exp", "tool1")
print(final_df)
final_df = add_line_to_final_df(final_df, "chr2", 2, 2, 2, 2, "strand", 2, "exp", "tool2")
print(final_df)