import pandas as pd

def create_final_table_structure():
    data = {
        'chr': [],
        'start_first_strand': [],
        'end_first_strand': [],
        'start_second_strand': [],
        'end_second_strand': [],
        'strand': [],
        'editing_site_location': [],
        'exp_level': []
    }
    return pd.DataFrame(data)

# Create the DataFrame
df = create_final_table_structure()
