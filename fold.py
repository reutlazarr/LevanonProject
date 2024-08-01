import os
import subprocess
import pre_fold as first
from get_fasta import genome_reader
import create_list_of_distance as l_dis
import abblast as blast
import post_fold_analysis as post_fold
import ratio_based_method as ratio_based_tool
import deafult_method as default_tool
import max_distance_method as max_distance_tool
import json
import os
import multiprocessing


def is_file_empty(file_path):
    return os.path.isfile(file_path) and os.path.getsize(file_path) == 0

# shape file - contains which sites we want to color 
def run_drawRNAstructure(path_ct_file, path_shape_file, path_svg_file):
    # path to the script we want to runf  
    path_to_sh_draw = "/home/alu/aluguest/Reut_Shelly/vscode/code_reut/LevanonProject/LevanonProject/run_drawRNAstructure.sh"
    subprocess.run([path_to_sh_draw, path_ct_file, path_svg_file, path_shape_file])

# variables: file - dbn. + its directory
# output - st. file with bdRNA output
# create st file 
def run_bpRNA(path_to_bpRNA_result, site_dir):
    # path to zohar's script
    bpRNA_path="/home/alu/aluguest/Reut_Shelly/vscode/code_reut/LevanonProject/LevanonProject/run_bpRNA.sh"
    os.chdir(site_dir)
    p = subprocess.run([bpRNA_path, path_to_bpRNA_result], capture_output=True, text=True)
    # if the process fails
    assert not p.stdout, "bpRNA cant run file: " + path_to_bpRNA_result

def create_bpRNA_path(path_to_bpRNA_result, site_dir):
    # create out file name
    out_f = path_to_bpRNA_result.split("/")[-1]
    # get rid of the dbn suffix
    out_f = remove_suffix(out_f, os.path.splitext(out_f)[1]) + ".st"
    st_path = site_dir + out_f
    return st_path

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

# call out four functions and send their output to the folding program

# run the folding program
def run_mxfold2(fasta_seq_to_fold, path_to_mxfold2_result):
    print("run mx")
    path_to_script = "/private10/Projects/Reut_Shelly/our_tool/mxfold_2/run_mxfold2.sh"
    subprocess.run([path_to_script, fasta_seq_to_fold, path_to_mxfold2_result], capture_output=True, text=True)
    print("run completed")
    return path_to_mxfold2_result

# create different kind of files
# the shape file is now a default one 

def create_files(location_of_site, tool_type, tool_dir):
    try:
        # Create path to ct file inside the relevant directory
        ct_file_name = f'{location_of_site}_{tool_type}_ct_file.ct'
        ct_file_path = os.path.join(tool_dir, ct_file_name)

        # Create path to shape file
        shape_file_path = "/private10/Projects/Reut_Shelly/our_tool/data/draw_RNA_structures/my_shape.shape"

        # Create path to svg file
        svg_file_name = f'{location_of_site}_{tool_type}_svg_file.svg'
        svg_file_path = os.path.join(tool_dir, svg_file_name)

        # Create dbn file for mxfold2
        dbn_file_name = f'{location_of_site}_{tool_type}_mxfolded.dbn'
        path_to_mxfold2_result = os.path.join(tool_dir, dbn_file_name)

        # Actually create the files to ensure they exist
        open(ct_file_path, 'a').close()
        open(svg_file_path, 'a').close()
        open(path_to_mxfold2_result, 'a').close()

        return ct_file_path, shape_file_path, svg_file_path, path_to_mxfold2_result
    except Exception as e:
        print(f"Error in create_files: {e}")
        return None, None, None, None

# this part is shared by the four different tools
def common_part_of_tool(chr, start, end, location_of_site, genome_path, tool, tool_dir):
    # create empty files
    ct_file_path, shape_file_path, svg_file_path, path_to_mxfold2_result = create_files(location_of_site, tool, tool_dir)
    gr = genome_reader(genome_path)
    #we should check this part! with it and without it
    unconverted_seq = gr.get_fasta(chr, int(start-1), int(end-1))
    #seq_converted = convert_dna_to_formal_format(unconverted_seq)
    seq_converted = (blast.transcribe_dna_to_rna(unconverted_seq)).upper()
    distance = end - start
    fasta_seq_to_fold= write_to_fasta_file(location_of_site, seq_converted, chr, tool, tool_dir, distance) 
    # convert to dbn file
    # send it to the folding program:
    if is_file_empty(path_to_mxfold2_result):
        path_to_mxfold2_result = run_mxfold2(fasta_seq_to_fold, path_to_mxfold2_result)
        print(f"after mx by {tool}")
    if is_file_empty(ct_file_path):
        convert_dbn_to_ct(path_to_mxfold2_result, ct_file_path)
        print("ct_file wasn't empty")
    print(f"after convertion to ct by {tool}")

    if not (is_file_empty(ct_file_path)) and not (is_file_empty(shape_file_path)) and is_file_empty(svg_file_path):
        run_drawRNAstructure(ct_file_path, shape_file_path, svg_file_path)
        print(f"after drawRNAst by {tool}")
    
    # copy everything that's inside the mxfolded file 
    # shutil.copyfile(path_to_mxfold2_result, path_to_bpRNA_result)
    st_path = create_bpRNA_path(path_to_mxfold2_result, tool_dir)
    st_path = run_bpRNA(path_to_mxfold2_result, tool_dir)
    print(f"after bpRNA by {tool}")
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
    print(tool_type_dir)
    if not os.path.exists(tool_type_dir):
        os.mkdir(tool_type_dir)
        return tool_type_dir
    else : return tool_type_dir

