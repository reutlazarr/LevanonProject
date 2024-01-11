#this was the_tool_shelly_sec_part
import os
import subprocess
import the_tool_shelly_updated as first
from get_fasta_itamar import genome_reader
import create_list_of_distances_from_editing_site as l_dis
import main as m
import abblast as blast
import post_fold_analysis as post_fold

# shape file - contains which sites we want to color 
def run_drawRNAstructure(path_ct_file, path_shape_file, path_svg_file):
    # path to the script we want to runf  
    path_to_sh_draw = "/private8/Projects/zohar/RNAstructure/itamar_code/run_drawRNAstructure.sh"
    subprocess.run([path_to_sh_draw, path_ct_file, path_svg_file, path_shape_file])

# variables: file - dbn. + its directory
# output - st. file with bdRNA output
# create st file 
def run_bpRNA(path_to_bpRNA_result, site_dir):
    # path to zohar's script
    bpRNA_path="/private6/Projects/Yeast_Itamar_10_2022/Fold_energy/bpRNA/run_bpRNA.sh"
    os.chdir(site_dir)
    p = subprocess.run([bpRNA_path, path_to_bpRNA_result], capture_output=True, text=True)
    # if the process fails
    assert not p.stdout, "bpRNA cant run file: " + path_to_bpRNA_result
    # create out file name
    out_f = path_to_bpRNA_result.split("/")[-1]
    # get rid of the dbn suffix
    out_f = remove_suffix(out_f, os.path.splitext(out_f)[1]) + ".st"
    return site_dir + out_f

def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string

def convert_dbn_to_ct(dbn_file, ct_file):
    path_to_sh_draw = "/private10/Projects/Reut_Shelly/our_tool/data/draw_RNA_structures/run_dot_to_ct.sh"
    subprocess.run([path_to_sh_draw, dbn_file, ct_file], capture_output=True, text=True)


def check_bed_file_validity(line):
    new_line = line.split()
    if len(new_line) < 6:
        print(f"{line} \n INVALID LINE - LESS THAN 6 COLUMNS")
        return
    if new_line[1].isdigit() == False:
        print(f"{line} \n INVALID LINE - NO PROPER START POINT")
        return
    if new_line[2].isdigit() == False:
        print(f"{line} \n INVALID LINE - NO PROPER END POINT")
        return
    if int(new_line[1]) >= int(new_line[2]):
        print(f"{line} \n INVALID LINE - END POINT IS NOT BIGGER THAN START POINT")
        return
    if new_line[5] != "+" and new_line[5] != "-" and new_line[5] != ".":
        print(f"{line} \n INVALID LINE - STRAND COLUMN IS NOT VALID")
        return

# hillel's format is not the identical to the UCSC format
def convert_Hillel_format_to_UCSC_format(orig_bed_file, new_bed_file):
    with open(orig_bed_file, 'r') as orig_file, open(new_bed_file, "w") as new_file:
        for line in orig_file:
            new_line = line.split()
            # Check if the line has enough elements
            if len(new_line) == 4:  # Assuming at least 4 columns are needed
                chr = new_line[0]
                start = int(new_line[1]) - 1
                end = new_line[1]
                strand = new_line[2]
                gene = new_line[3] 
                point = "."
                # Write to the new file
                new_file.write(f"{chr}\t{start}\t{end}\t{gene}\t{point}\t{strand}\n")

# call out four functions and send their output to the folding program

def get_output_ratio_based_tool(dis_list, location_of_site):
    # edge case: our site of interest has no other sites in its vicinity, thus folding it is irrelevant
    if len(dis_list) == 1:
        print("SITE OF INTEREST HAS NO SURROUNDING EDITING SITES")
        return
    # call the func based on best ratio
    # the output starts with scope
    min_positive = first.min_distance_for_positive(dis_list)
    min_negative = first.min_distance_for_negative(dis_list)
    best_ten = first.find_optimal_dis_in_scope_and_ratio(min_positive, min_negative)
    # the output starts with "start"
    new_combinations = first.new_ratio_combinations(best_ten, location_of_site)
    best_ratio_based_list = first.get_best_ratio(best_ten, new_combinations, location_of_site)
    # chr = best_ratio_based_list[5].split(": ")[1]
    start = int(best_ratio_based_list[0].split(": ")[1])
    end = int(best_ratio_based_list[1].split(": ")[1])
    return start, end
    
def get_output_max_distance_tool(dis_list, location_of_site):
    if len(dis_list) == 1:
        print("SITE OF INTEREST HAS NO SURROUNDING EDITING SITES")
        return
    # call the func based on max distance
    best_by_max_dis = first.max_distance(dis_list, location_of_site)
    # chr = best_by_max_dis[4].split(": ")[1]
    start = int(best_by_max_dis[0].split(": ")[1])
    end = int(best_by_max_dis[1].split(": ")[1])
    return start, end

