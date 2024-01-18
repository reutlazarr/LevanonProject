import subprocess
from get_fasta import genome_reader
from Bio import SeqIO
from Bio.Seq import Seq
import os
from Bio.Blast import NCBIWWW

#The code will look for base pairing near the relevant editing site by ab-blast.

global_genome_path = "/private/dropbox/Genomes/Human/hg38/hg38.fa"
gr = genome_reader(global_genome_path)


def transcribe_dna_to_rna(dna_sequence):
    """
    Transcribes a DNA sequence to an RNA sequence using Biopython.

    Parameters:
    - dna_sequence (str): The input DNA sequence.

    Returns:
    - str: The transcribed RNA sequence.
    """
    # Create a Biopython Seq object from the DNA sequence
    dna_seq = Seq(dna_sequence)

    # Use the transcribe() function to get the RNA sequence
    rna_sequence = dna_seq.transcribe()

    return str(rna_sequence)

#Extract the entire sequence of a chromosome from a FASTA file.
#input : fasta_file: Path to the FASTA file, chromosome_id: Identifier of the chromosome to extract
#output: The entire sequence of the chromosome as a string or None if the chromosome ID is not found
def extract_chromosome_sequence(global_genome_path, chromosome_id):
    with open(global_genome_path, 'r') as handle:
        for record in SeqIO.parse(handle, 'fasta'):
            if record.id == chromosome_id:
                return str(record.seq)
    return None

def calculate_chrom_size(chrom):
    whole_chr_seq = extract_chromosome_sequence(global_genome_path,chrom)
    chrom_size = len(whole_chr_seq)
    return chrom_size

def extract_sequences_from_genome(chr, start, end):
    substrate_seq = gr.get_fasta(chr, start, end)
    return substrate_seq


#Extract the sequence of the substrate sequence that we will search in it in with abblat the checked sequence
#input: thr chromosome ID and the location of editing site
#output: substrate_seq
def extract_substrate_seq(chr, chrom_size, location_of_site):
    site_window = 5000
    # checked_seq = our_tool.get_sequence(best_ratio_based_list,sites_from_genome_path)
    if location_of_site < site_window:
        start = 1
        end = (site_window*2) +1
        substrate_seq = extract_sequences_from_genome(chr, start, end)
        rna_substrate_seq = transcribe_dna_to_rna(substrate_seq)
        upper_rna_substrate_seq = rna_substrate_seq.upper()
        return upper_rna_substrate_seq
    elif (chrom_size - location_of_site < site_window): 
        start = chrom_size - (site_window*2)  
        end = chrom_size
        substrate_seq = extract_sequences_from_genome(chr, start, end)
        rna_substrate_seq = transcribe_dna_to_rna(substrate_seq)
        upper_rna_substrate_seq = rna_substrate_seq.upper()
        return upper_rna_substrate_seq
    else:
        start = location_of_site - site_window
        end = location_of_site + site_window
        substrate_seq = extract_sequences_from_genome(chr, start, end)
        rna_substrate_seq = transcribe_dna_to_rna(substrate_seq)
        upper_rna_substrate_seq = rna_substrate_seq.upper()
        return upper_rna_substrate_seq

def extract_minimal_check_seq(chr, chrom_size, location_of_site, minimal_window):
    start_crom = 1
    #minimal_window = 40
    # Checking if the editing site is located far enougth from the beginning of the chromosome realte to the minimal window
    if int(location_of_site) > (minimal_window / 2):
        # Checking if the editing site is located far enougth from the end of the chromosome realte to the minimal window
        if location_of_site < chrom_size - (minimal_window/2):
            start = int(location_of_site - (minimal_window/2)) 
            end = int(location_of_site + (minimal_window/2))
            minimal_check_seq = extract_sequences_from_genome(chr, start, end)
            rna_check_seq = transcribe_dna_to_rna(minimal_check_seq)
            upper_rna_check_seq = rna_check_seq.upper()
            return upper_rna_check_seq
        start = int(chrom_size - minimal_window)
        end = int(chrom_size)
        minimal_check_seq = extract_sequences_from_genome(chr, start, end)
        rna_check_seq = transcribe_dna_to_rna(minimal_check_seq)
        upper_rna_check_seq = rna_check_seq.upper()
        return upper_rna_check_seq
    elif location_of_site < (minimal_window / 2) :
        start = int(start_crom)
        end = int(minimal_window)
        minimal_check_seq = extract_sequences_from_genome(chr, start, end)
        rna_check_seq = transcribe_dna_to_rna(minimal_check_seq)
        upper_rna_check_seq = rna_check_seq.upper()
        return upper_rna_check_seq
    
