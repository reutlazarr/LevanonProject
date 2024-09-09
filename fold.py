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
import pandas as pd
import csv

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

def run_bpRNA(path_to_dbn_file, site_dir, st_path):
    bpRNA_path = "/home/alu/aluguest/Reut_Shelly/vscode/code_reut/LevanonProject/LevanonProject/run_bpRNA.sh"
    os.chdir(site_dir)
    p = subprocess.run([bpRNA_path, path_to_dbn_file], capture_output=True, text=True)
    with open('bpRNA_output.log', 'w') as log_file:
        log_file.write(f"STDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}\n")
    if os.path.getsize(st_path) == 0:
        print(f"Output .st file is empty. Something went wrong with bpRNA for file: {path_to_dbn_file}")
    return st_path

# def create_bpRNA_path(path_to_dbn_file, site_dir):
#     # create out file name
#     out_f = path_to_dbn_file.split("/")[-1]
#     # get rid of the dbn suffix
#     out_f = remove_suffix(out_f, os.path.splitext(out_f)[1]) + ".st"
#     st_path = site_dir + out_f
#     return st_path

def create_bpRNA_path(path_to_dbn_file, site_dir):
    # Debug print statements
    print(f"Processing file: {path_to_dbn_file}")
    print(f"Saving to directory: {site_dir}")

    # Extract the file name without extension
    file_name = os.path.splitext(os.path.basename(path_to_dbn_file))[0]
    st_path = os.path.join(site_dir, f"{file_name}.st")
    
    print(f"Generated .st path: {st_path}")
    
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
        return False
    if not new_line[1].isdigit():
        print(f"{line} \n INVALID LINE - NO PROPER START POINT")
        return False
    if not new_line[2].isdigit():
        print(f"{line} \n INVALID LINE - NO PROPER END POINT")
        return False
    if int(new_line[1]) >= int(new_line[2]):
        print(f"{line} \n INVALID LINE - END POINT IS NOT BIGGER THAN START POINT")
        return False
    if new_line[5] not in ["+", "-", "."]:
        print(f"{line} \n INVALID LINE - STRAND COLUMN IS NOT VALID")
        return False
    return True

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
def create_files(location_of_site, tool_type, tool_dir, new_location_of_site):
    try:
        # Create path to ct file inside the relevant directory
        ct_file_name = f'{location_of_site}_{tool_type}_ct_file.ct'
        ct_file_path = os.path.join(tool_dir, ct_file_name)

        # Create path to shape file
        shape_file_name = f'{location_of_site}_{tool_type}.shape'
        shape_file_path = os.path.join(tool_dir, shape_file_name)

        try:
            with open(shape_file_path, 'w') as shape_file:
                # Write only the editing site position with the score
                shape_file.write(f"{new_location_of_site} 0.5\n")
            print(f"Shape file created for editing site: {shape_file_path}")
        except Exception as e:
            print(f"Error in create_shape_file_for_editing_site: {e}")

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

def create_shape_file_after_fold(location_of_site, tool_type, tool_dir, editing_site_position, score):
    shape_file_name = f'{location_of_site}_{tool_type}.shape'
    shape_file_path = os.path.join(tool_dir, shape_file_name)

    try:
        with open(shape_file_path, 'w') as shape_file:
            # Write only the editing site position with the score
            shape_file.write(f"{editing_site_position} {score}\n")
        print(f"Shape file created for editing site: {shape_file_path}")
    except Exception as e:
        print(f"Error in create_shape_file_for_editing_site: {e}")

    return shape_file_path

