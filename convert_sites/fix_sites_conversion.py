import pandas as pd

# Path to the input CSV file
input_file_path = '/home/alu/aluguest/Reut_Shelly/vscode/code_shelly/LevanonProject/convert_sites/hillel_sites_final.csv'

# Path to the chr_end_strand file
chr_end_strand_path = '/private8/Projects/zohar/RNAstructure/list_of_site/hillel_site_AG_strand_new.bed'

# Load the input CSV file into a DataFrame
df = pd.read_csv(input_file_path)

# Filter rows where the fourth column (MM6) has the value 'AG'
filtered_df = df[df.iloc[:, 3] == 'AG']

# Further filter rows where the word "intergenic" is not in the fifth or sixth columns
filtered_df = filtered_df[
    (filtered_df.iloc[:, 4] != 'intergenic') & 
    (filtered_df.iloc[:, 5] != 'intergenic')
]

# Select specific columns and rename 'Gene.ncbiRefSeq' to 'Gene'
filtered_df = filtered_df[['Chr', 'Start', 'End', 'Gene.ncbiRefSeq']].rename(columns={'Gene.ncbiRefSeq': 'Gene'})

# Read chr_end_strand file into a DataFrame
df_strand = pd.read_csv(chr_end_strand_path, sep='\t', header=None, names=['Chr', 'End', 'Strand'])

# Merge the filtered DataFrame with the strand information based on 'Chr' and 'End'
filtered_df = pd.merge(filtered_df, df_strand[['End', 'Strand']], on='End', how='left')

# Convert to BED format
filtered_df['dot'] = '.'
bed_df = filtered_df[['Chr', 'Start', 'End', 'Gene', 'dot', 'Strand']]

# Path to the output BED file
output_bed_path = '/home/alu/aluguest/Reut_Shelly/vscode/code_shelly/LevanonProject/convert_sites/all_sites_converted.bed'

# Save the BED DataFrame to a new BED file
bed_df.to_csv(output_bed_path, sep='\t', index=False, header=False)

print(f"Filtered and merged BED file saved to {output_bed_path}")
