import re
import os
import pandas as pd

# the function will take the original numbering and change it to match the new numbering of the coloring software
def ReNumber_the_sequence(start, end, location_of_site, strand):
    start = round(start)
    end = round(end)
    new_start = 1
    new_end = end - start + 1

    if strand == "+":
        delta = start
        new_location_of_site = location_of_site - delta
    elif strand == "-":
        delta = end
        new_location_of_site = delta - location_of_site - 1
    else:
        raise ValueError(f"Invalid strand value: {strand}")

    print("new location of site:", new_location_of_site)
    return new_start, new_end, new_location_of_site, delta



def parse_st_file(st_file, new_location_of_site):
    # Initialize default values
    seqs_of_segment = "default_seqs"
    segment = "default_segment"
    length = "default_length"
    start_first_strand = None 
    end_first_strand = None
    start_second_strand = None
    end_second_strand = None
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
            print(f'range1["start"] {range1["start"]}')
            print(f'range1["end"] {range1["end"]}')
            print(f'range2["start"] {range2["start"]}')
            print(f'range2["end"] {range2["end"]}')
            if (range1["start"] <= new_location_of_site <= range1["end"]) or (
                range2["start"] <= new_location_of_site <= range2["end"]
            ):
                print("THE CONDITION CHECKING IF LOCATION IN IN THE SEGMENT")
                # Create DataFrame for the requested segment
                start_first_strand = range1["start"]
                end_first_strand = range1["end"]
                start_second_strand = range2["start"]
                end_second_strand = range2["end"]
                seqs_of_segment = (l[2], l[-1].strip("\n")) # seqs_of_segment is ('AGG', 'CCU')
                break  # Ensures that you stop searching once a match is found
    return start_first_strand, end_first_strand, start_second_strand, end_second_strand


def convert_to_genomic_coords(start_first_strand, end_first_strand, start_second_strand, end_second_strand, delta, strand):
    if None in [start_first_strand, end_first_strand, start_second_strand, end_second_strand]:
        print("Error: start/end of the segments are empty.")
        return None

    print("Start first strand and the rest are not None")

    if strand == "+":
        converted_start_first_strand = start_first_strand + delta
        converted_end_first_strand = end_first_strand + delta
        converted_start_second_strand = start_second_strand + delta
        converted_end_second_strand = end_second_strand + delta
    elif strand == "-":
        converted_start_first_strand = delta - end_first_strand
        converted_end_first_strand = delta - start_first_strand
        converted_start_second_strand = delta - end_second_strand
        converted_end_second_strand = delta - start_second_strand
    else:
        raise ValueError(f"Invalid strand value: {strand}")

    return (
        converted_start_first_strand,
        converted_end_first_strand,
        converted_start_second_strand,
        converted_end_second_strand,
    )



def extract_segment(start, end, st_path, location_of_site, strand):
    if start is None or end is None:
        print("Error: Start or end is None, skipping segment extraction.")
        return None
    print(f"@@ before renumber start: {start}, end: {end}, loc: {location_of_site}, strand: {strand}")
    new_start, new_end, new_location_of_site, delta = ReNumber_the_sequence(start, end, location_of_site, strand)
    print(f"DELTA in extract segment {delta}")
    print(f"After renumber the seq:  the new start is : {new_start} ,the new end is: {new_end} ,the new location of site is: {new_location_of_site} delta: {delta}" )
    # coords of the location of site's segment
    
    start_first_strand, end_first_strand, start_second_strand, end_second_strand = parse_st_file(st_path, new_location_of_site)
    if start_first_strand is None or end_first_strand is None or start_second_strand is None or end_second_strand is None:
        print("Error: parse_st_file fails since the editing site is not in a segment")
        return None
    print(f"@@ strands after psrse_st_file start_first: {start_first_strand}, end_first: {end_first_strand}, start_sec: {start_second_strand}, end_sec: {end_second_strand}")
    if start_first_strand <= new_location_of_site <= end_first_strand or start_second_strand <= new_location_of_site <= end_second_strand:
        print("loc is IN segment right after parse_st_file (new_location_of_site)")
    else:
        print("loc is NOT IN segment right after parse_st_file (new_location_of_site)")
    # def convert_to_genomic_coords(start_first_strand, end_first_strand, start_second_strand, end_second_strand, delta):
    result = convert_to_genomic_coords(start_first_strand, end_first_strand, start_second_strand, end_second_strand, delta, strand)
    if result is not None:
        converted_start_first_strand, converted_end_first_strand, converted_start_second_strand, converted_end_second_strand = result
        print(f"@@ strands after convert_to_genomics {converted_start_first_strand}, {converted_end_first_strand}, {converted_start_second_strand}, {converted_end_second_strand}")
        if converted_start_first_strand <= location_of_site <= converted_end_first_strand or converted_start_second_strand <= location_of_site <= converted_end_second_strand:
            print("loc is IN segment right after convert_to_genomics_coords (loc_of_site)")
            return result
        else:
            print("loc is NOT IN segment right after convert_to_genomics_coords (loc_of_site)")
        # Handle the case where segments were not found
    else:
        print("DDDDD result is None")
        return None