# this part is shared by the four different tools
def common_part_of_tool(chr, start, end, location_of_site, genome_path, tool, tool_dir, strand):
    # Calculate the sequence length
    sequence_length = end - start

    # Skip folding if the sequence is longer than 5500 bp
    if sequence_length > 5600:
        print(f"Skipping folding for {location_of_site} as sequence length {sequence_length} exceeds 5500 bp.")
        return None, None

    new_start, new_end, new_location_of_site, delta = post_fold.ReNumber_the_sequence(start, end, location_of_site, strand)

    # Create empty files
    ct_file_path, shape_file_path, svg_file_path, path_to_mxfold2_result = create_files(location_of_site, tool, tool_dir, new_location_of_site)
    gr = genome_reader(genome_path)
    print("start: ", start, "end: ", end)
    unconverted_seq = gr.get_fasta(chr, int(start-1), int(end-1))
    # print(unconverted_seq)
    #we should check this part! with it and without it:
    #seq_converted = convert_dna_to_formal_format(unconverted_seq)
    seq_converted = (blast.transcribe_dna_to_rna(unconverted_seq)).upper()
    # print("first", seq_converted)
    # add reverse complement  (-)
    if strand == "-":
        print("strand is minus!!")
        seq_converted = blast.reverse_complement_rna(seq_converted)
        # print("seq converted is:", seq_converted)
    # Check if new_location_of_site is within the bounds of the sequence
    if 0 <= new_location_of_site < len(seq_converted):
        nucleotide = seq_converted[new_location_of_site]
    distance = end - start
    fasta_seq_to_fold = write_to_fasta_file(location_of_site, seq_converted, chr, tool, tool_dir, distance) 
    # convert to dbn file
    # send it to the folding program:
    if is_file_empty(path_to_mxfold2_result):
        path_to_mxfold2_result = run_mxfold2(fasta_seq_to_fold, path_to_mxfold2_result)
        print(f"after mx by {tool} in {location_of_site}")
    if is_file_empty(ct_file_path):
        convert_dbn_to_ct(path_to_mxfold2_result, ct_file_path)
        print(f"ct_file was empty in {location_of_site}")
    print(f"after convertion to ct by {tool} in in {location_of_site}")

    if not (is_file_empty(ct_file_path)) and not (is_file_empty(shape_file_path)) and is_file_empty(svg_file_path):
        run_drawRNAstructure(ct_file_path, shape_file_path, svg_file_path)
        print(f"after drawRNAst by {tool} in {location_of_site}")
    
    # copy everything that's inside the mxfolded file 
    # shutil.copyfile(path_to_mxfold2_result, path_to_bpRNA_result)
    st_path = create_bpRNA_path(path_to_mxfold2_result, tool_dir)
    run_bpRNA(path_to_mxfold2_result, tool_dir, st_path)
    print(f"after bpRNA by {tool} in {location_of_site}")
    return st_path, nucleotide

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
    print("***************")
    tool_type_dir = f"{site_dir_path}{tool_type}/"
    print(f"the tool type is in : {tool_type_dir}")
    print("***************")
    if not os.path.exists(tool_type_dir):
        os.mkdir(tool_type_dir)
        return tool_type_dir
    else : return tool_type_dir

def run_by_tool_type(tool, dis_list, location_of_site, chr, genome_path, site_dir, strand):
    relevant_function = eval(f"{tool}.get_output_{tool}")
    start_point, end_point = relevant_function(dis_list, location_of_site)
    print(f"end - start in run_by_tool_type is {end_point - start_point} in {location_of_site}")
    # Initialize st_path to None or some default value
    st_path = ""

    if (start_point == 0 and end_point == 0):
        # st_path = ""
        print(f"st_path is none since start point and end point == 0 in {location_of_site}")
        return None, None, None, None
    
    else:
        dir = create_directory_by_tool_type(site_dir, tool)
        print(f"start - end in run by tool type after relevant function {end_point - start_point} in {location_of_site}")
        st_path, nucleotide = common_part_of_tool(chr, start_point, end_point, location_of_site, genome_path, tool, dir, strand)

        if st_path is None:
            return None, None, None, None
    return start_point, end_point, st_path, nucleotide

def open_json_file_for_reading(file):
    with open (file, 'r') as sites_from_genome_dict:
        sites_from_genome = json.load(sites_from_genome_dict)
        # return sites_from_genome