#creating fasta files to the checked sequence and to the substrate sequence
def create_fasta_files(chrom, checked_seq, substrate_seq, location_of_site):
    header_of_checked_seq = f">sequence of checked sequence in {chr} "
    fasta_string_of_checked_seq = f"{header_of_checked_seq}\n{checked_seq} in {chrom}\n"
    checked_seq_path = f"/private10/Projects/Reut_Shelly/our_tool/data/fasta_files/{location_of_site}_rna_checked_seq.fa"
    header_of_substrate_seq = f">sequence of substrate sequence in {chr}"
    fasta_string_of_substrate_seq = f"{header_of_substrate_seq}\n{substrate_seq}\n"
    substrate_seq_path = f"/private10/Projects/Reut_Shelly/our_tool/data/fasta_files/{location_of_site}_rna_substrate_seq.fa"
    
    if not os.path.exists(checked_seq_path):
        with open(checked_seq_path,"a") as checked_seq_file :
            checked_seq_file.write(fasta_string_of_checked_seq)
    
    if not os.path.exists(substrate_seq_path):        
        with open(substrate_seq_path, "a") as substrate_seq_file:
            substrate_seq_file.write(fasta_string_of_substrate_seq)
    return checked_seq_path, substrate_seq_path

def work_with_fasta_files(location_of_site):
    checked_seq_path = f"/private10/Projects/Reut_Shelly/our_tool/data/fasta_files/{location_of_site}_checked_seq.fa"
    substrate_seq_path = f"/private10/Projects/Reut_Shelly/our_tool/data/fasta_files/{location_of_site}_substrate_seq.fa"
    return checked_seq_path, substrate_seq_path

def preparation_for_first_run_abblast(chrom ,location_of_site, minimal_window):
    chrom_size = int(calculate_chrom_size(chrom))
    substrate_seq = extract_substrate_seq(chrom, chrom_size, location_of_site)
    checked_seq = extract_minimal_check_seq(chrom, chrom_size, location_of_site, minimal_window)
    (checked_seq_path, substrate_seq_path) = create_fasta_files(chrom ,checked_seq, substrate_seq, location_of_site)
    return (checked_seq_path, substrate_seq_path)

def create_xdformat_to_substrate_seq(substrate_seq_path):
    xdformat_path = f"{substrate_seq_path}.xnd"
    if not os.path.exists(xdformat_path):
        xdformat = "/private10/Projects/Reut_Shelly/our_tool/ABblast/ab-blast-20200317-linux-x64/xdformat"
        cmd = f"{xdformat} -n {substrate_seq_path}"
        subprocess.run(cmd, shell=True)

def run_blast(checked_seq_path, substrate_seq_path):
    #I need to add blast_output_path and save to it the data that is accepted by the running
    #I need to understand how to change the G-U definition
    blast_output_path="/private10/Projects/Reut_Shelly/our_tool/ABblast/checking/tmp_blast_output.csv"
    #blast_cmd = [blast_program, '-query', query_file, '-db', database, '-out', output_file, '-outfmt', '10']
    #cmd = f"{xblast} {substrate_seq_path} {checked_seq_path} -out {blast_output_path} -outfmt 10"
    #the path of the xblast
    ab_blastn = "/private10/Projects/Reut_Shelly/our_tool/ABblast/ab-blast-20200317-linux-x64/ab-blastn"
    cmd = f"{ab_blastn} {substrate_seq_path} {checked_seq_path} -matrix RNAfull"
    # -m DNAfull -evalue 0.001
    subprocess.run(cmd, shell=True)

#ab-blast searching for base paring
#we will search for base paring for (+) to (-) strands 
#input- location of site and the minimal window we want to check
#output- relevant parameters after the blast running
def united_abblast(chrom ,location_of_site, minimal_window):
    (checked_seq_path, substrate_seq_path) = preparation_for_first_run_abblast(chrom ,location_of_site, minimal_window)
    create_xdformat_to_substrate_seq(substrate_seq_path)
    run_blast(checked_seq_path, substrate_seq_path)

def first_run_on_abblast(chrom , minimal_check_seq, substrate_seq):
    simalirity_result = united_abblast()
    threshold_num = 10
    if simalirity_result < threshold_num:
        return True
    else: return False

# If the distance we got from the relation's function is lower than 300, we will use it.
# else we will take defualt distance of 300bp
#def second_run_on_blast():
    
    

if __name__ == "__main__":
    #united_abblast("chrY", int(3218829) ,int(100))
    #print("finally done")
    # Your query and subject RNA sequences
    query_sequence = "ACGUAGCUAGCUAGCUAGCUAGCUAGCUAGCUAGCUAGCUAGCUAGCUAGCUAGCUAGCUAGC"
    subject_sequence = "UAGCUAGCUAGCUAGCUAGCUAGCUAGCUAGCUAGCUAGCUAGCUAGCUAGCUAGCUAGCUAGC"

    # Perform BLAST search
    result_handle = NCBIWWW.qblast("blastn", "nt", query_sequence, subject_sequence)
    print (result_handle.read())

    # blast_result = 
    # # Save the result to a file
    # with open("blast_result.xml", "a") as out_handle:
    #     out_handle.write(result_handle.read())

    # # Close the result handle
    # result_handle.close()