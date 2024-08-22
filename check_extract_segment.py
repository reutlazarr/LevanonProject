import re
import os
import pandas as pd


# the function will take the original numbering and change it to match the new numbering of the coloring software
def ReNumber_the_sequence(start, end, location_of_site):
    print ("old start: " , start)
    print("old end: ", end)
    print("old site: " , location_of_site)
    start = round(start)
    end = round(end)
    new_start = 1
    new_end = end - start + 1
    delta = start - new_start 
    print("new end: " , new_end)     
    new_location_of_site = location_of_site - start + 1 
    print("new location of site:" , new_location_of_site)
    return (new_start, new_end, new_location_of_site, delta)

def parse_st_file(st_file, location_of_site):
    # Initialize default values
    print("here1")
    coords_of_segment = pd.DataFrame(columns=["start1", "end1", "start2", "end2"])
    print("here2")
    seqs_of_segment = "default_seqs"
    segment = "default_segment"
    length = "default_length"
    print("here3")
    # Check if the file exists
    if not os.path.exists(st_file):
        print(f"Error: The file {st_file} does not exist.")
        return coords_of_segment, seqs_of_segment, segment, length

    # Open the file
    with open(st_file, "r") as bpf:
        data = bpf.readlines()

    # Regex: 123...456
    regex = re.compile(r"(\s\d+\.\.\d+\s)")
    for line in data:
        print("here4")
        # If we are in the bottom part of the file which looks like this: "segment1 3bp 12..14 AGG 878..880 CCU"
        if "segment" in line:
            print("hereeeeeeeee")
            l = regex.split(line)    # Split the line this way: ['segment1 3bp', ' 12..14 ', 'AGG', ' 878..880 ', 'CCU']
            print(l)
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
                print("here5")
                coords_of_segment = pd.DataFrame({
                    "start1": [range1["start"]],
                    "end1": [range1["end"]],
                    "start2": [range2["start"]],
                    "end2": [range2["end"]],
                })
                print("here6")
                seqs_of_segment = (l[2], l[-1].strip("\n")) # seqs_of_segment is ('AGG', 'CCU')
                break  # Ensures that you stop searching once a match is found

    return coords_of_segment, seqs_of_segment, segment, length


def convert_to_genomic_coords(coords_of_segment, delta):
    if coords_of_segment.empty:
        print("Error: coords_of_segment DataFrame is empty.")
        return pd.DataFrame(columns=["start1", "end1", "start2", "end2"])

    print("coords of segmentttt\n")
    print(coords_of_segment["start1"].iloc[0])
    print(type(coords_of_segment["start1"].iloc[0]))

    # Add delta to the DataFrame coordinates
    genomic_coords_of_segment = coords_of_segment.copy()
    genomic_coords_of_segment["start1"] += delta
    genomic_coords_of_segment["end1"] += delta
    genomic_coords_of_segment["start2"] += delta
    genomic_coords_of_segment["end2"] += delta

    return genomic_coords_of_segment


def extract_segment(start, end, st_path, location_of_site):
    new_start, new_end, new_location_of_site, delta = ReNumber_the_sequence(start, end, location_of_site)
    print(f"new_start {new_start}")
    print(f"new_end {new_end}")
    print(f"new_location_of_site {new_location_of_site}")
    print(f"the new start is : {new_start} ,the new end is: {new_end} ,the new location of site is: {new_location_of_site}")
    # coords of the location of site's segment
    coords_of_segment, seqs_of_segment, segment, length = parse_st_file(st_path, new_location_of_site)
    genomic_coords_of_segment = convert_to_genomic_coords(coords_of_segment, delta)
    return genomic_coords_of_segment, seqs_of_segment, segment, length


start = 632939
end = 633472
st_path = "/private10/Projects/Reut_Shelly/our_tool/data/sites_analysis_update/chr1_632939/default_tool/632939_default_tool_mxfolded.st"
location_of_site = 632939
extract_segment(start, end, st_path, location_of_site)