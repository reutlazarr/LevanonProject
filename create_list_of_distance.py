# The function will check the distances between the given editing site and the other editing sites that are in the same gene
# and in the same strand
# input- the information on the given editing site and the sites from genome saved as dictionary
# output- sorted list of the distances between the given site and the others known editing sites from genome
import json
import pandas as pd

def split_editing_site_to_varibles(editing_site_of_interest):
    chr_of_editing_site = editing_site_of_interest[0]
    # print(f'30.08 specific site - {editing_site_of_interest[2]}\n')
    # print(f'30.08 all details- {editing_site_of_interest}')
    location_site_of_interest = int(editing_site_of_interest[2])
    strand_of_site= editing_site_of_interest[5]
    gene_of_site = editing_site_of_interest[3]
    key_to_search_in_genome = f'{gene_of_site}' +' '+ f'{strand_of_site}'
    # key_to_search_in_genome = f'{gene_of_site}' +' '+ f'{strand_of_site}'
    return chr_of_editing_site, location_site_of_interest, strand_of_site,gene_of_site,key_to_search_in_genome

# each part is made of 3: the editing site location, the distance from the editing site location and the chr
def create_list_of_distances_from_editing_site(chr_of_editing_site, location_site_of_interest, strand_of_site,gene_of_site,key_to_search_in_genome, sites_from_genome):
    #sites_from genome = {}
    #edit_site_of_interest = []
    dis_list = []
    #gene_of_site = editing_site_of_interest[3]
    #strand_of_site= editing_site_of_interest[2]
    #location_site_of_interest = editing_site_of_interest[1]
    #site_of_intersest = f'gene_of_site + strand_of_site'
    if key_to_search_in_genome in sites_from_genome:
        sites_at_the_same_gene_and_strand = sites_from_genome[key_to_search_in_genome]
        # Iterate over the fit editing sites in the dataframe
        for key in sites_at_the_same_gene_and_strand:
            # Access the 'Editing_Location' column value
            location_of_site_from_genome = key['Editing_Location']
            # Calculate the distance
            dis= int(location_of_site_from_genome)- int(location_site_of_interest)
            location_site_and_dis_and_chr = (location_of_site_from_genome, dis, chr_of_editing_site)
            dis_list.append(location_site_and_dis_and_chr)
    else : 
        raise KeyError(f'The value "{key_to_search_in_genome}" is not in the dictionary.')
    
    #Sorting by proximity to the given editing site
    sorted_dis_list = sorted(dis_list, key=lambda x: x[1])
    print(f"sorted distance list of {location_site_of_interest} is:" ,  sorted_dis_list)
    return sorted_dis_list


#The function will find how many editing sites there are in distance of 1000 base pb

#def minimal_distance(sorted_dis_list):

def pipline(fileds):
    dict_path = "/private10/Projects/Reut_Shelly/our_tool/data/dictionary/whole_dict.json"
    with open (dict_path, 'r') as dict:
        genome = json.load(dict)
    (chr, location, strand, gene, key)= split_editing_site_to_varibles(fileds)
    dis_list = create_list_of_distances_from_editing_site(chr, location, strand, gene, key, genome)
    return dis_list ,location, chr, strand

