# this was the_tool_shelly_updated
# sites_of_interest- this file contains the editing sites given by the user
# sites_from_genome - the file contains the editing sites of hillel

# import json
# import main as m
# import re
import pandas as pd
# from Bio import SeqIO
# from Bio.SeqRecord import SeqRecord

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

# write all unique genes in one list
def unique_genes(data):
    genes_list = []
    for gene in data["Gene"]:
        if gene not in genes_list:
            genes_list.append(gene)
    return genes_list

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

def iterrows(sites_from_genome):
    for row_ind in range(len(sites_from_genome)):
        print(sites_from_genome.at[row_ind, 'Gene'])

def print_values_of_dict():
    dict = group_editing_sites_by_gene_and_strand(sites_from_genome_path)
    for values in dict.values():
        print(values)

# remove keys that contain empty values
def remove_keys_with_empty_values(dict):
    empty_keys = [k for k,v in dict.items() if v.empty]
    for k in empty_keys:
        del dict[k]
    return dict

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
def group_editing_sites_by_gene_and_strand(sites_from_genome_path):
    sites_from_genome = pd.read_csv(sites_from_genome_path)
    # create the structure of the dictionary containing gene as a key and df as it's value
    united_dict = create_the_dictionary_structure(sites_from_genome)
    for row_ind in range(len(sites_from_genome)):
        for key in united_dict:
            if sites_from_genome.at[row_ind, 'Gene'] == key.split(" ")[0] and sites_from_genome.at[row_ind, 'Strand'] == key.split(" ")[1]:
                united_dict[key] = pd.concat([united_dict[key], sites_from_genome.loc[row_ind]], ignore_index=True)
    return remove_keys_with_empty_values(united_dict)

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


# dislist is made of [site (not of interest), scope, chr]
def min_distance_for_positive(dis_list):
    # list of tuples containing scope and ratio of number of sites/ distance
    scope_ratio_num_of_editing_sites = []
    # for each scope, itearate the different editing sites
    for scope in range(0, 10000, 200):
        site_count = 0
        for _, site_dis_chr in enumerate(dis_list):
            # first is distance, sec is ratio, third is site, fourth is chr
            dis_of_specific_site = site_dis_chr[1]
            chr_of_specific_site = site_dis_chr[2]
            # check if the current site is in the scope checked
            if dis_of_specific_site <= scope and dis_of_specific_site > 0:
                site_count += 1
                ratio = site_count/scope
                # avoid duplicates
                if len(scope_ratio_num_of_editing_sites) != 0 and scope_ratio_num_of_editing_sites[-1][0] == "scope: " + str(scope):
                    scope_ratio_num_of_editing_sites[-1][1] = "ratio: " + str(ratio)
                    scope_ratio_num_of_editing_sites[-1][2] = "site: " + str(site_count)
                    scope_ratio_num_of_editing_sites[-1][3] = "chr: " + str(chr_of_specific_site)
                else: 
                    scope_ratio_num_of_editing_sites.append(["scope: " +str(scope), "ratio: " + str(ratio), "site: " + str(site_count), "chr: " + str(chr_of_specific_site)])
    return scope_ratio_num_of_editing_sites


def min_distance_for_negative(dis_list):
         # list of tuples cotaining scope and ratio of number of sites/ distance
    scope_ratio_num_of_editing_sites = []
    # for each scope, itearate the different editing sites
    for scope in range(0, -10000, -200):
        site_count = 0
        for _, site_dis_str in enumerate(dis_list):
            # first is distance, sec is ratio, third is 
            dis_of_specific_site = site_dis_str[1]
            chr_of_specific_site = site_dis_str[2]
            # check if the current site is in the scope checked
            if dis_of_specific_site >= scope and dis_of_specific_site < 0:
                site_count += 1
                ratio = -(site_count)/(scope)
                # avoid duplicates
                if len(scope_ratio_num_of_editing_sites) != 0 and scope_ratio_num_of_editing_sites[-1][0] == "scope: " + str(scope):
                    scope_ratio_num_of_editing_sites[-1][1] = "ratio: " + str(ratio)
                    scope_ratio_num_of_editing_sites[-1][2] = "site: " + str(site_count)
                    scope_ratio_num_of_editing_sites[-1][3] = "chr: " + str(chr_of_specific_site)
                else: 
                    scope_ratio_num_of_editing_sites.append(["scope: " +str(scope), "ratio: " + str(ratio), "site: " + str(site_count), "chr: " + str(chr_of_specific_site)])
    return scope_ratio_num_of_editing_sites


