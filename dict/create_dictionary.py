import pandas as pd
import json
from concurrent.futures import ProcessPoolExecutor

# Function to process each row
def process_row(row):
    # Extracting data from the row
    gene = row[3]
    strand = row[5]
    chr = row[0]
    editing_location = row[2]
    
    # Creating the key and new entry
    key = f"{gene} {strand}"
    new_entry = {
        'Chr': str(chr),
        'Editing_Location': int(editing_location),
        'Strand': str(strand),
        'Gene': str(gene)
    }
    return key, new_entry

# Function to group editing sites by gene and strand
def group_editing_sites_by_gene_and_strand(sites_from_genome_path):
    # Reading the file with editing sites
    sites_from_genome = pd.read_csv(sites_from_genome_path, delimiter='\t')
    
    # Checking if the file has at least 6 columns
    if sites_from_genome.shape[1] < 6:
        raise ValueError("The input file must have at least 6 columns.")

    # Creating the structure of the dictionary containing gene as a key and list of dictionaries as its value
    united_dict = create_the_dictionary_structure(sites_from_genome)
    print("empty dict: ", united_dict)

    # Converting the DataFrame to a list of rows
    rows = sites_from_genome.values.tolist()

    # Using ProcessPoolExecutor for parallel processing of rows
    with ProcessPoolExecutor() as executor:
        results = executor.map(process_row, rows)

    # Adding the results to the dictionary
    for key, new_entry in results:
        if key in united_dict:
            united_dict[key].append(new_entry)

    # Removing empty keys and saving the dictionary to a JSON file
    united_dict = remove_keys_with_empty_values(united_dict)
    save_dict_to_json(united_dict, '/private10/Projects/Reut_Shelly/our_tool/data/dictionary/whole_dict.json')
    return united_dict

# Function to save the dictionary to a JSON file
def save_dict_to_json(dict, filename):
    with open(filename, 'w') as f:
        json.dump(dict, f, indent=4)

# Function to remove empty keys from the dictionary
def remove_keys_with_empty_values(dict):
    empty_keys = [k for k, v in dict.items() if not v]
    for k in empty_keys:
        del dict[k]
    return dict

# Function to create the initial dictionary structure
def create_the_dictionary_structure(sites_from_genome):
    # Creating a list of unique genes
    genes = unique_genes(sites_from_genome)
    print("genes are: ", genes)
    
    # Creating keys for each gene with plus and minus strands
    keys_plus = [gene + " +" for gene in genes]
    keys_minus = [gene + " -" for gene in genes]
    
    # Creating the dictionary with empty lists for each key
    united_dict = {key: [] for key in keys_plus + keys_minus}
    return united_dict

# Function to create a list of unique genes from the DataFrame
def unique_genes(data):
    genes_list = []
    for gene in data.iloc[:, 3]:  # Assuming 'Gene' is the fourth column (index 3)
        if gene not in genes_list:
            genes_list.append(gene)
    return genes_list

# Function to print the values of the dictionary (for debugging)
def print_values_of_dict():
    dict = group_editing_sites_by_gene_and_strand("/private10/Projects/Reut_Shelly/our_tool/data/convert_sites/all_sites_converted.bed")
    for values in dict.values():
        print(values)

if __name__ == "__main__":
    print_values_of_dict()