def get_output_default_tool(dis_list, location_of_site):
    # call the func based on default scope
    start, end = l_dis.defaultive_distance(dis_list, location_of_site)
    return start, end

def get_output_ABblast_tool():
    # call the func based on ABblast
                # substrate_seq = m.abblast.substrate_seq(chr, location_of_site)
            # # the checked_seq depends on the result of the get_output_ratio_based_tool 
            # checked_seq = ""
            # m.abblast.first_run_on_abblast(chr ,checked_seq ,substrate_seq)
    # get the relevant sequence from the genome
    # gr = genome_reader(genome_path)
    # return(convert_dna_to_formal_format(gr.get_fasta(seq_by_AB_blast)))
    # # send it to the folding program:
    # seq_to_fold_AB_Blast_based = "/home/alu/aluguest/Reut_Shelly/vscode/code_shelly/seq_to_fold_AB_Blast_based.fa"
    pass
    

# run the folding program
def run_mxfold2(fasta_seq_to_fold, path_to_mxfold2_result):
    path_to_script = "/private10/Projects/Reut_Shelly/our_tool/mxfold_2/run_mxfold2.sh"
    subprocess.run([path_to_script, fasta_seq_to_fold, path_to_mxfold2_result], capture_output=True, text=True)
    return path_to_mxfold2_result

# create different kind of files
# the shape file is now a default one 
def create_files(location_of_site, tool_type, tool_dir):
    # create path to ct file inside the relevant directory
    ct_file_name = f'{location_of_site}_{tool_type}_ct_file.ct'
    ct_file_path = r"{}{}".format(tool_dir, ct_file_name)
    # # create path to shape file   
    # shape_file_name = f'{location_of_site}_{tool_type}_shape_file.shape'
    # shape_file_path = r"{}{}".format(site_dir, shape_file_name)
    shape_file_path = "/private10/Projects/Reut_Shelly/our_tool/data/draw_RNA_structures/my_shape.shape"
    # create path to svg file
    svg_file_name = f'{location_of_site}_{tool_type}_svg_file.svg'
    svg_file_path = r"{}{}".format(tool_dir, svg_file_name)
    # create dbn file for mxfold2
    dbn_file_name = f'{location_of_site}_{tool_type}_mxfolded.dbn'
    path_to_mxfold2_result = r"{}{}".format(tool_dir, dbn_file_name)
    return ct_file_path, shape_file_path, svg_file_path, path_to_mxfold2_result

# this part is shared by the four different tools
def common_part_of_tool(chr, start, end, location_of_site, genome_path, tool_type, tool_dir):
    # create empty files
    ct_file_path, shape_file_path, svg_file_path, path_to_mxfold2_result = create_files(location_of_site, tool_type, tool_dir)
    gr = genome_reader(genome_path)
    #we should check this part! with it and without it
    unconverted_seq = gr.get_fasta(chr, int(start-1), int(end-1))
    #seq_converted = convert_dna_to_formal_format(unconverted_seq)
    seq_converted = (blast.transcribe_dna_to_rna(unconverted_seq)).upper()
    distance = end - start
    fasta_seq_to_fold= write_to_fasta_file(location_of_site, seq_converted, chr, tool_type, tool_dir, distance) 
    # convert to dbn file
    # send it to the folding program:
    path_to_mxfold2_result = run_mxfold2(fasta_seq_to_fold, path_to_mxfold2_result)
    print(f"after mx by {tool_type}")
    convert_dbn_to_ct(path_to_mxfold2_result, ct_file_path)
    print(f"after convertion to ct by {tool_type}")
    run_drawRNAstructure(ct_file_path, shape_file_path, svg_file_path)
    print(f"after drawRNAst by {tool_type}")
    
    # copy everything that's inside the mxfolded file 
    # shutil.copyfile(path_to_mxfold2_result, path_to_bpRNA_result)
    st_path = run_bpRNA(path_to_mxfold2_result, tool_dir)
    print(f"after bpRNA by {tool_type}")
    return st_path


def write_to_fasta_file(location_of_site, sequence, chr, tool_type, site_dir, distance):
    sequence_path_name = f"{location_of_site}_{tool_type}.fa"
    sequence_path = f"{site_dir}{sequence_path_name}"
    header_of_checked_seq = f"> seq to fold of {distance}bp in {chr} in location {location_of_site} by {tool_type}"
    fasta_string_of_checked_seq = f"{header_of_checked_seq}\n{sequence}\n"
    if not os.path.exists(sequence_path):
        with open(sequence_path, "a") as sequence_file:
            #if os.stat(sequence_path).st_size == 0:
            sequence_file.write(fasta_string_of_checked_seq)
    else:
        print(f"The sequence of {location_of_site} has already been written to a fasta file")
    return sequence_path

