# list of seq - the entire seq
# list of features - all the features
# loc -  המיקום הגנומי

# extract the segment:
# נקרא לפונקציה שמחלצת את המיקום של אתר העריכה בקובץ הST

import pandas as pd 
import csv
# call the function that 
# extract the genomic location of the fasta (common..)
# extract the st location (renumber...)
# new_start, new_end, new_location_of_site = Renumber_the_sequence()
# extract the segment using itamar's code
# coords_of_segment, seqs_of_segment, stem_length = parse_st_file(st_file, location_of_site)
# check if the seq is on the first_strand or sec_strand
# given the segment:
# כל הדברים פה הם ביחס לST 


# רשימה של המבנים באזור אתר העריכה
# 
coords_of_segment, seqs_of_segment, stem_length = parse_st_file(st_file, location_of_site)
# call st_parse_by zohar in order to create each editijg site's lists
# create_df_structure

# the func's output is two lists in which the first one is the sites evolving bases and the second one is the site's structures
def process_st_file_by_shelly(st_file, pos_of_editing_site, range_of_interest):
    list_of_seq = []
    list_of_features = []
    # open the st file
    with open(st_file, 'r') as file:
        # annotation is each line
        annotation = file.read().split('\n')
        # first linE
    name = annotation[0]
    # Second line
    seq_length = annotation[1]
    # the actual sequence (line 4)
    cur_sequence = annotation[3]
    # the dot bracket part (line 5)
    cur_structure = annotation[4]
    # E S I etc
    features = annotation[5]

    # the interesting part - probably 40 bases for each site
    start_range = pos_of_editing_site - range_of_interest
    end_range = pos_of_editing_site + range_of_interest
    pass
def check_strand_identity(coords_of_segment):
    
    return start_of_first_strand, end_of_first_strand, start_of_sec_strand, end_of_sec_strand, editing_on_first_strand, editing_on_sec_strand
def create_df_structure(file_path):
    # "number of X" is among the 81 bases in the vicinity
    column_names = [["stem length", "editing location feature", "number of I", "number of S", "number of H", "number of E", "number of B", "number of M"]]
    # Specify the location and name of the CSV file
    df = pd.DataFrame(column_names)
    # Save the DataFrame to a CSV file
    df.to_csv(file_path, index=False)
    return file_path

def fill_df_with_data():
    pass

def catogarize_features():
    m_count = 0
    s_count = 0 
    h_count = 0
    i_count = 0
    e_count = 0 
    b_count = 0

    pass

# def parse_st_file(st_file, location_of_site):
#         with open(st_file, "r") as bpf:
#             data = bpf.readlines()
#         regex = re.compile(r"(\s\d+\.\.\d+\s)")
#         for line in data:
#             if "segment" in line:
#                 l = regex.split(line)
#                 pattern_of_bp = re.compile(r"(\d+)bp")
#                 range1 = l[1].strip()
#                 range1 = {
#                     "start": int(range1.split(".")[0]),
#                     "end": int(range1.split(".")[-1]),
#                 }
#                 range2 = l[3].strip()
#                 range2 = {
#                     "start": int(range2.split(".")[0]),
#                     "end": int(range2.split(".")[-1]),
#                 }
#                 # if the editing site is in that segmant
#                 if (range1["start"] <= location_of_site + 1 <= range1["end"]) or (
#                     range2["start"] <= location_of_site + 1 <= range2["end"]
#                 ):
#                     coords_of_segment = (
#                         range1["start"],
#                         range1["end"],
#                         range2["start"],
#                         range2["end"],
#                     )
#                     seqs_of_segment = (l[2], l[-1].strip("\n"))
#                     match = pattern_of_bp.match(line)
#                     if match:
#                          stem_length =  match.group(1)
#                     else:
#                          print("no bp found")
#                     return (coords_of_segment, seqs_of_segment, stem_length)
#         # if we our editng site is in any segment
#         return (0, 0)