# line, genome_path, final_df_path, no_segment_df_path, orig_site_dir)
def process_line(line, genome_path, final_df_path, no_segment_df_path, orig_site_dir):
    if not check_bed_file_validity(line):
        no_segment_row = [int(location_of_site), tool, "Invalid BED file line: {line}"]
        with open(no_segment_df_path, 'a', newline='') as csvfile2:
            csvwriter2 = csv.writer(csvfile2)
            csvwriter2.writerow(no_segment_row)

    fields = line.strip().split('\t')
    dis_list, location_of_site, chr, strand= l_dis.pipline(fields)
    site_dir = f"{orig_site_dir}{chr}_{location_of_site}/"

    if not os.path.exists(site_dir):
        os.mkdir(site_dir)

    tools_list = ["ratio_based_tool", "default_tool", "max_distance_tool"]

    for tool in tools_list:
        start, end, st_path, nucleotide  = run_by_tool_type(tool, dis_list, location_of_site, chr, genome_path, site_dir, strand)
       
        if start is None or end is None or st_path is None:
            no_segment_row = [int(location_of_site), tool, "st_path is None"]
            with open(no_segment_df_path, 'a', newline='') as csvfile2:
                csvwriter2 = csv.writer(csvfile2)
                csvwriter2.writerow(no_segment_row)
                continue
        
        converted_start_first_strand, converted_end_first_strand, converted_start_second_strand, converted_end_second_strand = post_fold.extract_segment(start, end, st_path, location_of_site, strand)
        
        if (converted_start_first_strand is not None and 
            converted_end_first_strand is not None and 
            converted_start_second_strand is not None and 
            converted_end_second_strand is not None):
            
            # Prepare the row to write
            row = [
                chr, int(converted_start_first_strand), int(converted_end_first_strand),
                int(converted_start_second_strand), int(converted_end_second_strand),
                strand, int(location_of_site), "exp", tool, nucleotide,
            ]
            
            with open(final_df_path, 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(row)
            print(f"Row appended to {final_df_path} for location {location_of_site} using tool {tool}")
        else:
            no_segment_row = [int(location_of_site), tool, "one of the converted start/end is None"]
            with open(no_segment_df_path, 'a', newline='') as csvfile2:
                csvwriter2 = csv.writer(csvfile2)
                csvwriter2.writerow(no_segment_row)
    
def add_line_to_final_df(final_df, chr, start_first_strand, end_first_strand, start_second_strand, end_second_strand, strand, editing_site_location, exp_level, method, nucleotide):
    # Create a new row as a DataFrame
    new_row = pd.DataFrame({
        'chr': [chr],
        'start_first_strand': [start_first_strand],
        'end_first_strand': [end_first_strand],
        'start_second_strand': [start_second_strand],
        'end_second_strand': [end_second_strand],
        'strand': [strand],
        'editing_site_location': [editing_site_location],
        'exp_level': [exp_level],
        'method': [method],
        'editing_base': [nucleotide]
    })
    
    # Append the new row to the existing DataFrame
    final_df = pd.concat([final_df, new_row], ignore_index=True)
    
    return final_df

def sort_df(orig_path, file_name):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(orig_path)

    # Sort the DataFrame by the 'editing_site' column
    df_sorted = df.sort_values(by='editing_site_location')

    # Define the output file name
    output_file = f'sorted_{file_name}'

    # Save the sorted DataFrame to a new CSV file
    df_sorted.to_csv(output_file, index=False)

    # If you just want to see the sorted DataFrame
    return output_file

def create_no_segment_df():
    # Define the data structure with three columns
    data = {
        'editing_site_location': [],  # Column for the editing site location
        'method': [],                 # Column for the method
        'error': []                   # Column for the error
    }
    
    # Create the DataFrame with the specified structure
    df = pd.DataFrame(data)
    
    # Ensure the 'editing_site_location' column is treated as an integer
    df = df.astype({
        'editing_site_location': 'int'
    })
    
    return df

def create_final_table_structure():
    data = {
        'chr': [],
        'start_first_strand': [],
        'end_first_strand': [],
        'start_second_strand': [],
        'end_second_strand': [],
        'strand': [],
        'editing_site_location': [],
        'exp_level': [],
        'method': [],
        'editing_base': []
    }
    df = pd.DataFrame(data)
    
    # Ensure specific columns are treated as integers
    df = df.astype({
        'start_first_strand': 'int',
        'end_first_strand': 'int',
        'start_second_strand': 'int',
        'end_second_strand': 'int',
        'editing_site_location': 'int'
    })
    
    return df

def united_main():
    bed_file_path = "/private10/Projects/Reut_Shelly/our_tool/data/convert_sites/sites_for_analysis/split_sites/sites_3001_4000.bed"
    genome_path = "/private/dropbox/Genomes/Human/hg38/hg38.fa"
    orig_site_dir = "/private10/Projects/Reut_Shelly/our_tool/data/division_to_1000/3001-4000/"
    final_df_path = os.path.join(orig_site_dir, "final_df.csv")
    no_segment_df_path = os.path.join(orig_site_dir, "no_segment_df.csv")

    # Write the header of the CSV files
    header_final_df = [
        'chr', 'start_first_strand', 'end_first_strand',
        'start_second_strand', 'end_second_strand', 
        'strand', 'editing_site_location', 'exp_level', 'method', 'editing_base'
    ]
    header_no_segment = ['editing_site_location', 'method', 'error']
    
    with open(final_df_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header_final_df)

    with open(no_segment_df_path, 'w', newline='') as csvfile2:
        csvwriter2 = csv.writer(csvfile2)
        csvwriter2.writerow(header_no_segment)

    with open(bed_file_path, 'r') as bed_file:
        lines = bed_file.readlines()

    # for line in lines:
    #     process_line(line, genome_path, final_df_path, no_segment_df_path, orig_site_dir)

    with multiprocessing.Pool(processes=35) as pool:
        pool.starmap(process_line, [(line, genome_path, final_df_path, no_segment_df_path, orig_site_dir) for line in lines])
    
    sorted_final_df = sort_df(final_df_path, "sorted_final_df")
    sorted_no_segment_df = sort_df(no_segment_df_path, "sorted_no_segment")
    print("EVERYTHING IS DONE")

if __name__ == "__main__":
    united_main()