# convert dna to the UCSC format
def convert_dna_to_formal_format(dna):
    count = 0
    new_dna = ""
    uppercase_dna = dna.upper()
    for i in range(len(uppercase_dna)):
        count += 1
        new_dna += uppercase_dna[i]
        if count % 50 == 0:
            new_dna += '\n'
    return new_dna

# create directory for each tool
def create_directory_by_tool_type(site_dir_path, tool_type):
    # site_dir = f"/private10/Projects/Reut_Shelly/our_tool/data/site_of_interest_analysis/{chr}_{location_of_site}/"
    tool_type_dir = f"{site_dir_path}{tool_type}/"
    if not os.path.exists(tool_type_dir):
        os.mkdir(tool_type_dir)
        return tool_type_dir
    else : return tool_type_dir

def run_by_tool_type(tool_type1, dis_list, location_of_site, chr, genome_path, site_dir):
    dir = create_directory_by_tool_type(site_dir, tool_type1)
    relevant_function = eval(f"get_output_{tool_type1}")
    start_point, end_point = relevant_function(dis_list, location_of_site)
    st_path = common_part_of_tool(chr, start_point, end_point, location_of_site, genome_path, tool_type1, dir)
    return start_point, end_point , st_path

# for specific site of interest extracted by the file "site of interest":
# check the gene and strand - find the suitable key in the dictionary
# create a list of the distances from our site of interest to each one of the sites
# add to the value 

def united_main():
    # This file contains the known editing sites from genome saved as a dictionary
    sites_from_genome_path = '/private10/Projects/Reut_Shelly/our_tool/data/whole_dict.json'
    sites_from_genome = m.open_json_file_for_reading(sites_from_genome_path)
    # sites_of_interest_path = user_interface()
    # This file contains the editing sites we want to examine given by the user
    bed_file_path = "/private10/Projects/Reut_Shelly/our_tool/data/sites_second_sample.bed"
    # Open the BED file and read its content
    # use each one of the four tools
    genome_path = "/private/dropbox/Genomes/Human/hg38/hg38.fa"
    with open(bed_file_path, 'r') as bed_file:
    # Iterate through the lines of the BED file- through the editing sites of interest
        for line in bed_file:
        # Split the line into fields
            fields = line.strip().split('\t')
            check_bed_file_validity(line)
            # we should add function that validates the bed file's propriety
            # Extract relevant information from BED fields
            chr = fields[0]  # Chromosome name
            location_of_site = int(fields[2])  # The location of the editing site is on the end location
            gene_of_site = fields[3]  
            strand_of_site = fields[5]
            key_to_search_in_genome = f'{gene_of_site}' +' '+ f'{strand_of_site}'
            # we should add call for the distance's functions
            dis_list = l_dis.create_list_of_distances_from_editing_site(chr, location_of_site, strand_of_site,gene_of_site, key_to_search_in_genome, sites_from_genome)
            # create new folder for each site
            site_dir = f"/private10/Projects/Reut_Shelly/our_tool/data/sites_of_interest_analysis/{chr}_{location_of_site}/"
            if not os.path.exists(site_dir):
                os.mkdir(site_dir)
            tool_types_list = ["default_tool", "ratio_based_tool", "max_distance_tool"]
            for tool_type in tool_types_list:
                start, end, st_path = run_by_tool_type(tool_type, dis_list, location_of_site, chr, genome_path, site_dir)
                post_fold.main_analysis(start, end, st_path, location_of_site)
            print("done")


if __name__ == "__main__":
    united_main()



###
# chr = "chrY"
# location_of_site = "3218829"
# path_to_mxfold2_result = "/private10/Projects/Reut_Shelly/our_tool/data/chr_plus_site_of_interest/3218829_chrY_dir/3218829_default_tool_mxfolded.dbn"
# path_to_bpRNA_result = "/private10/Projects/Reut_Shelly/our_tool/data/chr_plus_site_of_interest/3218829_chrY_dir/path_ex.dbn"
# os.chdir(f"/private10/Projects/Reut_Shelly/our_tool/data/chr_plus_site_of_interest/{location_of_site}_{chr}_dir/")
# # copy everything that's inside the mxfolded file 
# # cmd_copy = "cp path_to_mxfold2_result path_to_bpRNA_result"
# # subprocess.run(cmd_copy, capture_output=True, text=True)
# shutil.copyfile(path_to_mxfold2_result, path_to_bpRNA_result)

# site_dir = "/private10/Projects/Reut_Shelly/our_tool/data/chr_plus_site_of_interest/3218829_chrY_dir/"
# run_bpRNA(path_to_bpRNA_result, site_dir)
# print("after bpRNA")