# find the ideal distance by first sort the list by the ratio and then return its matching window
def find_optimal_dis_in_scope_and_ratio(scope_ratio_num_of_editing_sites_p, scope_ratio_num_of_editing_sites_n):
    scope_ratio_num_of_editing_sites_p += scope_ratio_num_of_editing_sites_n
    n_p_sorted = sorted(scope_ratio_num_of_editing_sites_p, key=lambda x: float(x[1].split(': ')[1]))
    n_p_sorted_best_10 = n_p_sorted[len(n_p_sorted) - 10 :len(n_p_sorted)]
    return n_p_sorted_best_10

# chr added
# create different combinations of optimal scopes
# extract start, end
def new_ratio_combinations(n_p_sorted_best_10, location_of_site):
    combi_scopes_ratios_sites = []
    # create new combinations of scopes and ratios
    for item1 in n_p_sorted_best_10:
        for item2 in n_p_sorted_best_10:
            # multiply the different items only if they are not identical
            if item1 != item2:
                # the following variables are not affected by the scopes' negativity/ positivity
                scope1 = int(item1[0].split(": ")[1])
                scope2 = int(item2[0].split(": ")[1])
                chr = item1[3].split(": ")[1]
                # the start, end points are affectecd by the scopes' negativity/ positivity
                if scope1 > 0 and scope2 > 0:
                    start = location_of_site
                    end = max(scope1, scope2) + location_of_site
                    # one scope contains the other scope
                    cur_num_site = max(int(item1[2].split(": ")[1]), int(item2[2].split(": ")[1]))
                if scope1 < 0 and scope2 < 0:
                    start = min(scope1, scope2) + location_of_site
                    end = location_of_site
                    cur_num_site = min(int(item1[2].split(": ")[1]), int(item2[2].split(": ")[1]))
                # one of the item's scope is positive and the other one is negative
                if scope1 < 0 and scope2 > 0:
                    start = location_of_site + scope1
                    end = location_of_site + scope2
                    cur_num_site = int(item1[2].split(": ")[1]) + int(item2[2].split(": ")[1])
                if scope1 > 0 and scope2 < 0:
                    start = location_of_site + scope2
                    end = location_of_site + scope1
                    cur_num_site = int(item1[2].split(": ")[1]) + int(item2[2].split(": ")[1])
                # cur_scope is affected by scopes' signs, therefore assigned at the end of the function
                cur_scope = end - start
                cur_ratio = cur_num_site/cur_scope
                combi_scopes_ratios_sites.append(["start: " + str(start), "end: " + str(end), "scope: " +str(cur_scope), "ratio: " + str(cur_ratio), "site: " + str(cur_num_site), "chr: " + str(chr)])
    return combi_scopes_ratios_sites

