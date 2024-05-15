'''
reorganize.py
site_index = 1

def create_df_from_bed_file(sites_of_interest):

def extract_site_from_sites_of_interest(df):

def is_gene_in_sites_from_genome(gene, data):

removed - def unique_genes(data):

removed - def create_the_dictionary_structure(sites_from_genome):

def iterrows(sites_from_genome):

removed - def print_values_of_dict():

removed - def remove_keys_with_empty_values(dict):

removed - def group_editing_sites_by_gene_and_strand(sites_from_genome_path):

def find_num_of_sites_in_scope(dis_list, scope):

def max_distance(dis_list, location_of_site):

def display_the_dict(united_dict):

def min_distance_for_positive(dis_list):

def min_distance_for_negative(dis_list):

def find_optimal_dis_in_scope_and_ratio(scope_ratio_num_of_editing_sites_p, scope_ratio_num_of_editing_sites_n):

def new_ratio_combinations(n_p_sorted_best_10, location_of_site):

def get_best_ratio(n_p_sorted_best_10, combi_scopes_ratios_sites, location_of_site):

def get_reverse_complement(string_seq):

in the main function
path to sites of genome (by hillel)
convert the file to csv
create dictionary where key=gene and value= [list of sites] and remove keys with empty values
create path for this dict
we cleared this file from its callings to different functions 
'''

'''
fold.py

def is_file_empty(file_path):

def run_drawRNAstructure(path_ct_file, path_shape_file, path_svg_file):

def run_bpRNA(path_to_bpRNA_result, site_dir):

def create_bpRNA_path(path_to_bpRNA_result, site_dir):

def remove_suffix(input_string, suffix):

def convert_dbn_to_ct(dbn_file, ct_file):

def check_bed_file_validity(line):

def convert_Hillel_format_to_UCSC_format(orig_bed_file, new_bed_file):

def get_output_ratio_based_tool(dis_list, location_of_site):

def get_output_max_distance_tool(dis_list, location_of_site):

def get_output_default_tool(dis_list, location_of_site):

def get_output_ABblast_tool():

def run_mxfold2(fasta_seq_to_fold, path_to_mxfold2_result):

def create_files(location_of_site, tool_type, tool_dir):

def common_part_of_tool(chr, start, end, location_of_site, genome_path, tool_type, tool_dir):

def write_to_fasta_file(location_of_site, sequence, chr, tool_type, site_dir, distance):

def convert_dna_to_formal_format(dna):

def create_directory_by_tool_type(site_dir_path, tool_type):

def run_by_tool_type(tool_type1, dis_list, location_of_site, chr, genome_path, site_dir):

def open_json_file_for_reading(file):

united main():
to add: call def group_editing_sites_by_gene_and_strand(sites_from_genome_path) with all its functions

'''                                                                                                                                                                                                                                                                    