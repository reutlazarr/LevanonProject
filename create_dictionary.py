import pandas as pd

def group_editing_sites_by_gene_and_strand(sites_from_genome_path):
    sites_from_genome = pd.read_csv(sites_from_genome_path)
    # create the structure of the dictionary containing gene as a key and df as it's value
    united_dict = create_the_dictionary_structure(sites_from_genome)
    for row_ind in range(len(sites_from_genome)):
        for key in united_dict:
            if sites_from_genome.at[row_ind, 'Gene'] == key.split(" ")[0] and sites_from_genome.at[row_ind, 'Strand'] == key.split(" ")[1]:
                united_dict[key] = pd.concat([united_dict[key], sites_from_genome.loc[row_ind]], ignore_index=True)
    return remove_keys_with_empty_values(united_dict)

# remove keys that contain empty values
def remove_keys_with_empty_values(dict):
    empty_keys = [k for k,v in dict.items() if v.empty]
    for k in empty_keys:
        del dict[k]
    return dict

def create_the_dictionary_structure(sites_from_genome):
        # create list of unique genes 
    genes = unique_genes(sites_from_genome)
    # extract the number of genes
    num_of_genes = len(genes)
    # create two df for each gene -/+
    # create df for each gene using dictionary, so that the key is the gene name and the strand and the value is the the df 
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
    for gene in data["Gene"]:
        if gene not in genes_list:
            genes_list.append(gene)
    return genes_list

def print_values_of_dict():
    dict = group_editing_sites_by_gene_and_strand(sites_from_genome_path)
    for values in dict.values():
        print(values)