def run_by_tool_type(tool, dis_list, location_of_site, chr, genome_path, site_dir):
    relevant_function = eval(f"{tool}.get_output_{tool}")
    print(relevant_function)
    start_point, end_point = relevant_function(dis_list, location_of_site)
    if (start_point == 0 and end_point == 0):
        st_path = ""
    else:
        dir = create_directory_by_tool_type(site_dir, tool)
        st_path = common_part_of_tool(chr, start_point, end_point, location_of_site, genome_path, tool, dir)
        print("tool " + tool)
    return start_point, end_point, st_path
    
def open_json_file_for_reading(file):
    with open (file, 'r') as sites_from_genome_dict:
        sites_from_genome = json.load(sites_from_genome_dict)
        return sites_from_genome
    
# def united_main():
#     # Define paths for the bed file and the genome file
#     bed_file_path = "/private10/Projects/Reut_Shelly/our_tool/data/sites_sample_shelly.bed"
#     genome_path = "/private/dropbox/Genomes/Human/hg38/hg38.fa"

#     # Open the BED file to process sites of interest
#     with open(bed_file_path, 'r') as bed_file:
#         # Read through each line in the BED file, representing different editing sites
#         for line in bed_file:
#             # Ensure the line is valid according to predefined criteria
#             check_bed_file_validity(line)
#             # Extract relevant fields from the line
#             fields = line.strip().split('\t')
#             # Calculate distances to each site of interest and determine their chromosome and position
#             dis_list, location_of_site, chr = l_dis.pipline(fields) 
#             # Generate a directory path for analyses specific to each site
#             site_dir = f"/private10/Projects/Reut_Shelly/our_tool/data/sites_of_interest_analysis/{chr}_{location_of_site}/"
#             # Create the directory if it does not exist
#             if not os.path.exists(site_dir):
#                 os.mkdir(site_dir)
            
#             # List of tools for processing the sites
#             tools_list = ["ratio_based_tool"]
#             # Process each site with the listed tools
#             for tool in tools_list:
#                 # Run analysis for each tool, capturing analysis-specific parameters
#                 start, end, st_path = run_by_tool_type(tool, dis_list, location_of_site, chr, genome_path, site_dir)
#                 print(f"The original start is: {start}, the original end is: {end}, the original location of site is: {location_of_site}")
#                 if not st_path:
#                         print(f"Failed to get st_path for tool {tool}")
#                         continue
#                 # Print results of the tool run for verification and logging

#                 # Perform the main analysis using the obtained parameters
#                 # don't forget
#                 # post_fold.extract_segment(start, end, st_path, location_of_site)
#             # Indicate completion of processing for the current site
#             print("done")


def process_line(line, genome_path):
    check_bed_file_validity(line)
    fields = line.strip().split('\t')
    dis_list, location_of_site, chr = l_dis.pipline(fields)
    site_dir = f"/private10/Projects/Reut_Shelly/our_tool/data/multi_100/{chr}_{location_of_site}/"
    # site_dir = f"/private10/Projects/Reut_Shelly/our_tool/data/sites_of_interest_analysis_multi_process/{chr}_{location_of_site}/"
    # site_dir = f"/private10/Projects/Reut_Shelly/our_tool/data/sites_of_interest_analysis/{chr}_{location_of_site}/"
    if not os.path.exists(site_dir):
        os.mkdir(site_dir)
    
    tools_list = ["default_tool", "ratio_based_tool", "max_distance_tool"]
    for tool in tools_list:
        start, end, st_path = run_by_tool_type(tool, dis_list, location_of_site, chr, genome_path, site_dir)
        print(f"The original start is: {start}, the original end is: {end}, the original location of site is: {location_of_site}")
        if not st_path:
            print(f"Failed to get st_path for tool {tool}")
            continue
        # Perform the main analysis using the obtained parameters
        # post_fold.extract_segment(start, end, st_path, location_of_site)
    print("done")

def united_main():
    # bed_file_path = "/private10/Projects/Reut_Shelly/our_tool/data/bed_files_shelly/10_editing_sites.bed"
    # bed_file_path = "/private10/Projects/Reut_Shelly/our_tool/data/bed_files_shelly/new_bed_file_shelly.bed"
    bed_file_path ="/private10/Projects/Reut_Shelly/our_tool/data/bed_files_shelly/1000_editing_sites.bed"
    genome_path = "/private/dropbox/Genomes/Human/hg38/hg38.fa"
    
    with open(bed_file_path, 'r') as bed_file:
        lines = bed_file.readlines()

    # Use multiprocessing Pool
    with multiprocessing.Pool(processes=35) as pool:  # Adjust the number of processes as needed
        pool.starmap(process_line, [(line, genome_path) for line in lines])


if __name__ == "__main__":
    united_main()