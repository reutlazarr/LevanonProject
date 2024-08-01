# import pandas as pd
# import json

# def group_editing_sites_by_gene_and_strand(sites_from_genome_path):
#     sites_from_genome = pd.read_csv(sites_from_genome_path)
#     # create the structure of the dictionary containing gene as a key and df as it's value
#     united_dict = create_the_dictionary_structure(sites_from_genome)
#     for row_ind in range(len(sites_from_genome)):
#         for key in united_dict:
#             if sites_from_genome.at[row_ind, 'Gene'] == key.split(" ")[0] and sites_from_genome.at[row_ind, 'Strand'] == key.split(" ")[1]:
#                 united_dict[key] = pd.concat([united_dict[key], sites_from_genome.loc[row_ind]], ignore_index=True)
#     united_dict = remove_keys_with_empty_values(united_dict)
#     save_dict_to_json(united_dict, '/private10/Projects/Reut_Shelly/our_tool/data/dictionary/dict.json')
#     return united_dict

# def save_dict_to_json(dict, filename):
#     json_dict = {k: v.to_dict() for k, v in dict.items()}
#     with open(filename, 'w') as f:
#         json.dump(json_dict, f)

# # remove keys that contain empty values
# def remove_keys_with_empty_values(dict):
#     empty_keys = [k for k,v in dict.items() if v.empty]
#     for k in empty_keys:
#         del dict[k]
#     return dict

# def create_the_dictionary_structure(sites_from_genome):
#         # create list of unique genes 
#     genes = unique_genes(sites_from_genome)
#     # extract the number of genes
#     num_of_genes = len(genes)
#     # create two df for each gene -/+
#     # create df for each gene using dictionary, so that the key is the gene name and the strand and the value is the the df 
#     keys_plus = [gene + " +" for gene in genes]
#     values_plus = [pd.DataFrame() for i in range(1, num_of_genes + 1)]
#     dfs_plus_strand = dict(zip(keys_plus, values_plus))
#     keys_minus = [gene + " -" for gene in genes]
#     values_minus = [pd.DataFrame() for i in range(1, num_of_genes + 1)]
#     dfs_minus_strand = dict(zip(keys_minus, values_minus))
#     united_dict = {**dfs_plus_strand, **dfs_minus_strand}
#     return united_dict

# # write all unique genes in one list
# def unique_genes(data):
#     genes_list = []
#     for gene in data["Gene"]:
#         if gene not in genes_list:
#             genes_list.append(gene)
#     return genes_list

# def print_values_of_dict():
#     dict = group_editing_sites_by_gene_and_strand("/private10/Projects/Reut_Shelly/our_tool/data/convert_sites/all_sites_converted.bed")
#     for values in dict.values():
#         print(values)

# if __name__ == "__main__":
#     print_values_of_dict()
import pandas as pd
import json

def group_editing_sites_by_gene_and_strand(sites_from_genome_path):
    sites_from_genome = pd.read_csv(sites_from_genome_path, delimiter='\t')
    
    # # Debugging: print first few rows of the DataFrame
    # print("First few rows of the DataFrame:")
    # print(sites_from_genome.head())

    # shape[1] = number of columns, should be 6 
    if sites_from_genome.shape[1] < 6:
        raise ValueError("The input file must have at least 6 columns.")

    # create the structure of the dictionary containing gene as a key and df as its value
    united_dict = create_the_dictionary_structure(sites_from_genome)
    print("empty dict: " , united_dict)

    for row_ind in range(len(sites_from_genome)):
        gene = sites_from_genome.iloc[row_ind, 3]  # Assuming 'Gene' is the third column (index 2)
        print("gene: ", gene)
        strand = sites_from_genome.iloc[row_ind, 5]  # Assuming 'Strand' is the sixth column (index 5)
        print("strand:", strand)
        for key in united_dict:
            if gene == key.split(" ")[0] and strand == key.split(" ")[1]:
                united_dict[key] = pd.concat([united_dict[key], sites_from_genome.iloc[[row_ind]]], ignore_index=True)
    united_dict = remove_keys_with_empty_values(united_dict)
    save_dict_to_json(united_dict, '/private10/Projects/Reut_Shelly/our_tool/data/dictionary/mini_dict.json')
    return united_dict

def save_dict_to_json(dict, filename):
    json_dict = {k: v.to_dict() for k, v in dict.items()}
    with open(filename, 'w') as f:
        json.dump(json_dict, f)

# remove keys that contain empty values
def remove_keys_with_empty_values(dict):
    empty_keys = [k for k,v in dict.items() if v.empty]
    for k in empty_keys:
        del dict[k]
    return dict

def create_the_dictionary_structure(sites_from_genome):
    # create list of unique genes 
    genes = unique_genes(sites_from_genome)
    print("genes are: ", genes)
    # extract the number of genes
    num_of_genes = len(genes)
    print("num of genes: ", num_of_genes)
    # create two df for each gene -/+
    # create df for each gene using dictionary, so that the key is the gene name and the strand and the value is the df 
    keys_plus = [gene + " +" for gene in genes]
    values_plus = [pd.DataFrame() for i in range(1, num_of_genes + 1)]
    dfs_plus_strand = dict(zip(keys_plus, values_plus))
    keys_minus = [gene + " -" for gene in genes]
    values_minus = [pd.DataFrame() for i in range(1, num_of_genes + 1)]
    dfs_minus_strand = dict(zip(keys_minus, values_minus))
    united_dict = {**dfs_plus_strand, **dfs_minus_strand}
    return united_dict

# write all unique genes in one list
def unique_genes(data):
    genes_list = []
    for gene in data.iloc[:, 3]:  # Assuming 'Gene' is the third column (index 2)
        if gene not in genes_list:
            genes_list.append(gene)
    return genes_list

def print_values_of_dict():
    dict = group_editing_sites_by_gene_and_strand("/private10/Projects/Reut_Shelly/our_tool/data/convert_sites/mini_all_sites.bed")
    for values in dict.values():
        print(values)

if __name__ == "__main__":
    print_values_of_dict()
