# this was the_tool_shelly_updated
# sites_of_interest- this file contains the editing sites given by the user
# sites_from_genome - the file contains the editing sites of hillel

import pandas as pd
# if we delete the columns' row, site_index should initialize to 0
site_index = 1

def create_df_from_bed_file(sites_of_interest):
    data = []
    with open(sites_of_interest) as f:
        for line in f:
            data.append(line.split("\t"))
    df = pd.DataFrame(data)
    return df

# each site will be extracted as a dictionary
# site_index is a global variable so that we can iterate through df freely
def extract_site_from_sites_of_interest(df):
    global site_index
    one_site_as_list = df.loc[site_index].tolist()
    site_index += 1
    return one_site_as_list

# check if the gene is in the data
def is_gene_in_sites_from_genome(gene, data):
    if gene not in data["Gene"]:
        print("ERROR: GENE NAME IS NOT IN THE GIVEN DATA")

def iterrows(sites_from_genome):
    for row_ind in range(len(sites_from_genome)):
        print(sites_from_genome.at[row_ind, 'Gene'])

# original
# def group_editing_sites_by_gene_and_strand(sites_from_genome_path):
#     sites_from_genome = pd.read_csv(sites_from_genome_path)
#     # create the structure of the dictionary containing gene as a key and df as it's value
#     united_dict = create_the_dictionary_structure(sites_from_genome)
#     for row_ind in range(len(sites_from_genome)):
#         for key in united_dict:
#             if sites_from_genome.at[row_ind, 'Gene'] == key.split(" ")[0] and sites_from_genome.at[row_ind, 'Strand'] == key.split(" ")[1]:
#                 united_dict[key] = united_dict[key]._append(sites_from_genome.loc[row_ind], ignore_index=True)
#     return remove_keys_with_empty_values(united_dict)

# new
def find_num_of_sites_in_scope(dis_list, scope):
    # scope is positive (loc_site_of_interest is before site)
    ind_of_dis_zero = [dis_list.index(tupl) for tupl in dis_list if tupl[1] == 0]
    ind_of_cur_scope = [dis_list.index(tupl) for tupl in dis_list if tupl[1] == scope]
    # site == num of sites
    site = abs(int(ind_of_cur_scope[0]) - int(ind_of_dis_zero[0]))
    return site

    # iterate dis list from the first item until [loc, 0, chr]

# chr added
# [loc, dis, chr]]
# there is a list of tuples for each site of interest. the first part contains the site's loc, the second contains the distance from our site of interest, the third contains the chr's name
# we should extract the maximal distance and return it as our chosen window
# changes: delete our_tuple and add variable of "tuple_sites_of_interest"
def max_distance(dis_list, location_of_site):
    max_tuple = max(dis_list, key= lambda x: x[1])
    min_tuple = min(dis_list, key= lambda x: x[1])
    max_scope = max_tuple[1]
    min_scope = min_tuple[1]
    if max_scope > 0 and min_scope > 0:
        start = location_of_site
        end = location_of_site + max_scope
        site = find_num_of_sites_in_scope(dis_list, max_scope)
    elif max_scope < 0 and min_scope < 0:
        start = location_of_site + max_scope
        end = location_of_site
        site = find_num_of_sites_in_scope(dis_list, min_scope)
    elif max_scope > 0 and min_scope < 0:
        start = location_of_site + min_scope
        end = location_of_site + max_scope
        site = find_num_of_sites_in_scope(dis_list, max_scope) + find_num_of_sites_in_scope(dis_list, min_scope)
    elif max_scope == 0:
        start = location_of_site + min_scope
        end = location_of_site
        site = find_num_of_sites_in_scope(dis_list, min_scope)
    elif min_scope == 0:
        start = location_of_site
        end = location_of_site + max_scope
        site = find_num_of_sites_in_scope(dis_list, max_scope)
    else:
        # max_scope < 0 and min_scope > 0
        raise Exception("ERROR: MIN SCOPE CAN'T BE BIGGER THAN MAX SCOPE!!!")
    scope = end - start
    chr = str(max_tuple[2])
    # site == num of sites in the current scope
    return ["start: " + str(start), "end: " + str(end), "scope: " + str(scope), "site: " + str(site), "chr: " + str(chr)]


# the dict is msde of sites of genome divided by gene and strand
def display_the_dict(united_dict):
    for key, value in united_dict.items():
        print(f"{key}\n{value}")


def get_reverse_complement(string_seq):
    reverse = string_seq[::-1]
    complement_dict = {'N':'N','A': 'U', 'U': 'A', 'G': 'C', 'C': 'G','a': 'u', 'u': 'a', 'g': 'c', 'c': 'g'}
    reverse_complement = ''.join([complement_dict[base] for base in reverse])
    return reverse_complement

