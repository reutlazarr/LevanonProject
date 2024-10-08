import re
import os
import pandas as pd

# the function will take the original numbering and change it to match the new numbering of the coloring software
def ReNumber_the_sequence(start, end, location_of_site, strand):
    # start = 3000, end = 4000, loc = 3200
    # new_start = 1, end = 1001, loc = 201
    # delta = start - new_start = 3000 - 1 = 2999
    # new_loc = 3200 - 2999 = 201 = delta
    # the correct one : new_loc = loc - start = 3200 - 300 = 200
    start = round(start)
    end = round(end)
    new_start = 1
    new_end = end - start + 1
    delta = start
    new_location_of_site = location_of_site - delta 

    if strand == "-":
        new_location_of_site = new_end - new_location_of_site - 1
    print("new location of site:" , new_location_of_site)
    return (new_start, new_end, new_location_of_site, delta)


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


def convert_to_genomic_coords(start_first_strand, end_first_strand, start_second_strand, end_second_strand, delta):
    if start_first_strand == None or end_first_strand == None or start_second_strand == None or end_second_strand == None:
        print("Error: start/end of the segments are empty.")
        return None, None, None, None  # Return four None values to avoid unpacking errors
    print("start first strand and the rest are not None")
    # Add delta to the DataFrame coordinates
    converted_start_first_strand = start_first_strand + delta
    converted_end_first_strand = end_first_strand + delta
    converted_start_second_strand = start_second_strand + delta
    converted_end_second_strand = end_second_strand + delta
    return converted_start_first_strand, converted_end_first_strand, converted_start_second_strand, converted_end_second_strand


def extract_segment(start, end, st_path, location_of_site, strand):
    if start is None or end is None:
        print("Error: Start or end is None, skipping segment extraction.")
        return None, None, None, None
    new_start, new_end, new_location_of_site, delta = ReNumber_the_sequence(start, end, location_of_site, strand)
    print(f"After renumber the seq:  the new start is : {new_start} ,the new end is: {new_end} ,the new location of site is: {new_location_of_site}")
    # coords of the location of site's segment
    start_first_strand, end_first_strand, start_second_strand, end_second_strand = parse_st_file(st_path, new_location_of_site)
    if start_first_strand is None or end_first_strand is None or start_second_strand is None or end_second_strand is None:
        print("Error: parse_st_file fails since the editing site is not in a segment")
        return None, None, None, None
    converted_start_first_strand, converted_end_first_strand, converted_start_second_strand, converted_end_second_strand = convert_to_genomic_coords(start_first_strand, end_first_strand, start_second_strand, end_second_strand, delta)
    # Handle the case where segments were not found
    if converted_start_first_strand is None or converted_end_first_strand is None or converted_start_second_strand is None or converted_end_second_strand is None:
        print("Error: conversion to genomic coords failed")
        return None, None, None, None
    
    print("coordinates are converted to genomics successfully")
    if (converted_start_first_strand <= location_of_site <= converted_end_first_strand) or (converted_start_second_strand <= location_of_site <= converted_end_second_strand):
        print ("loc in segment in extract_segment")
        return converted_start_first_strand, converted_end_first_strand, converted_start_second_strand, converted_end_second_strand
    else:
        print("loc NOT in segment in extract_segment")
        return None, None, None, None
