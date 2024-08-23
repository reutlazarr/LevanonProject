import re
import os
import pandas as pd

# the function will take the original numbering and change it to match the new numbering of the coloring software
def ReNumber_the_sequence(start, end, location_of_site):
    start = round(start)
    end = round(end)
    new_start = 1
    new_end = end - start + 1
    delta = start - new_start  
    new_location_of_site = location_of_site - start + 1 
    print("new location of site:" , new_location_of_site)
    return (new_start, new_end, new_location_of_site, delta)

def parse_st_file(st_file, location_of_site):
    # Initialize default values
    # coords_of_segment = pd.DataFrame(columns=["start1", "end1", "start2", "end2"])
    seqs_of_segment = "default_seqs"
    segment = "default_segment"
    length = "default_length"
    start_first_strand = "default" 
    end_first_strand = "default"
    start_second_strand = "default"
    end_second_strand = "default"
    # Check if the file exists
    if not os.path.exists(st_file):
        print(f"Error: The file {st_file} does not exist.")
        # return coords_of_segment, seqs_of_segment, segment, length
        return start_first_strand, end_first_strand, start_second_strand, end_second_strand

    # Open the file
    with open(st_file, "r") as bpf:
        data = bpf.readlines()

    # Regex: 123...456
    regex = re.compile(r"(\s\d+\.\.\d+\s)")
    for line in data:
        # If we are in the bottom part of the file which looks like this: "segment1 3bp 12..14 AGG 878..880 CCU"
        if "segment" in line:
            l = regex.split(line)    # Split the line this way: ['segment1 3bp', ' 12..14 ', 'AGG', ' 878..880 ', 'CCU']
            segment_and_length = l[0] # 'segment1 3bp'
            
            split_segment_and_length = segment_and_length.split()
            segment = split_segment_and_length[0] # segment1
            length = split_segment_and_length[1] # 3bp
            range1 = l[1].strip() # Remove spaces from '  12..14  '
            range1 = {
                "start": int(range1.split(".")[0]), # 12
                "end": int(range1.split(".")[-1]), # 14
            }
            range2 = l[3].strip() # Same with the second range
            range2 = {
                "start": int(range2.split(".")[0]),
                "end": int(range2.split(".")[-1]),
            }
            # Check if the editing site is in that segment
            if (range1["start"] <= location_of_site + 1 <= range1["end"]) or (
                range2["start"] <= location_of_site + 1 <= range2["end"]
            ):
                # Create DataFrame for the requested segment
                start_first_strand = range1["start"]
                end_first_strand = range1["end"]
                start_second_strand = range2["start"]
                end_second_strand = range2["end"]
                seqs_of_segment = (l[2], l[-1].strip("\n")) # seqs_of_segment is ('AGG', 'CCU')
                break  # Ensures that you stop searching once a match is found

    return start_first_strand, end_first_strand, start_second_strand, end_second_strand


def convert_to_genomic_coords(start_first_strand, end_first_strand, start_second_strand, end_second_strand, delta):
    if start_first_strand == "default" or end_first_strand == "default" or start_second_strand == "default" or end_second_strand == "default":
        print("Error: start/end of the segments are empty.")
        return None, None, None, None  # Return four None values to avoid unpacking errors
    
    # Add delta to the DataFrame coordinates
    converted_start_first_strand = start_first_strand + delta
    converted_end_first_strand = end_first_strand + delta
    converted_start_second_strand = start_second_strand + delta
    converted_end_second_strand = end_second_strand + delta
    return converted_start_first_strand, converted_end_first_strand, converted_start_second_strand, converted_end_second_strand


def extract_segment(start, end, st_path, location_of_site):
    new_start, new_end, new_location_of_site, delta = ReNumber_the_sequence(start, end, location_of_site)
    print(f"new_location_of_site {new_location_of_site}")
    print(f"the new start is : {new_start} ,the new end is: {new_end} ,the new location of site is: {new_location_of_site}")
    # coords of the location of site's segment
    start_first_strand, end_first_strand, start_second_strand, end_second_strand = parse_st_file(st_path, new_location_of_site)
    converted_start_first_strand, converted_end_first_strand, converted_start_second_strand, converted_end_second_strand = convert_to_genomic_coords(start_first_strand, end_first_strand, start_second_strand, end_second_strand, delta)
    # Handle the case where segments were not found
    if converted_start_first_strand is None:
        print("Error: Could not convert to genomic coordinates. Returning None values.")
        return None, None, None, None
    
    return converted_start_first_strand, converted_end_first_strand, converted_start_second_strand, converted_end_second_strand