# firstly, extract the best ratio from the combinations' list
# secondly, extract the best ratio from the best ten ratios list which was previously sorted
# compare the two of them
# return the best ratio
def get_best_ratio(n_p_sorted_best_10, combi_scopes_ratios_sites, location_of_site):
    combi_sorted = sorted(combi_scopes_ratios_sites, key=lambda x: float(x[3].split(': ')[1]))
    # extract the last item since the array is increasingly sorted
    best_from_combi = combi_sorted[len(combi_sorted) - 1]
    best_from_best_10 = n_p_sorted_best_10[len(n_p_sorted_best_10) - 1]
    site_best_from_best_10 = int(best_from_best_10[2].split(": ")[1]) 
    scope_best_from_best_10 = int(best_from_best_10[0].split(": ")[1])
    chr_best_from_best_10 = best_from_best_10[3].split(": ")[1]
    # if best scope > 0 
    if scope_best_from_best_10 > 0:
        start_best_from_best_10 = location_of_site
        end_best_from_best_10 = location_of_site + scope_best_from_best_10
    # if best scope < 0 
    if scope_best_from_best_10 < 0:
        start_best_from_best_10 = location_of_site + scope_best_from_best_10
        end_best_from_best_10 = location_of_site
    # compare ratio from the best combi and ratio from the best 10
    if float(best_from_combi[3].split(": ")[1]) >= float(best_from_best_10[1].split(": ")[1]):
        print("return best combi")
        return best_from_combi
    # if the ratio of best from best 10 is bigger
    else:
        print("return something else")
        ratio = float(best_from_best_10[1].split(": ")[1])
        return ["start: " + str(start_best_from_best_10), "end: " + str(end_best_from_best_10), "scope: " + str(scope_best_from_best_10), "ratio: " + str(ratio), "site: " + str(site_best_from_best_10), "chr: " + str(chr_best_from_best_10)]
    # zohar's get_sequence

def get_reverse_complement(string_seq):
    reverse = string_seq[::-1]
    complement_dict = {'N':'N','A': 'U', 'U': 'A', 'G': 'C', 'C': 'G','a': 'u', 'u': 'a', 'g': 'c', 'c': 'g'}
    reverse_complement = ''.join([complement_dict[base] for base in reverse])
    return reverse_complement


# main
sites_from_genome_path = "/private10/Projects/Reut_Shelly/our_tool/data/sites_from_genome.csv"
sample_sites_from_genome_path = "/private10/Projects/Reut_Shelly/our_tool/data/sample_file.csv"
sites_from_genome = pd.read_csv(sites_from_genome_path)

df = create_df_from_bed_file("/private10/Projects/Reut_Shelly/our_tool/data/sites_of_interest_sample.bed")
sample_sites_from_genome_path = "/private10/Projects/Reut_Shelly/our_tool/data/sample_file.csv"
united_dict = group_editing_sites_by_gene_and_strand(sample_sites_from_genome_path)
dict_path = '/private10/Projects/Reut_Shelly/our_tool/data/whole_dict.json'


genome_path = "/private/dropbox/Genomes/Human/hg38/hg38.fa"
# 3
# loc3 = 3218829
# # #dislist is made of [site (not of interest), scope, chr]
# dis_list3 = [(3195223, -23606, 'chrY'), (3195224, -23605, 'chrY'), (3195299, -23530, 'chrY'), (3208500, -10329, 'chrY'), (3208570, -10259, 'chrY'), (3215475, -3354, 'chrY'), (3215477, -3352, 'chrY'), (3218665, -164, 'chrY'), (3218691, -138, 'chrY'), (3218692, -137, 'chrY'), (3218826, -3, 'chrY'), (3218827, -2, 'chrY'), (3218829, 0, 'chrY')]

# # # 2
# loc2 = 100024063
# dis_list2 = [(100024063, 0, 'chr1')]

# 1
# loc1 = 10003145
# dis_list1 = [(9988297, -14848, 'chr1'), (10003145, 0, 'chr1'), (10004789, 1644, 'chr1'), (10006225, 3080, 'chr1')]

# print(main.main())

# print("site 1")
# get_output_ratio_based_tool(dis_list1, loc1, genome_path)
# print("site 2")
# get_output_ratio_based_tool(dis_list2, loc2, genome_path)
# print("site 3")
# get_output_ratio_based_tool(dis_list3, loc3, genome_path)
# site, end, scope, site, chrs